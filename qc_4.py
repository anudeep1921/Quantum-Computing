from qiskit import QuantumCircuit, transpile
from qiskit.transpiler import CouplingMap
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt

# Create a circuit that assumes full connectivity
qc = QuantumCircuit(3)
qc.cx(0, 2)  # This requires direct connection between qubit 0 and 2
qc.measure_all()

print("Original Circuit:")
print(qc.draw('mpl'))

# Define a restricted coupling map (linear qubit connectivity)
coupling = CouplingMap([[0, 1], [1, 2]])  # Only 0-1 and 1-2 connected
#simulator = AerSimulator()
# Transpile with the restricted connectivity
transpiled_qc = transpile(qc, coupling_map=coupling, optimization_level=0)
#transpiled_qc = transpile(qc, simulator, optimization_level=0)
print("\nTranspiled Circuit (with forced SWAPs):")
print(transpiled_qc.draw('mpl'))
plt.show()