import Table
import Spot
from collections import defaultdict
import numpy as np


def setPersonsMatrix(table: Table):
    num_of_persons = len(table.spots)
    personsMatrix = [[0.5] * num_of_persons] * num_of_persons
    return personsMatrix


def setPrMatrix(table: Table):
    num_of_persons = len(table.spots)
    prMatrix = [[1 / num_of_persons]] * num_of_persons * num_of_persons
    return prMatrix


def updatePersonsMatrix(personsMatrix, person1, person2, like):
    if personsMatrix[person1][person2] != 0.5:
        return False
    if like:
        personsMatrix[person1][person2] = personsMatrix[person2][person1] = 1
        return True
    if not like:
        personsMatrix[person1][person2] = personsMatrix[person2][person1] = 0
        return True
    return False


def updatePrMatrix(table, prMatrix, personsMatrix):
    numRows, numColumns = len(prMatrix), len(prMatrix)
    res = np.zeros_like(prMatrix)
    for spot in range(numRows):
        res_denominator = 0
        for person in range(numColumns):
            res[spot][person] = prMatrix[spot][person] * calculateSupport(
                table, personsMatrix, person, spot, prMatrix
            )
            res_denominator += res[spot][person]
        for i in range(numRows):
            update = res[spot][i] / res_denominator
            prMatrix[spot][i] = update


def calculateR(table: Table, personsMatrix, person1, spot1, person2, spot2):
    if person1 == person2:
        if spot1 == spot2:
            return 1
        else:
            return 0
    if spot1 == spot2:
        return 0
    else:
        return abs(
            0.9
            - abs(
                personsMatrix[person1][person2]
                - table.get_relation_between(table, spot1, spot2)
            )
        )


def calculateSupport(table, personsMatrix, person1, spot1, prMatrix):
    support = 0
    for spot in table.spots:
        for person in personsMatrix[person1]:
            support = (
                support
                + calculateR(table, personsMatrix, person1, spot1, person, spot)
                * prMatrix[spot][person]
            )
    return support


def findSitting(table: Table, personsMatrix):
    prMatrix = setPrMatrix(table)
    for i in range(100):
        updatePrMatrix(table, prMatrix, personsMatrix)

    seatingArr = []
    for i in range(len(table.spots)):
        seatingArr[i] = prMatrix.index(max(prMatrix[i]))
    print(seatingArr)
