from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator       # ← AerSimulator comes from qiskit_aer, not qiskit.providers
import matplotlib.pyplot as plt
import time

# Function to simulate and measure time complexity
def simulate_circuit(qc, simulator):
    start_time = time.time()
    job = simulator.run(qc, shots=1024)   # ← use .run(...) instead of execute(...)
    result = job.result()
    counts = result.get_counts()
    elapsed = time.time() - start_time
    print(f"Time taken to simulate the circuit: {elapsed:.6f} seconds")
    return counts, elapsed

# Build a Clifford Circuit
def create_clifford_circuit(num_qubits):
    qc = QuantumCircuit(num_qubits)
    qc.h(0)
    for i in range(num_qubits - 1):
        qc.cx(i, i + 1)
    qc.s(1)
    qc.measure_all()
    return qc

# Build a Non-Clifford Circuit (adds a T-gate)
def create_non_clifford_circuit(num_qubits):
    qc = QuantumCircuit(num_qubits)
    qc.h(0)
    for i in range(num_qubits - 1):
        qc.cx(i, i + 1)
    qc.s(1)
    qc.t(1)
    qc.measure_all()
    return qc

# Main: compare Clifford vs Non-Clifford
def main(num_qubits):
    qc_c = create_clifford_circuit(num_qubits)
    qc_nc = create_non_clifford_circuit(num_qubits)

    print("Clifford Circuit:\n", qc_c)
    print("\nNon-Clifford Circuit:\n", qc_nc)

    # Instantiate the Aer simulator with the 'qasm' method:
    sim = AerSimulator()      

    counts_c, t_c = simulate_circuit(qc_c, sim)
    counts_nc, t_nc = simulate_circuit(qc_nc, sim)

    print("\nClifford counts:", counts_c)
    print("Non-Clifford counts:", counts_nc)

    # Plot circuits and results
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))

    # Circuit diagrams
    axs[0, 0].axis('off')
    qc_c.draw('mpl', ax=axs[0, 0])
    axs[0, 0].set_title(f"Clifford ({num_qubits} qubits)")

    axs[0, 1].axis('off')
    qc_nc.draw('mpl', ax=axs[0, 1])
    axs[0, 1].set_title(f"Non-Clifford ({num_qubits} qubits)")

    # Histograms
    labels_c, vals_c = zip(*counts_c.items())
    labels_nc, vals_nc = zip(*counts_nc.items())
    x = range(len(labels_c))
    w = 0.35

    axs[1, 0].bar(x, vals_c, w, label='Clifford')
    axs[1, 0].bar([i + w for i in x], vals_nc, w, label='Non-Clifford')
    axs[1, 0].set_xticks([i + w/2 for i in x])
    axs[1, 0].set_xticklabels(labels_c)
    axs[1, 0].set_xlabel('Outcome')
    axs[1, 0].set_ylabel('Counts')
    axs[1, 0].set_title('Measurement Results')
    axs[1, 0].legend()

    # Timing info
    axs[1, 1].axis('off')
    axs[1, 1].text(
        0.5, 0.5,
        f"Clifford time: {t_c:.6f}s\nNon-Clifford time: {t_nc:.6f}s",
        ha='center', va='center', fontsize=12,
        bbox=dict(facecolor='white', alpha=0.8)
    )

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main(num_qubits=6)
