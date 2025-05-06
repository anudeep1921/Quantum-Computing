from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.units import DistanceUnit

from qiskit_nature.second_q.mappers import ParityMapper
from qiskit_nature.second_q.circuit.library import HartreeFock, UCCSD
from qiskit_nature.second_q.algorithms import GroundStateEigensolver

from qiskit_algorithms import VQE
from qiskit.algorithms.optimizers import SLSQP
from qiskit import Aer
from qiskit.utils import QuantumInstance
from qiskit.opflow import StateFn, PauliExpectation

# Step 1: Define the molecule
driver = PySCFDriver(atom="H 0 0 0; H 0 0 0.735", 
                     basis="sto3g", 
                     unit=DistanceUnit.ANGSTROM)
problem = driver.run()

# Step 2: Map to qubit Hamiltonian
mapper = ParityMapper()
qubit_converter = mapper

# Step 3: Build ansatz (UCCSD + HartreeFock)
num_particles = problem.num_particles
num_spatial_orbitals = problem.num_spatial_orbitals
initial_state = HartreeFock(num_spatial_orbitals, num_particles, qubit_converter)
ansatz = UCCSD(num_spatial_orbitals, num_particles, qubit_converter, initial_state=initial_state)

# Step 4: Set up VQE
backend = Aer.get_backend('statevector_simulator')
quantum_instance = QuantumInstance(backend)

optimizer = SLSQP()
vqe = VQE(ansatz=ansatz, optimizer=optimizer, quantum_instance=quantum_instance)

# Step 5: Solve ground state
solver = GroundStateEigensolver(mapper, vqe)
result = solver.solve(problem)

# Step 6: Display result
print(f"\nGround state energy: {result.total_energies[0]:.6f} Ha")
