#Grover’s Algorithm AES Resource Estimation

This repository contains code and scripts for estimating the quantum resources required to apply Grover’s algorithm to AES encryption. Below is a description of the key files in the repository.

##File Descriptions

```src/g.qs```

This is the main Q# program responsible for performing the resource estimation. It is based on Microsoft’s implementation of Grover’s algorithm, modified to include an estimation for AES encryption.
	•	AES Resource Numbers:
The AES-related values used in this program were derived using scaling.py, based on the paper by Jang et al. These values cover AES-128, AES-192, and AES-256 encryption and have been scaled down to smaller qubit sizes (e.g., 12 and 24 qubits) for testing.
	•	Note: The scaled values can be adjusted directly in the program.

```scaling.py```

This Python script is used to generate scaled values for AES resource estimates. It determines the relationship (linear, polynomial, or exponential) and applies scaling to obtain approximate resource requirements for different qubit sizes.
	•	Purpose:
To provide a rough estimation for AES encryption with reduced qubit counts, enabling resource comparisons at smaller scales.
	•	Limitations:
The scaling is not exact but provides a reasonable approximation based on the methodology described in Jang et al.

```qsharp.json```

This file is needed for Python to be able to run the Q# (it's an empty file).

```run_grover.py```

This script was an attempt to run the resource estimation program via Python. Unfortunately, it did not work.

Usage Instructions
	1.	Run the Q# program:
The main functionality is implemented in g.qs. Use the VSCode extension and "Estimate".
	2.	Scale AES values:
If you need to adjust AES values for different qubit sizes, modify and run scaling.py.
	3.	Python integration (doesn’t work):
Maybe one day run_grover.py will work (it won’t)

```run_grover_12.ipynb``` and ```run_grover_24.ipynb```
These contain the actual code used for estimating that provided the numbers used in the paper. You can run this to get the numbers.


