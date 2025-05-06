from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import ParityMapper
from qiskit.primitives import Estimator
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import SLSQP
from qiskit_nature.second_q.circuit.library import HartreeFock, UCCSD
from qiskit_nature.second_q.algorithms import GroundStateEigensolver

# For visualization
from ase import Atoms
from ase.visualize import view

# Define H2 molecule with positions in angstroms
h2_molecule = Atoms('H2', positions=[[0, 0, 0], [0, 0, 0.735]])
view(h2_molecule)  # This opens the GUI

# === Quantum Chemistry Calculation ===

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

# 5. Solve the ground state problem
solver = GroundStateEigensolver(mapper, vqe_solver)
result = solver.solve(problem)

# 6. Print result
print(f"Ground state energy: {result.total_energies[0]:.6f} Ha")
