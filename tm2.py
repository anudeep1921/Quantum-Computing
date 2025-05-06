from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp
import numpy as np
import matplotlib.pyplot as plt

# Time parameter
t = 1.0

# Step 1: Create 2-qubit circuit for H = Z₁Z₂ + X₁
qc = QuantumCircuit(2)

# Apply e^{-i Z₁ Z₂ t} using CX - RZ - CX trick
qc.cx(0, 1)
qc.rz(2 * t, 1)  # 2t in RZ gives correct phase for Z₁Z₂
qc.cx(0, 1)

# Apply e^{-i X₁ t} using RX gate on qubit 0
qc.rx(2 * t, 0)

# Step 2: Simulate to get statevector
statevec = Statevector.from_instruction(qc)

# Step 3: Show statevector
print("Final Statevector:")
print(statevec)

# Step 4: Calculate expectation value of Z ⊗ Z
observable = SparsePauliOp.from_list([("ZZ", 1.0)])
expectation = statevec.expectation_value(observable)
print("\nExpectation value of Z⊗Z:")
print(expectation)

# Step 5: Plot probabilities of each basis state
probs = np.abs(statevec.data) ** 2
labels = ['|00⟩', '|01⟩', '|10⟩', '|11⟩']
prob_dict = dict(zip(labels, probs))

plt.figure(figsize=(6, 4))
plt.bar(prob_dict.keys(), prob_dict.values(), color='skyblue')
plt.ylabel('Probability')
plt.title('Statevector Probabilities')
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.show()
