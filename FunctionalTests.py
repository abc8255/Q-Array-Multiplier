from qiskit import QuantumRegister, QuantumCircuit, ClassicalRegister
import numpy as np
import approxQArrayMultiplier as AQAM
import ImpRepAddition as IOPB
import QArrayMultiplier as QAM
import RepeatedAddition as OPB
from sharedFunctions import runIdeal, runNoisy
from math import ceil, log2


def OPBTest(maxNum):
    """
    TODO

    :param maxNum: The highest size input to run the test up to
    """
    # Testing Square case
    num = ""
    for i in range(maxNum):
        num = num + "1"
        print("Creating a square OPB Circuit of size ", num)
        qc = OPB.createOPBCircuit(num, num)
        print("depth :", qc.decompose().decompose().decompose().depth())
        runIdeal(qc)
        runNoisy(qc)
        del qc
        print("---------", num)
    num = ""
    print("-----------------------", num)
    # Testing Identity case
    for i in range(maxNum):
        num = num + "1"
        print("Creating an identity OPB Circuit of size ", num)
        qc = OPB.createOPBCircuit(num, "1")
        print("depth :", qc.decompose().decompose().decompose().depth())
        runIdeal(qc)
        runNoisy(qc)
        del qc
        print("---------", num)
    print("______________END_OF_OPB_______________", num)


def IOPBTest(maxNum):
    """
    TODO

    :param maxNum: The highest size input to run the test up to
    """
    # Testing Square case
    num = ""
    for i in range(maxNum):
        num = num + "1"
        print("Creating a square IOPB Circuit of size ", num)
        qc = IOPB.createIOPBCircuit(num, num)
        print("depth :", qc.decompose().decompose().decompose().depth())
        runIdeal(qc)
        runNoisy(qc)
        del qc
        print("---------", num)
    num = ""
    print("-----------------------", num)
    # Testing Identity case
    for i in range(maxNum):
        num = num + "1"
        print("Creating an identity IOPB Circuit of size ", num)
        qc = IOPB.createIOPBCircuit(num, "1")
        print("depth :", qc.decompose().decompose().decompose().depth())
        runIdeal(qc)
        runNoisy(qc)
        del qc
        print("---------", num)
    print("______________END_OF_IOPB_______________", num)


def QAMTest(maxNum):
    """
    TODO

    :param maxNum: The highest size input to run the test up to
    """
    # Testing Square case
    num = ""
    for i in range(maxNum):
        num = num + "1"
        print("Creating a square QAM Circuit of size ", num)
        qc = QAM.createQAMCircuit(num, num)
        print("depth :", qc.decompose().decompose().decompose().depth())
        runIdeal(qc)
        runNoisy(qc)
        del qc
        print("---------", num)
    num = ""
    print("-----------------------", num)
    # Testing Identity case
    for i in range(maxNum):
        num = num + "1"
        print("Creating an identity QAM Circuit of size ", num)
        qc = QAM.createQAMCircuit(num, "1")
        print("depth :", qc.decompose().decompose().decompose().depth())
        runIdeal(qc)
        runNoisy(qc)
        del qc
        print("---------", num)
    print("______________END_OF_QAM_______________")


def AQAMTest(maxNum):
    """
    TODO

    :param maxNum: The highest size input to run the test up to
    """
    # Testing Square case
    num = ""
    for i in range(1, maxNum+1):
        num = num + "1"
        limit = ceil(log2(i*2) + 2)
        print("Creating a square AQAM Circuit of size ", num)
        qc = AQAM.createAQAMCircuit(num, num, limit)
        print("depth :", qc.decompose().decompose().decompose().depth())
        runIdeal(qc)
        runNoisy(qc)
        del qc
        print("---------", num)
    num = ""
    print("-----------------------", num)
    # Testing Identity case
    for i in range(1, maxNum+1):
        num = num + "1"
        limit = ceil(log2(i+1) + 2)
        print("Creating an identity AQAM Circuit of size ", num)
        qc = AQAM.createAQAMCircuit(num, "1", limit)
        print("depth :", qc.decompose().decompose().decompose().depth())
        runIdeal(qc)
        runNoisy(qc)
        del qc
        print("---------", num)
    print("______________END_OF_AQAM_______________", num)


def main():
    numToTest = 4
    # OPBTest(numToTest)
    # IOPBTest(numToTest)
    # QAMTest(numToTest)
    AQAMTest(numToTest)


if __name__ == "__main__":
    main()
