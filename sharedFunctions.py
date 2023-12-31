from qiskit_aer import AerSimulator
from qiskit.providers.fake_provider import FakeManilaV2
from math import pi


# ----------------------Circuit Components---------------------------
def initializeQReg(qc, reg, num):
    """
    Initializes a register using the binary string passed in to determine where to apply X gates
    :param qc: The quantum circuit being created
    :param reg: The register being initialized
    :param num: The string representation of the binary number
    :return: N/A
    """
    for i in range(len(num)):
        if num[i] == '1':
            qc.x(reg[len(num) - i - 1])


def QFT(qc, reg):
    """
    Computes the quantum Fourier transform of reg, one qubit at
    a time.
    Apply one Hadamard gate to the nth qubit of the quantum register reg, and
    then apply repeated phase rotations with parameters being pi divided by
    increasing powers of two.
    """
    for i in range(0, len(reg)):
        n = len(reg) - 1 - i

        qc.h(reg[n])
        for j in range(0, n):
            qc.cp(pi / float(2 ** (j + 1)), reg[n - (j + 1)], reg[n])


def invQFT(qc, reg):
    """
    Performs the inverse quantum Fourier transform on a register reg.
    Apply repeated phase rotations with parameters being pi divided by
    decreasing powers of two, and then apply a Hadamard gate to the nth qubit
    of the register reg.
    """
    for n in range(0, len(reg)):
        for j in range(0, n):
            qc.cp(-1 * pi / float(2 ** (n - j)), reg[j], reg[n])
        qc.h(reg[n])


def evolveQFTState(qc, reg_a, reg_b, n, factor):
    """
    Evolves the state |F(ψ(reg_a))> to |F(ψ(reg_a+reg_b))> using the quantum
    Fourier transform conditioned on the qubits of the reg_b.
    Apply repeated phase rotations with parameters being pi divided by
    increasing powers of two.
    """
    len_b = len(reg_b)
    for i in range(0, n + 1):
        if (n - i) > len_b - 1:
            pass
        else:
            qc.cp(factor * pi / float(2 ** i), reg_b[n - i], reg_a[n])


# ----------------------Simulator Code---------------------------
def runIdeal(qc):
    """
    Runs the provided circuit with 1024 shots without noise
    :param qc: The pre-created quantum circuit to be run
    :return: The results of the simulation
    """
    # Construct an ideal simulator
    aersim = AerSimulator()
    # Perform an ideal simulation
    result_ideal = aersim.run(qc).result()
    counts_ideal = result_ideal.get_counts(0)
    print('Counts(ideal):', counts_ideal)

    return result_ideal


def runNoisy(qc):
    """
    Runs the provided circuit with 1024 shots with noise
    :param qc: The pre-created quantum circuit to be run
    :return: The results of the simulation
    """
    backend = FakeManilaV2()
    aersim_backend = AerSimulator.from_backend(backend)

    # Perform noisy simulation
    result_noise = aersim_backend.run(qc).result()
    counts_noise = result_noise.get_counts(0)

    print('Counts(noise):', counts_noise)
    return result_noise
