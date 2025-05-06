from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt

# Create a simple quantum circuit
qc = QuantumCircuit(3)
qc.h(0)  # Apply Hadamard gate to qubit 0
qc.cx(0, 1)  # Apply CNOT gate between qubit 0 and qubit 1
qc.cx(1, 2)  # Apply CNOT gate between qubit 1 and qubit 2

# Visualize the original circuit
print("Original Circuit:")
print(qc.draw('mpl'))

# Transpile the circuit for the AerSimulator backend (simulate a real device)
simulator = AerSimulator()
transpiled_qc = transpile(qc, simulator,optimization_level=0)

# Visualize the transpiled circuit
print("\nTranspiled Circuit:")
print(transpiled_qc.draw('mpl'))
plt.show()