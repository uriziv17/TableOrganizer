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
    maxVal = 0.7
    minVal = 1-maxVal/(num_of_persons-1)
    prMatrix = np.full((num_of_persons, num_of_persons),minVal)
    for i in range(num_of_persons):
        prMatrix[i, i] =maxVal
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
    print(prMatrix, "after update ")


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
                - table.get_relation_between(spot1, spot2)
            )
        )


def calculateSupport(table, personsMatrix, person1, spot1, prMatrix):
    support = 0
    for spot in table.spots.keys():
        for person in range(len(personsMatrix)):
            support = (
                support
                + calculateR(table, personsMatrix, person1, spot1, person, spot)
                * prMatrix[spot][person]
            )
    return support


def findSitting(table: Table, personsMatrix):
    prMatrix = setPrMatrix(table)
    for i in range(5):
        updatePrMatrix(table, prMatrix, personsMatrix)

    seatingArr = []
    for i in range(len(table.spots)):
        currSpotPr = []
        for j in range(len(table.spots)):
            currSpotPr.append(prMatrix[i][j])
        person = currSpotPr.index(max(currSpotPr))
        seatingArr.append(person)
        for l in range(i+1, len(table.spots)):
            prMatrix[l][person] = 0
        print(prMatrix, "after removing person ",person)
        print(currSpotPr, "test current spot")
    print(seatingArr)
    return seatingArr
