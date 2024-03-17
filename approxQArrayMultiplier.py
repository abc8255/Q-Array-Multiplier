from qiskit import QuantumRegister, QuantumCircuit, ClassicalRegister
import numpy as np
from math import pi, log2, ceil
from sharedFunctions import runNoisy, runLessNoisy, runIdeal, initializeQReg, CCP


def addMultRow(qc, reg_a, s, reg_b, reg_p, limit):
    """
    Add a quantum register reg_b if reg_aVal is 1, and store the result in reg_p.
    :param qc:      quantum circuit that is being operated on.
    :param reg_a:   the smaller of the two inputs, the multiplicand.
    :param s:       the current index of register a.
    :param reg_b:   the larger of the two inputs, the multiplier.
    :param reg_p:   the qregister holding the resultant product.
    :param limit:   the minimum size that the phase shift can be
    """
    for b in range(0, len(reg_b)):
        for j in range(0, len(reg_b) - b):
            lam = np.pi / (2 ** (j + 1))
            if abs((j + 1)) <= limit:
                CCP(qc, lam, reg_a[s], reg_b[b], reg_p[b + j + s])
        for i in range(0, len(reg_p) - len(reg_b) - s):
            lam = np.pi / (2 ** (b + 2 + i))
            if abs((b + 2 + i)) <= limit:
                CCP(qc, lam, reg_a[s], reg_b[len(reg_b) - b - 1], reg_p[len(reg_b) + i + s])


def AQFT(qc, reg, limit):
    """
    Computes the approximate quantum Fourier transform of reg, one qubit at
    a time.
    :param qc:      quantum circuit that is being operated on.
    :param reg:     The quantum register for the AQFT to be applied to.
    :param limit:   The smallest acceptable phase shift to be performed.
    """
    for i in range(0, len(reg)):
        n = len(reg) - 1 - i
        qc.h(reg[n])
        for j in range(0, n):
            if abs((j + 1)) <= limit:
                qc.cp(pi / float(2 ** (j + 1)), reg[n - (j + 1)], reg[n])


def invAQFT(qc, reg, limit):
    """
    Performs the inverse quantum Fourier transform on a register reg.
    :param qc:      quantum circuit that is being operated on
    :param reg:     The quantum register for the AQFT to be applied to.
    :param limit:   The smallest acceptable phase shift to be performed.
    """
    for n in range(0, len(reg)):
        for j in range(0, n):
            if abs((n - j)) <= limit:
                qc.cp(-1 * pi / float(2 ** (n - j)), reg[j], reg[n])
        qc.h(reg[n])


def createAQAMCircuit(multiplier, multiplicand, limit, readable=False):
    """
    Multiply two numbers using a structure of the array multiplier, along with a phase limitation.
    :param multiplier: A binary string of the multiplier ie) "011"
    :param multiplicand: A binary string of the multiplicand ie) "001"
    :param limit: The smallest acceptable phase shift to be performed.
    :param readable: Whether to include barriers between stages (will increase circuit depth)
    :return: a QC built using the two input numbers and their binary lengths
    """
    # Take two numbers as user input in binary form
    len1 = len(multiplicand)
    len2 = len(multiplier)

    if (len1 >= 1) & (len2 >= 1):
        qrMultiplicand = QuantumRegister(len1, name="Multiplicand")  # Multiplicand
        qrMultiplier = QuantumRegister(len2, name="Multiplier")  # Multiplier
        qProduct = QuantumRegister(len1 + len2, name="product")  # holds both the final multiplied result
        CarrySum = ClassicalRegister(len1 + len2)  # Classical register to hold the final measured values

        qc = QuantumCircuit(qrMultiplicand, qrMultiplier, qProduct, CarrySum, name="qc2")

        # Store bit strings in quantum registers
        initializeQReg(qc, qrMultiplicand, multiplicand)
        initializeQReg(qc, qrMultiplier, multiplier)

        if readable: qc.barrier(label="Initialized + Start QFT")

        # Compute the Fourier transform of accumulator
        AQFT(qc, qProduct, limit)

        for i in range(0, len(qrMultiplicand)):
            if readable: qc.barrier(label=("Start of Row " + str(i)))

            addMultRow(qc, qrMultiplicand, i, qrMultiplier, qProduct, limit)

        if readable: qc.barrier(label="Done Looping")

        # Compute the inverse Fourier transform of accumulator
        invAQFT(qc, qProduct, limit)

        qc.measure(qProduct, CarrySum)

        return qc


def squareAQAMMultDepth(num, limit):
    """
    Generates the circuit for a square multiplication and returns the resulting depth

    :param num: The number being used as both the multiplier and multiplicand
    :param limit: the minimum size that the phase shift can be
    :return: The depth of the generated circuit
    """
    qc = createAQAMCircuit(num, num, limit)
    depth = qc.decompose().decompose().decompose().depth()

    del qc
    return depth


def identityAQAMMultDepth(num, limit):
    """
    Generates the circuit for an identity multiplication and returns the resulting depth

    :param num: The number being used as the multiplicand
    :param limit: the minimum size that the phase shift can be
    :return: The depth of the generated circuit
    """
    qc = createAQAMCircuit(num, "1", limit)
    depth = qc.decompose().decompose().decompose().depth()
    del qc
    return depth


def getDepths():
    """
    Tests a hardcoded sample of input sizes both for identity multiplication and square multiplication.
    Uses a limit of Log_2(n) for inputs of size n for approximate QFT operations Prints results to the console.

    :return: N/A+

    """
    testArray = {"1": "1", "2": "11", "3": "111", "4": "1111", "5": "11111", "6": "111111"
                 , "7": "1111111",
                 "8": "11111111", "9": "111111111", "10": "1111111111",
                 "11": "11111111111", "12": "111111111111"}# , "13": "1111111111111", "14": "11111111111111",
                 # "15": "111111111111111", "16": "1111111111111111", "17": "11111111111111111",
                 # "18": "111111111111111111", "19": "1111111111111111111", "20": "11111111111111111111"
                 #}
    print("____________________________________")
    for num in testArray:
        squareLimit = ceil(log2(len(testArray[num])*2) + 2)
        identityLimit = ceil(log2(len(testArray[num]) + 1) + 2)
        print("Depth for an input of size {}".format(num))
        print("Limit for this input size {}".format(squareLimit))
        depth = identityAQAMMultDepth(testArray[num], squareLimit)
        print("identity depth: {}".format(depth))
        print("_____________")
        depth = squareAQAMMultDepth(testArray[num], identityLimit)
        print("square depth: {}".format(depth))
        print("____________________________________")


def main():
    # Get all depths defined in the following function
    # getDepths()

    # #Test a sample input (3x3)
    sample = "1111"
    print("b'", sample, "' x b'", sample, "'")
    value = (int(sample, 2)) ** 2
    qc = createAQAMCircuit(sample, sample, ceil(log2(len(sample)*2)+2))
    #Draw Circuit
    #qc.draw(output="mpl", style="iqp")
    print("---Ideal, Noisy, Less Noisy---")
    runIdeal(qc, value, len(sample)*2)
    runNoisy(qc, value, len(sample)*2)
    runLessNoisy(qc, value, len(sample)*2)


if __name__ == "__main__":
    main()
