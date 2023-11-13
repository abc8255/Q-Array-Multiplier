from qiskit import QuantumRegister, QuantumCircuit, ClassicalRegister
from sharedFunctions import QFT, invQFT, runNoisy, runIdeal, initializeQReg, evolveQFTState


def add(reg_a, reg_b, circ, factor):
    """
    Add two quantum registers reg_a and reg_b, and store the result in
    reg_a.
    """
    n = len(reg_a) - 1

    # Compute the Fourier transform of register a
    QFT(circ, reg_a)

    # Add the two numbers by evolving the Fourier transform F(ψ(reg_a))>
    # to |F(ψ(reg_a+reg_b))>
    for i in range(0, n + 1):
        evolveQFTState(circ, reg_a, reg_b, n - i, factor)
    # Compute the inverse Fourier transform of register a
    invQFT(circ, reg_a)


def createOPBCircuit(multiplier, multiplicand):
    """
    Creates the circuit for a repeated addition
    :param multiplier: A binary string of the multiplier
    :param multiplicand: A binary string of the multiplicand
    :return: a QC built using the two input numbers and their binary lengths
    """
    len1 = len(multiplicand)
    len2 = len(multiplier)

    if len2 > len1:
        multiplier, multiplicand = multiplicand, multiplier
        len2, len1 = len1, len2

    qrMultiplicand = QuantumRegister(len1, name="Multiplicand")
    qrMultiplier = QuantumRegister(len2, name="Multiplier")
    accumulator = QuantumRegister(len1 + len2, name="accumulator")
    cl = ClassicalRegister(len1 + len2, name="classic")
    d = QuantumRegister(1)

    circ = QuantumCircuit(accumulator, qrMultiplier, qrMultiplicand, d, cl, name="qc")

    # ancillary qubit
    circ.x(d)

    # Store bit strings in quantum registers
    initializeQReg(circ, qrMultiplicand, multiplicand)
    initializeQReg(circ, qrMultiplier, multiplier)

    multiplier_str = int(multiplier, 2)

    # Perform repeated addition until the multiplier
    while multiplier_str != 0:
        add(accumulator, qrMultiplicand, circ, 1)
        add(qrMultiplier, d, circ, -1)
        for i in range(len(qrMultiplier)):
            circ.measure(qrMultiplier[i], cl[i])
        # result = execute(circ, backend=Aer.get_backend('qasm_simulator'), # Actual simulation is commented out to
        #  shots=2).result().get_counts(circ.name)                          # reduce run-time
        multiplier_str += -1

    circ.measure(accumulator, cl)

    return circ


def squareOPBMultDepth(num):
    """
    Generates the circuit for a square multiplication and returns the resulting depth

    :param num: The number being used as both the multiplier and multiplicand
    :return: The depth of the generated circuit
    """
    qc = createOPBCircuit(num, num)

    return qc.decompose().decompose().decompose().depth()


def identityOPBMultDepth(num):
    """
    Generates the circuit for a square multiplication and returns the resulting depth

    :param num: The number being used as the multiplicand
    :return: The depth of the generated circuit
    """
    qc = createOPBCircuit(num, "1")

    return qc.decompose().decompose().decompose().depth()


def getDepths():
    """
    Tests a hardcoded sample of input sizes both for identity multiplication and square multiplication. Prints
    results to the console
    :return: N/A
    """
    testArray = ["1", "11", "111", "1111", "11111", "111111", "1111111", "11111111", "111111111", "1111111111",
                 "11111111111", "111111111111"]

    for num in testArray:
        print("Depth for a identity input of {}".format(num))
        depth = identityOPBMultDepth(num)
        print("{}".format(depth))
        print("Depth for a square input of {}".format(num))
        depth = squareOPBMultDepth(num)
        print("{}".format(depth))


def main():
    # getDepths()
    # Test a sample input (3x3)
    print("b'11' x b'11'")
    circ = createOPBCircuit("11", "11")

    runIdeal(circ)
    runNoisy(circ)


if __name__ == "__main__":
    main()
