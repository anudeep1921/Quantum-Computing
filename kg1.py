from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
import time

# Function to simulate and measure time complexity
def simulate_circuit(qc, simulator, shots=1024):
    start_time = time.time()
    job = simulator.run(qc, shots=shots)
    result = job.result()
    counts = result.get_counts()
    elapsed = time.time() - start_time
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

# Main function to simulate and compare circuits for a list of qubits
def main(qubit_list):
    sim = AerSimulator(max_memory_mb=32768)  # defaults to automatic shot-based mode

    time_clifford_list = []
    time_non_clifford_list = []

    # First pass: collect timings
    for n in qubit_list:
        qc_c = create_clifford_circuit(n)
        qc_nc = create_non_clifford_circuit(n)
        _, t_c = simulate_circuit(qc_c, sim)
        _, t_nc = simulate_circuit(qc_nc, sim)
        time_clifford_list.append(t_c)
        time_non_clifford_list.append(t_nc)
        print(f"Qubits={n}: Clifford {t_c:.4f}s, Non-Clifford {t_nc:.4f}s")

    # Plot time complexity
    fig_time, ax = plt.subplots(figsize=(8,5))
    ax.plot(qubit_list, time_clifford_list, 'o-', label='Clifford')
    ax.plot(qubit_list, time_non_clifford_list, 'o-', label='Non-Clifford')
    ax.set_xlabel('Number of Qubits')
    ax.set_ylabel('Simulation Time (s)')
    ax.set_title('Clifford vs Non-Clifford Time Complexity')
    ax.legend()
    ax.grid(True)
    plt.show()

    # Example: show circuits and counts for the largest size
    n = qubit_list[-1]
    qc_c = create_clifford_circuit(n)
    qc_nc = create_non_clifford_circuit(n)
    counts_c, _ = simulate_circuit(qc_c, sim)
    counts_nc, _ = simulate_circuit(qc_nc, sim)

    fig, axs = plt.subplots(2, 2, figsize=(12,10))
    # Circuit diagrams
    axs[0,0].axis('off'); qc_c.draw('mpl', ax=axs[0,0]); axs[0,0].set_title(f'Clifford ({n} qubits)')
    axs[0,1].axis('off'); qc_nc.draw('mpl', ax=axs[0,1]); axs[0,1].set_title(f'Non-Clifford ({n} qubits)')
    # Histograms
    labels_c, vals_c = zip(*counts_c.items())
    labels_nc, vals_nc = zip(*counts_nc.items())
    x = range(len(labels_c))
    w = 0.35
    axs[1,0].bar(x, vals_c, w, label='Clifford')
    axs[1,0].bar([i+w for i in x], vals_nc, w, label='Non-Clifford')
    axs[1,0].set_xticks([i+w/2 for i in x]); axs[1,0].set_xticklabels(labels_c)
    axs[1,0].set_xlabel('Outcome'); axs[1,0].set_ylabel('Counts')
    axs[1,0].set_title('Measurement Results'); axs[1,0].legend()
    # Timing summary
    axs[1,1].axis('off')
    axs[1,1].text(0.5, 0.5,
        f"Clifford: {time_clifford_list[-1]:.4f}s\nNon-Clifford: {time_non_clifford_list[-1]:.4f}s",
        ha='center', va='center', fontsize=12, bbox=dict(facecolor='white', alpha=0.8))
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # adjust range as needed (e.g. 2→30)
    qubit_list = list(range(2, 31))
    main(qubit_list)
