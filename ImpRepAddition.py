from qiskit import QuantumRegister, QuantumCircuit, ClassicalRegister
from math import pi

from sharedFunctions import QFT, invQFT, runIdeal, runNoisy, evolveQFTState


def add(qc, reg_a, reg_b, factor):
    """
    Add two quantum registers reg_a and reg_b, and store the result in
    reg_a.
    :param qc: The quantum circuit being operated on.
    :param reg_a: The first register for the addition, which will contain the sum afterward.
    :param reg_b: The second register for the addition.
    :param factor: The current factor to multiply the phase shift by
    :return: None
    """
    # Add the two numbers by evolving the Fourier transform F(ψ(reg_a))>
    # to |F(ψ(reg_a+reg_b))>
    for i in range(0, len(reg_a)):
        evolveQFTState(qc, reg_a, reg_b, len(reg_a) - 1 - i, factor)


def sub1(qc, reg_a):
    """
    Subtracts 1 from a given register that is currently in the phase domain.
    :param qc: The quantum circuit being operated on.
    :param reg_a: The register to have 1 subtracted from it.
    :return: None
    """
    for i in range(0, len(reg_a)):
        n = len(reg_a) - 1 - i
        for j in range(0, n + 1):
            if (n - j) > 0:
                pass
            else:
                qc.p(-1 * pi / float(2 ** j), reg_a[n])


def createIOPBCircuit(multiplier, multiplicand):
    """
    Generates the improved repeated addition circuit using the provided multiplier and multiplicand bit strings
    :param multiplier: A binary string of the multiplier ie) "010"
    :param multiplicand: A binary string of the multiplicand ie) "110"
    :return: a QC built using the two input numbers and their binary lengths
    """
    len1 = len(multiplicand)
    len2 = len(multiplier)

    # Make sure multiplier is the smaller input
    if len2 > len1:
        multiplier, multiplicand = multiplicand, multiplier
        len2, len1 = len1, len2

    qrMultiplicand = QuantumRegister(len1)
    qrMultiplier = QuantumRegister(len2)
    accumulator = QuantumRegister(len1 + len2)
    cl = ClassicalRegister(len1 + len2)

    qc = QuantumCircuit(accumulator, qrMultiplier, qrMultiplicand, cl, name="qc")

    for i in range(len1):
        if multiplicand[i] == '1':
            qc.x(qrMultiplicand[len1 - i - 1])

    for i in range(len2):
        if multiplier[i] == '1':
            qc.x(qrMultiplier[len2 - i - 1])

    QFT(qc, accumulator)

    multiplier_str = int(multiplier, 2)
    # Perform repeated addition until the multiplier
    # is zero
    while multiplier_str != 0:

        add(qc, accumulator, qrMultiplicand, 1)

        # Compute the Fourier transform of multiplier
        QFT(qc, qrMultiplier)

        sub1(qc, qrMultiplier)

        # Compute the inverse Fourier transform of multiplier
        invQFT(qc, qrMultiplier)

        # measure current multiplier state
        for i in range(len(qrMultiplier)):
            qc.measure(qrMultiplier[i], cl[i])
        multiplier_str += -1

    # Compute the inverse Fourier transform of accumulator
    invQFT(qc, accumulator)

    qc.measure(accumulator, cl)
    return qc


def squareMultDepth(num):
    """
    Generates the circuit for a square multiplication and returns the resulting depth

    :param num: The number being used as both the multiplier and multiplicand
    :return: The depth of the generated circuit
    """
    qc = createIOPBCircuit(num, num)

    return qc.decompose().decompose().decompose().depth()


def identityMultDepth(num):
    """
    Generates the circuit for a square multiplication and returns the resulting depth

    :param num: The number being used as the multiplicand
    :return: The depth of the generated circuit
    """
    qc = createIOPBCircuit(num, "1")

    return qc.decompose().decompose().decompose().depth()


def getDepths():
    """
    Tests a hardcoded sample of input sizes both for identity multiplication and square multiplication. Prints
    results to the console

    :return: N/A
    """
    testArray = {"1": "1", "2": "11", "3": "111", "4": "1111", "5": "11111", "6": "111111", "7": "1111111",
                 "8": "11111111", "9": "111111111", "10": "1111111111",
                 "11": "11111111111", "12": "111111111111"}

    for num in testArray:
        print("Depth for a identity input of size {}".format(num))
        depth = identityMultDepth(testArray[num])
        print("{}".format(depth))
        print("Depth for a square input of size {}".format(num))
        depth = squareMultDepth(testArray[num])
        print("{}".format(depth))


def main():
    # Get all depths defined in the following function
    # getDepths()


    # Test a sample input (3x3)
    print("b'111' x b'111'")
    sample = "111"
    circ = createIOPBCircuit(sample, sample)
    value = (int(sample, 2)) ** 2
    runIdeal(circ, value, len(sample)*2)
    runNoisy(circ, value, len(sample)*2)


if __name__ == "__main__":
    main()
