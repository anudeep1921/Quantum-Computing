from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# Create a simple quantum circuit
qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

# Use AerSimulator
simulator = AerSimulator()

# Transpile the circuit for the simulator
compiled_circuit = transpile(qc, simulator)

# Run the simulation
result = simulator.run(compiled_circuit, shots=100000).result()

# Get the measurement results
counts = result.get_counts()
print("Measurement result:", counts)
