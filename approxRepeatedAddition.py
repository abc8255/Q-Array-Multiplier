from qiskit import QuantumRegister, QuantumCircuit, ClassicalRegister
from sharedFunctions import AQFT, invAQFT, runNoisy, runLessNoisy, runIdeal, initializeQReg, evolveAQFTState

import numpy as np
from math import pi, log2, ceil


def add(qc, reg_a, reg_b, factor, limit):
    """
    Add two quantum registers reg_a and reg_b, and store the result in
    reg_a.
    """
    # Add the two numbers by evolving the Fourier transform F(ψ(reg_a))>
    # to |F(ψ(reg_a+reg_b))>
    for i in range(0, len(reg_a)):
        evolveAQFTState(qc, reg_a, reg_b, len(reg_a) - 1 - i, factor, limit)


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


def createAOPBCircuit(multiplier, multiplicand, readable=False):
    """
    Creates the circuit for a repeated addition
    :param multiplier: A binary string of the multiplier
    :param multiplicand: A binary string of the multiplicand
    :return: a QC built using the two input numbers and their binary lengths
    """
    len1 = len(multiplicand)
    len2 = len(multiplier)

    # Limit calculated as ceil(log_2(size_of_product)+2)
    limit = ceil(log2(len1 + len2) + 2)

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

    if readable: qc.barrier(label="Initialized + Start QFT")

    AQFT(qc, accumulator, limit)

    if readable: qc.barrier(label=("End QFT"))

    multiplier_str = int(multiplier, 2)
    # Perform repeated addition until the multiplier
    # is zero
    while multiplier_str != 0:
        if readable: qc.barrier(label="Add")
        add(qc, accumulator, qrMultiplicand, 1, limit)
        if readable: qc.barrier(label="begin decrement")
        # Compute the Fourier transform of multiplier
        AQFT(qc, qrMultiplier, limit)

        sub1(qc, qrMultiplier)

        # Compute the inverse Fourier transform of multiplier
        invAQFT(qc, qrMultiplier, limit)


        # measure current multiplier state
        for i in range(len(qrMultiplier)):
            qc.measure(qrMultiplier[i], cl[i])
        if readable: qc.barrier(label="End Decrement")
        multiplier_str += -1

    # Compute the inverse Fourier transform of accumulator
    if readable: qc.barrier(label="Begin IAQFT")
    invAQFT(qc, accumulator, limit)
    if readable: qc.barrier(label="End IAQFT")

    qc.measure(accumulator, cl)

    # add(qc, accumulator, qrMultiplicand, 1, limit)
    return qc


def squareAOPBMultDepth(num):
    """
    Generates the circuit for a square multiplication and returns the resulting depth

    :param num: The number being used as both the multiplier and multiplicand
    :return: The depth of the generated circuit
    """
    qc = createAOPBCircuit(num, num, readable=True)

    return qc.decompose().decompose().decompose().depth()


def identityAOPBMultDepth(num):
    """
    Generates the circuit for a square multiplication and returns the resulting depth

    :param num: The number being used as the multiplicand
    :return: The depth of the generated circuit
    """
    qc = createAOPBCircuit(num, "1", readable=True)

    return qc.decompose().decompose().decompose().depth()


def getDepths():
    """
    Tests a hardcoded sample of input sizes both for identity multiplication and square multiplication. Prints
    results to the console
    :return: N/A
    """
    testArray = {"1": "1", "2": "11", "3": "111", "4": "1111", "5": "11111", "6": "111111", "7": "1111111",
                 "8": "11111111", "9": "111111111", "10": "1111111111",
                 "11": "11111111111", "12": "111111111111"
                 }

    print("____________________________________")
    for num in testArray:
        print("Depth for an input of size {}".format(num))
        # print("Limit for this input size {}".format(squareLimit))
        depth = identityAOPBMultDepth(testArray[num])
        print("identity depth: {}".format(depth))
        print("_____________")
        depth = squareAOPBMultDepth(testArray[num])
        print("square depth: {}".format(depth))
        print("____________________________________")


def main():
    # getDepths()
    # Test a sample input (3x3)

    sample = "1111"
    print("b'", sample, "' x b'", sample, "'")
    # print("b'", sample, "' x b'", "1", "'")
    value = (int(sample, 2)) ** 2
    # value = int(sample, 2)
    qc = createAOPBCircuit(sample, sample, readable=True)
    qc.draw(output="mpl", style="iqp", filename="tester2.png", scale=1, fold=200)
    # print("depth: ", qc.decompose().decompose().decompose().decompose().depth())
    # print("---Ideal, Noisy, Less Noisy---")
    # # runIdeal(qc, value, len(sample) * 2)
    # runIdeal(qc, value, len(sample)+1)
    # runNoisy(qc, value, len(sample)+1)
    # runLessNoisy(qc, value, len(sample) * 2)


if __name__ == "__main__":
    main()
