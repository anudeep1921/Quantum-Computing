from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import ParityMapper
from qiskit.primitives import Estimator
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import SLSQP
from qiskit_nature.second_q.circuit.library import HartreeFock, UCCSD
from qiskit_nature.second_q.algorithms import GroundStateEigensolver
from qiskit_nature.second_q.algorithms.excited_states_solvers import QEOM

# 1. Define the molecule and driver
driver = PySCFDriver(
    atom="H 0 0 0; H 0 0 0.735",
    unit=DistanceUnit.ANGSTROM,
    basis="sto3g",
    charge=0,
    spin=0,
)
problem = driver.run()

# 2. Define mapper
mapper = ParityMapper()

# 3. Setup Hartree-Fock and UCCSD ansatz
num_particles = problem.num_particles
num_spatial_orbitals = problem.num_spatial_orbitals

initial_state = HartreeFock(
    num_spatial_orbitals=num_spatial_orbitals,
    num_particles=num_particles,
    qubit_mapper=mapper,
)

ansatz = UCCSD(
    num_spatial_orbitals=num_spatial_orbitals,
    num_particles=num_particles,
    qubit_mapper=mapper,
    initial_state=initial_state,
)

# 4. Set up VQE
estimator = Estimator()
optimizer = SLSQP()
vqe_solver = VQE(estimator=estimator, ansatz=ansatz, optimizer=optimizer)
vqe_solver.initial_point = [0.0] * ansatz.num_parameters

# 5. Create ground-state solver
gse_solver = GroundStateEigensolver(mapper, vqe_solver)

# 6. QEOM Excited state solver
qeom_solver = QEOM(gse_solver, estimator)

# 7. Solve for excited states
excited_result = qeom_solver.solve(problem)

# 8. Print energy levels
print("\nElectronic Energy Levels (Hartree):")
energies = excited_result.total_energies
print(f"Ground state: {energies[0]:.6f} Ha")
for i, energy in enumerate(energies[1:], start=1):
    delta_e = energy - energies[0]
    print(f"Excited state {i}: {energy:.6f} Ha (ΔE = {delta_e:.6f})")
import matplotlib.pyplot as plt

energies = excited_result.total_energies
ground_energy = energies[0]

plt.figure(figsize=(6, 4))
for i, energy in enumerate(energies):
    label = "Ground state" if i == 0 else f"Excited state {i}"
    plt.hlines(energy, xmin=0.3, xmax=0.7, colors='blue' if i == 0 else 'orange')
    plt.text(0.75, energy, f"{label}\n{energy:.4f} Ha", va='center')

plt.xlabel("States")
plt.ylabel("Energy (Ha)")
plt.title("Electronic Energy Levels of H₂")
plt.yticks([])
plt.xticks([])
plt.grid(False)
plt.tight_layout()
plt.show()
