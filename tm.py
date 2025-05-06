from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np
import matplotlib.pyplot as mp

# Trotterization function
def apply_trotter_step(qc, t, N):
    dt = t / N
    for _ in range(N):
        qc.rz(-2 * dt, 0)  # Simulate exp(-i * Z * dt)
        qc.rx(-2 * dt, 1)  # Simulate exp(-i * X * dt)

# Create a quantum circuit with two qubits
qc = QuantumCircuit(2)

# Apply Trotter steps
apply_trotter_step(qc, t=1, N=10)

# Visualize the circuit
qc.draw('mpl')  # Will show circuit if running in notebook; can skip or use .draw('text') in terminal

# Simulate using Statevector
statevector = Statevector.from_instruction(qc)

# Print the final statevector
print(statevector)
