from ase.build import molecule
from ase.visualize import view

water = molecule('H2O')
view(water)
from pyscf import gto, scf
import matplotlib.pyplot as plt

# Define H2 molecule using PySCF directly
mol = gto.Mole()
mol.atom = 'H 0 0 0; H 0 0 0.735'
mol.basis = 'sto-3g'
mol.unit = 'Angstrom'
mol.build()

mf = scf.RHF(mol)
mf.kernel()

# Get molecular orbital energies
mo_energies = mf.mo_energy

# Plot orbital energies
plt.figure(figsize=(6, 4))
for i, energy in enumerate(mo_energies):
    plt.hlines(energy, i - 0.4, i + 0.4, colors='blue')
plt.title("Molecular Orbital Energy Levels of H₂ (STO-3G)")
plt.ylabel("Energy (Hartree)")
plt.xlabel("Orbital index")
plt.grid(True)
plt.tight_layout()
plt.show()
