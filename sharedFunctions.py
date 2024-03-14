from qiskit_aer import AerSimulator
from qiskit.providers.fake_provider import ConfigurableFakeBackend
from qiskit import transpile
from math import pi


# ----------------------Circuit Components---------------------------
def initializeQReg(qc, reg, num):
    """
    Initializes a register using the binary string passed in to determine where to apply X gates
    :param qc: The quantum circuit being created
    :param reg: The register being initialized
    :param num: The string representation of the binary number
    :return: None
    """
    for i in range(len(num)):
        if num[i] == '1':
            qc.x(reg[len(num) - i - 1])


def CCP(qc, theta, A, B, T):
    """
    Multiple controlled phase shift
    :param qc: Quantum Circuit
    :param theta: phase shift amount
    :param A: Control 1
    :param B: Control 2
    :param T: Target
    :return: None
    """
    qc.cp(theta, B, T)
    qc.cx(A, B)
    qc.cp(-theta, B, T)
    qc.cx(A, B)
    qc.cp(theta, A, T)


def QFT(qc, reg):
    """
    Computes the quantum Fourier transform of reg, one qubit at
    a time.
    Apply one Hadamard gate to the nth qubit of the quantum register reg, and
    then apply repeated phase rotations with parameters being pi divided by
    increasing powers of two.
    :param qc: The quantum circuit being operated on
    :param reg: The register being changed to the phase basis
    :return: None
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
    :param qc: The quantum circuit being operated on
    :param reg: The register being changed out of the phase basis
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
def runIdeal(qc, answer, bits, printAll=False):
    """
    Runs the provided circuit with 1024 shots without noise
    :param qc: The pre-created quantum circuit to be run
    :param answer: The expected answer for the multiplication
    :param bits: how many bits there will be in the output
    :param printAll: Whether to print all the counts or just those for the answer
    :return: The results of the simulation
    """
    # Construct an ideal simulator (Use GPU line if Aer is installed with GPU support)
    aersim = AerSimulator()
    #aersim = AerSimulator(device="GPU")
    # Perform an ideal simulation
    result_ideal = aersim.run(qc).result()
    counts_ideal = result_ideal.get_counts(0)
    if printAll:
        print('Counts(ideal):', counts_ideal)
    key = bin(answer).lstrip('0b').zfill(bits)
    if key in counts_ideal:
        print(key, ": ", counts_ideal[key])
    else:
        print("key, ", key, ", not present in results")

    return result_ideal


def runNoisy(qc, answer, bits, printAll=False):
    """
    Runs the provided circuit with 1024 shots and noise
    :param qc: The pre-created quantum circuit to be run
    :param answer: The expected answer for the multiplication
    :param bits: how many bits there will be in the output
    :param printAll: Whether to print all the counts or just those for the answer
    :return: The results of the simulation
    """
    # Creating a generic backend for the current number of qubits being simulated
    backend = ConfigurableFakeBackend("testy", n_qubits=qc.num_qubits, version=1.0)

    # Perform noisy simulation (Use GPU line if Aer is installed with GPU support) (blocking_qubits=??)
    transpiled_circuit = transpile(qc, backend)
    result_noise = backend.run(transpiled_circuit).result()
    # result_noise = backend.run(transpiled_circuit, device="GPU", blocking_enable=True).result()
    counts_noise = result_noise.get_counts(0)
    if printAll:
        print('Counts(noise):', counts_noise)
    key = bin(answer).lstrip('0b').zfill(bits)
    if key in counts_noise:
        print(key, ": ", counts_noise[key])
    else:
        print("key, ", key, ", not present in results")
    return result_noise
