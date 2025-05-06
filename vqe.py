from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Statevector
from scipy.optimize import minimize
import numpy as np

# Define the Hamiltonian H = Z₀Z₁ + X₀
H = SparsePauliOp.from_list([
    ("ZZ", 1.0),
    ("XI", 1.0)
])

# Ansatz: Parametrized Ry rotations and CX entanglement
def ansatz(params):
    qc = QuantumCircuit(2)
    qc.ry(params[0], 0)
    qc.ry(params[1], 1)
    qc.cx(0, 1)
    return qc

# Objective: Compute ⟨ψ(θ)|H|ψ(θ)⟩
def expectation(params):
    qc = ansatz(params)
    state = Statevector.from_instruction(qc)
    return np.real(state.expectation_value(H))

# Optimize parameters to minimize energy
initial_params = [0.1, 0.1]
result = minimize(expectation, initial_params, method='COBYLA')

# Print optimal energy and parameters
print("Optimal parameters:", result.x)
print("Estimated ground state energy:", result.fun)
