import math

def calculate_optimal_iterations(n_qubits):
    # N = 2^nQubits
    N = 2 ** n_qubits
    
    # Grover's algorithm optimal iterations: pi/4 * sqrt(N)
    grover_iterations = (math.pi / 4) * math.sqrt(N)
    
    # Round to nearest integer
    iterations = round(grover_iterations)
    
    return iterations

# Example usage for 128 qubits
n_qubits = 128
iterations = calculate_optimal_iterations(n_qubits)
print(f"Optimal iterations for Grover's algorithm with {n_qubits} qubits: {iterations}")
