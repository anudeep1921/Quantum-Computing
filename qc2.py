from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt

# Create a basic quantum circuit
qc = QuantumCircuit(2,2)
qc.h(0)  # Hadamard on qubit 0
qc.cx(0, 1)  # CNOT gate with qubit 0 as control and qubit 1 as target
qc.measure(0,0)
qc.measure(1,1)
# Visualize the original circuit
print("Original Circuit:")
print(qc.draw('mpl'))

# Now transpile the circuit for the Aer simulator backend
simulator = AerSimulator()
transpiled_qc = transpile(qc, simulator)

# Visualize the transpiled circuit
print("\nTranspiled Circuit:")
print(transpiled_qc.draw('mpl'))
result = simulator.run(transpiled_qc, shots=100000).result()

# Get the measurement results
counts = result.get_counts()
print("Measurement result:", counts)
plt.show()