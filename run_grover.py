import json
import qsharp
from argparse import ArgumentParser

# Initialize Q# project
qsharp.init(project_root=".")

# Define the resource estimation parameters
def get_resource_estimates():
    params = [
        {
            "errorBudget": 0.01,
            "qubitParams": {"name": "qubit_gate_ns_e3"},
            "qecScheme": {"name": "surface_code"},
                        "constraints": {
                "logicalDepthFactor": 1,
                "maxTFactories": 5
            }
        }
    ]

    # Run the Q# operation and get resource estimates
    res = qsharp.estimate(
        "g.Main",
        params=params
    )

    return json.loads(res.json)

# Process the resource estimation results
def process_results(results):
    if isinstance(results, dict):
        results = [results]

    data = []
    for item in results:
        data_item = []

        # Run name
        data_item.append(item["jobParams"]["qubitParams"]["name"])

        # T factory fraction and Runtime
        if "physicalCountsFormatted" in item:
            data_item.append(
                item["physicalCountsFormatted"]["physicalQubitsForTfactoriesPercentage"]
            )
            data_item.append(item["physicalCountsFormatted"]["runtime"])
        elif "frontierEntries" in item:
            data_item.append(
                item["frontierEntries"][0]["physicalCountsFormatted"][
                    "physicalQubitsForTfactoriesPercentage"
                ]
            )
            data_item.append(
                item["frontierEntries"][0]["physicalCountsFormatted"]["runtime"]
            )
        else:
            data_item.append("-")
            data_item.append("-")

        # Physical qubits and rQOPS
        if "physicalCounts" in item:
            data_item.append(item["physicalCounts"]["physicalQubits"])
            data_item.append(item["physicalCounts"]["rqops"])
        elif "frontierEntries" in item:
            data_item.append(
                item["frontierEntries"][0]["physicalCounts"]["physicalQubits"]
            )
            data_item.append(
                item["frontierEntries"][0]["physicalCounts"]["rqops"]
            )
        else:
            data_item.append("-")
            data_item.append("-")

        data.append(data_item)

    return data

# Format and display the results
def display_results(data):
    # Define the table headers
    headers = ["Run name", "T factory fraction", "Runtime", "Physical qubits", "rQOPS"]

    # Determine the width of each column
    col_widths = [max(len(str(item)) for item in column) for column in zip(headers, *data)]

    # Function to format a row
    def format_row(row):
        return " | ".join(
            f"{str(item).ljust(width)}" for item, width in zip(row, col_widths)
        )

    # Create the table
    header_row = format_row(headers)
    separator_row = "-+-".join("-" * width for width in col_widths)
    data_rows = [format_row(row) for row in data]

    # Print the table
    print(header_row)
    print(separator_row)
    for row in data_rows:
        print(row)

    print("\nFor more detailed resource counts, see file resource_estimate.json")

# Main execution
if __name__ == "__main__":
    parser = ArgumentParser(description="Run resource estimation for Grover's algorithm")
    parser.add_argument(
        "-o", "--output", default="resource_estimate.json", help="Path to save the resource estimate results"
    )
    args = parser.parse_args()

    print("Running resource estimation...")
    estimates = get_resource_estimates()

    print("Processing results...")
    data = process_results(estimates)

    print("Displaying results...")
    display_results(data)

    # Save results to a file
    with open(args.output, "w") as f:
        json.dump(estimates, f, indent=4)
    print(f"Results saved to {args.output}")
