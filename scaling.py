import numpy as np
import pandas as pd

# Input data for 128, 192, and 256 qubits
data = {
    "Qubits": [128, 192, 256],
    "#CNOT": [296396, 334896, 414568],
    "#1qCliff": [39096, 43864, 53983],
    "#T": [206220, 232680, 289212],
    "T-depth": [120, 144, 168],
    "#qubit (M)": [6288, 6608, 6896],
    "Full depth": [710, 850, 997],
    "Td-M cost (Td x M)": [754560, 951552, 1158528],
    "FD-M cost (FD x M)": [4464480, 5616800, 6875312]
}

# Convert the data into a DataFrame
df = pd.DataFrame(data)

# Function to extrapolate values for a given number of qubits
def extrapolate_values(df, target_qubits):
    qubits = df["Qubits"].values
    results = {}
    
    for column in df.columns[1:]:  # Skip the "Qubits" column
        values = df[column].values
        log_qubits = np.log(qubits)
        log_values = np.log(values)

        # Perform linear regression in log-log space
        coefficients = np.polyfit(log_qubits, log_values, 1)
        slope, intercept = coefficients

        # Extrapolate for the target qubits
        extrapolated_value = np.exp(intercept) * target_qubits ** slope
        results[column] = extrapolated_value

    return results

# Extrapolate for 31 and 62 qubits
target_qubits = [5, 12, 24]
extrapolated_data = []

for q in target_qubits:
    extrapolated_data.append({"Qubits": q, **extrapolate_values(df, q)})

# Convert extrapolated data into a DataFrame
extrapolated_df = pd.DataFrame(extrapolated_data)

# Combine original and extrapolated data into a single DataFrame
combined_df = pd.concat([extrapolated_df, df]).sort_values(by="Qubits").reset_index(drop=True)

# Generate AQRE-Compatible Parameters
def generate_aqre_parameters(row):
    t_count = int(row["#T"])
    aux_qubit_count = int(row["#qubit (M)"])
    rotation_count = int(row["#1qCliff"])  # Approximation
    rotation_depth = int(row["T-depth"] + 0.1 * row["#CNOT"])
    measurement_count = int(np.log2(row["#qubit (M)"]))  # Approximation based on qubit count
    
    print(f"AQRE Parameters for {int(row['Qubits'])} qubits:")
    print(f"TCount({t_count}), AuxQubitCount({aux_qubit_count}), "
          f"RotationCount({rotation_count}), RotationDepth({rotation_depth}), "
          f"MeasurementCount({measurement_count})")
    print("-" * 50)

# Display AQRE parameters for all qubits
for _, row in combined_df.iterrows():
    generate_aqre_parameters(row)
