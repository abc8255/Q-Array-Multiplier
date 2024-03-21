from qiskit import QuantumRegister, QuantumCircuit, ClassicalRegister
import numpy as np
import approxQArrayMultiplier as AQAM
import ImpRepAddition as IOPB
import QArrayMultiplier as QAM
import RepeatedAddition as OPB
import QFourierMultiplier as QFM
from sharedFunctions import runIdeal, runNoisy
from math import ceil, log2


def OPBTest(maxNum, timesToTest):
    """
    Runs both the square and identity OPB circuits up to the max input length, repeating each design a number of times
    defined when called.

    :param maxNum: The highest size input to run the test up to
    :param timesToTest: The number of times to repeat each generated circuit
    :return: None
    """
    # Testing Square case
    num = ""
    for i in range(maxNum):
        num = num + "1"
        value = (int(num, 2)) ** 2
        print("Creating a square OPB Circuit of size ", num)
        qc = OPB.createOPBCircuit(num, num)
        print("depth :", qc.decompose().decompose().decompose().depth())
        # Commented out Ideal code because all circuits work in an ideal system
        # print("-------Ideal-------")
        # for i in range(timesToTest):
        #     runIdeal(qc, value, len(num)*2)
        print("-------Noisy-------")
        for i in range(timesToTest):
            runNoisy(qc, value, len(num)*2)
        del qc
        print("---------", i+1)
    num = ""
    print("-----------------------", num)
    # Testing Identity case
    for i in range(maxNum):
        num = num + "1"
        value = int(num, 2)
        print("Creating an identity OPB Circuit of size ", num)
        qc = OPB.createOPBCircuit(num, "1")
        print("depth :", qc.decompose().decompose().decompose().depth())
        # Commented out Ideal code because all circuits work in an ideal system
        # print("-------Ideal-------")
        # for i in range(timesToTest):
        #     runIdeal(qc, value, len(num) + 1)
        print("-------Noisy-------")
        for i in range(timesToTest):
            runNoisy(qc, value, len(num) + 1)
        del qc
        print("---------", i+1)
    print("______________END_OF_OPB_______________", num)


def IOPBTest(maxNum, timesToTest):
    """
    Runs both the square and identity IOPB circuits up to the max input length, repeating each design a number of times
    defined when called.

    :param maxNum: The highest size input to run the test up to
    :param timesToTest: The number of times to repeat each generated circuit
    :return: None
    """
    # Testing Square case
    num = ""
    for i in range(maxNum):
        num = num + "1"
        value = (int(num, 2)) ** 2
        print("i: ", i, "  -- Value: ", value, "  -- num: ", num)

        print("Creating a square IOPB Circuit of size ", num)
        qc = IOPB.createIOPBCircuit(num, num)
        print("depth :", qc.decompose().decompose().decompose().depth())
        # Commented out Ideal code because all circuits work in an ideal system
        # print("-------Ideal-------")
        # for i in range(timesToTest):
        #     runIdeal(qc, value, len(num) * 2)
        print("-------Noisy-------")
        for i in range(timesToTest):
            runNoisy(qc, value, len(num) * 2)
        del qc
        print("---------", i+1)
    num = ""
    print("-----------------------", num)
    # Testing Identity case
    for i in range(maxNum):
        num = num + "1"
        value = int(num, 2)
        print("i: ", i, "  -- Value: ", value, "  -- num: ", num)
        print("Creating an identity IOPB Circuit of size ", num)
        qc = IOPB.createIOPBCircuit(num, "1")
        print("depth :", qc.decompose().decompose().decompose().depth())
        # Commented out Ideal code because all circuits work in an ideal system
        # print("-------Ideal-------")
        # for i in range(timesToTest):
        #     runIdeal(qc, value, len(num) + 1)
        print("-------Noisy-------")
        for i in range(timesToTest):
            runNoisy(qc, value, len(num) + 1)
        del qc
        print("---------", i+1)
    print("______________END_OF_IOPB_______________", num)


def QFMTest(maxNum, timesToTest):
    """
    Runs both the square and identity QFM circuits up to the max input length, repeating each design a number of times
    defined when called.

    :param maxNum: The highest size input to run the test up to
    :param timesToTest: The number of times to repeat each generated circuit
    :return: None
    """
    # Testing Square case
    num = ""
    for i in range(maxNum):
        num = num + "1"
        value = (int(num, 2)) ** 2
        print("Creating a square QFM Circuit of size ", num)
        qc = QFM.createQFMCircuit(num, num)
        print("depth :", qc.decompose().decompose().decompose().depth())
        # Commented out Ideal code because all circuits work in an ideal system
        # print("-------Ideal-------")
        # for i in range(timesToTest):
        #     runIdeal(qc.decompose().decompose().decompose().decompose(), value, len(num)*2)
        print("-------Noisy-------")
        for i in range(timesToTest):
            runNoisy(qc.decompose().decompose().decompose().decompose(), value, len(num)*2)
        del qc
        print("---------", i+1)
    print("______________END_OF_QFM_______________")


def QAMTest(maxNum, timesToTest):
    """
    Runs both the square and identity QAM circuits up to the max input length, repeating each design a number of times
    defined when called.

    :param maxNum: The highest size input to run the test up to
    :param timesToTest: The number of times to repeat each generated circuit
    :return: None
    """
    # Testing Square case
    num = ""
    for i in range(maxNum):
        num = num + "1"
        value = (int(num, 2)) ** 2
        print("Creating a square QAM Circuit of size ", num)
        qc = QAM.createQAMCircuit(num, num)
        print("depth :", qc.decompose().decompose().decompose().depth())
        # Commented out Ideal code because all circuits work in an ideal system
        # print("-------Ideal-------")
        # for i in range(timesToTest):
        #     runIdeal(qc, value, len(num) * 2)
        print("-------Noisy-------")
        for i in range(timesToTest):
            runNoisy(qc, value, len(num) * 2)
        del qc
        print("---------", i+1)
    num = ""
    print("-----------------------", num)
    # Testing Identity case
    for i in range(maxNum):
        num = num + "1"
        value = int(num, 2)
        print("Creating an identity QAM Circuit of size ", num)
        qc = QAM.createQAMCircuit(num, "1")
        print("depth :", qc.decompose().decompose().decompose().depth())
        # Commented out Ideal code because all circuits work in an ideal system
        # print("-------Ideal-------")
        # for i in range(timesToTest):
        #     runIdeal(qc, value, len(num) + 1)
        print("-------Noisy-------")
        for i in range(timesToTest):
            runNoisy(qc, value, len(num) + 1)
        del qc
        print("---------", i+1)
    print("______________END_OF_QAM_______________")


def AQAMTest(maxNum, timesToTest):
    """
    Runs both the square and identity AQAM circuits up to the max input length, repeating each design a number of times
    defined when called.

    :param maxNum: The highest size input to run the test up to
    :param timesToTest: The number of times to repeat each generated circuit
    :return: None
    """
    # Testing Square case
    num = ""
    for i in range(1, maxNum+1):
        num = num + "1"
        value = (int(num, 2)) ** 2
        limit = ceil(log2(i*2) + 2)
        print("Creating a square AQAM Circuit of size ", num)
        qc = AQAM.createAQAMCircuit(num, num, limit)
        print("depth :", qc.decompose().decompose().decompose().depth())
        # This one isn't 100% accurate when ideal so still run
        print("-------Ideal-------")
        for i in range(timesToTest):
            runIdeal(qc, value, len(num) * 2)
        print("-------Noisy-------")
        for i in range(timesToTest):
            runNoisy(qc, value, len(num) * 2)
        del qc
        print("---------", i)
    num = ""
    print("-----------------------", num)
    # Testing Identity case
    for i in range(1, maxNum+1):
        num = num + "1"
        value = int(num, 2)
        limit = ceil(log2(i+1) + 2)
        print("Creating an identity AQAM Circuit of size ", num)
        qc = AQAM.createAQAMCircuit(num, "1", limit)
        print("depth :", qc.decompose().decompose().decompose().depth())
        # This one isn't 100% accurate when ideal so still run
        print("-------Ideal-------")
        for i in range(timesToTest):
            runIdeal(qc, value, len(num)+1)
        print("-------Noisy-------")
        for i in range(timesToTest):
            runNoisy(qc, value, len(num)+1)
        del qc
        print("---------", i)
    print("______________END_OF_AQAM_______________")


def ScalingAllTests(inputSize):
    """
    Runs all algorithms, up to a given input size getting the depth for each.

    :param inputSize: The size input to run the test up to
    :return: None
    """
    # Generate inputs to test all the possible values
    testInputs = []
    bigInput = "1" * inputSize
    for i in range(inputSize):
        currNum = "1" * (i+1)
        testInputs.append(currNum)
    print("All 8 bit inputs with values changed ie) '00000001', '00000011'...")
    for sample in testInputs:
        sample = sample.zfill(inputSize)
        print("input size of: ", sample, " operation: ", len(sample), " x ", len(bigInput))
        # OPB
        qc = OPB.createOPBCircuit(sample, bigInput)
        print(" OPB depth:", qc.decompose().decompose().decompose().depth())
        del qc

        # IOPB
        qc = IOPB.createIOPBCircuit(sample, bigInput)
        print("IOPB depth:", qc.decompose().decompose().decompose().depth())
        del qc

        # QFM
        qc = QFM.createQFMCircuit(bigInput, sample)
        print(" QFM depth:", qc.decompose().decompose().decompose().decompose().decompose().depth())
        del qc

        # QAM
        qc = QAM.createQAMCircuit(sample, bigInput)
        print(" QAM depth:", qc.decompose().decompose().decompose().depth())
        del qc

        # AQAM
        limit = ceil(log2(len(sample) + len(bigInput)) + 2)
        qc = AQAM.createAQAMCircuit(sample, bigInput, limit)
        print("AQAM depth:", qc.decompose().decompose().decompose().depth())
        del qc

    print("The size of the second input changes ie) '1', '11', '111'...")
    for sample in testInputs:
        print("input size of: ", len(sample), " x ", len(bigInput))
        # OPB
        qc = OPB.createOPBCircuit(sample, bigInput)
        print(" OPB depth:", qc.decompose().decompose().decompose().depth())
        del qc

        # IOPB
        qc = IOPB.createIOPBCircuit(sample, bigInput)
        print("IOPB depth:", qc.decompose().decompose().decompose().depth())
        del qc

        # QFM
        # qc = QFM.createQFMCircuit(sample, bigInput)
        # print(" QFM depth:", qc.decompose().decompose().decompose().depth())
        # del qc

        # QAM
        qc = QAM.createQAMCircuit(sample, bigInput)
        print(" QAM depth:", qc.decompose().decompose().decompose().depth())
        del qc

        # AQAM
        limit = ceil(log2(len(sample)+len(bigInput)) + 2)
        qc = AQAM.createAQAMCircuit(sample, bigInput, limit)
        print("AQAM depth:", qc.decompose().decompose().decompose().depth())
        del qc


def main():
    numToTest = 8                       # max number of bits to run the simulation to
    timesToTest = 20                    # number of times to repeat each test
    ScalingAllTests(8)
    # OPBTest(numToTest, timesToTest)
    # IOPBTest(numToTest, timesToTest)
    # QFMTest(numToTest, timesToTest)
    # QAMTest(numToTest, timesToTest)
    # AQAMTest(numToTest, timesToTest)


if __name__ == "__main__":
    main()
