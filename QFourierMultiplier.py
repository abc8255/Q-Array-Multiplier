import qiskit.circuit.library
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
import numpy as np
from sharedFunctions import runNoisy, runIdeal, QFT, invQFT, initializeQReg, CCP

def createQFMCircuit(multiplier, multiplicand, readable=False):
    """
    Multiply two numbers using a weighted array structure
    :param multiplier: A binary string of the multiplier
    :param multiplicand: A binary string of the multiplicand
    :param readable: Whether to include barriers between stages (will increase circuit depth)
    :return: a QC built using the two input numbers and their binary lengths
    """
    # Take two numbers as user input in binary form
    len1 = len(multiplicand)
    len2 = len(multiplier)

    if (len1 >= 1) & (len2 >= 1) & (len1 == len2):
        qrMultiplicand = QuantumRegister(len1, name="Multiplicand")  # Multiplicand
        qrMultiplier = QuantumRegister(len2, name="Multiplier")  # Multiplier
        qProduct = QuantumRegister(len1 + len2, name="product")  # holds both the final multiplied result
        CarrySum = ClassicalRegister(len1 + len2)  # Classical register to hold the final measured values

        qc = QuantumCircuit(qrMultiplicand, qrMultiplier, qProduct, CarrySum, name="qc2")

        # Store bit strings in quantum registers
        initializeQReg(qc, qrMultiplicand, multiplicand)
        initializeQReg(qc, qrMultiplier, multiplier)

        if readable: qc.barrier(label="Initialized + Start QFM")

        QFM = qiskit.circuit.library.RGQFTMultiplier(len1, len1+len2, "QFM")
        qc.append(QFM, [qrMultiplicand[0], qrMultiplicand[1], qrMultiplier[0], qrMultiplier[1], qProduct[0], qProduct[1], qProduct[2], qProduct[3]])

        # # Compute the Fourier transform of accumulator
        # QFT(qc, qProduct)
        #
        # for i in range(0, len(qrMultiplicand)):
        #     if readable: qc.barrier(label=("Start of Row " + str(i)))
        #
        #     addMultRow(qc, qrMultiplicand, i, qrMultiplier, qProduct)
        #
        # if readable: qc.barrier(label="Done Looping")
        #
        # # Compute the inverse Fourier transform of accumulator
        # invQFT(qc, qProduct)

        qc.measure(qProduct, CarrySum)

        return qc


def squareQFMMultDepth(num):
    """
    Generates the circuit for a square multiplication and returns the resulting depth

    :param num: The number being used as both the multiplier and multiplicand
    :return: The depth of the generated circuit
    """
    qc = createQFMCircuit(num, num)

    return qc.decompose().decompose().decompose().depth()


# def identityQFMMultDepth(num):
#     """
#     Generates the circuit for an identity multiplication and returns the resulting depth
#
#     :param num: The number being used as the multiplicand
#     :return: The depth of the generated circuit
#     """
#     qc = createQFMCircuit(num, "1")
#
#     return qc.decompose().decompose().decompose().depth()


def getDepths():
    """
    Tests a hardcoded sample of input sizes both for identity multiplication and square multiplication. Prints
    results to the console

    :return: N/A
    """
    testArray = {"1": "1", "2": "11", "3": "111", "4": "1111", "5": "11111", "6": "111111", "7": "1111111",
                 "8": "11111111", "9": "111111111", "10": "1111111111",
                 "11": "11111111111", "12": "111111111111", "13": "1111111111111", "14": "11111111111111",
                 "15": "111111111111111", "16": "1111111111111111", "17": "11111111111111111",
                 "18": "111111111111111111", "19": "1111111111111111111", "20": "11111111111111111111"}
    print("____________________________________")
    for num in testArray:
        print("Depth for an input of size {}".format(num))
        # depth = identityQFMMultDepth(testArray[num])
        # print("identity: {}".format(depth))
        depth = squareQFMMultDepth(testArray[num])
        print("square: {}".format(depth))
        print("____________________________________")


def main():
    # getDepths()
    # Test a sample input (3x3)
    qc = createQFMCircuit("11", "11")

    qc.draw(output="mpl", style="iqp", filename="test1.png")
    runIdeal(qc.decompose().decompose().decompose().decompose())
    # runNoisy(qc)


if __name__ == "__main__":
    main()
