import Table
import Spot
from collections import defaultdict

def setPersonsMatrix(table):
    num_of_persons = len(table.spots)
    personsMatrix = [[0.5]*num_of_persons]*num_of_persons
    return personsMatrix

def setPrMatrix(table):
    num_of_persons = len(table.spots)
    prMatrix = [[1/num_of_persons]]*num_of_persons*num_of_persons
    return prMatrix

def updatePersonsMatrix(personsMatrix, person1, person2, like):
    if personsMatrix[person1][person2]!= 0.5:
        return False
    if like:
        personsMatrix[person1][person2]=personsMatrix[person2][person1]=1
        return True
    if like==False:
        personsMatrix[person1][person2]=personsMatrix[person2][person1]=0
        return True
    return False

def calculateR(table, personsMatrix, person1, spot1, person2, spot2):
    if person1==person2:
        if spot1==spot2:
            return 1
        else:
            return 0
    if (personsMatrix[person1][person2])<0.5:
        return 0.9
    elif (personsMatrix[person1][person2])>0.5:
        return 0.001
    else:
        return 0.5
    
def calculateSupport(table, personsMatrix, person1, spot1, prMatrix):
    support = 0
    for spot in table.spots:
        for person in personsMatrix[person1]:
            support = support+ calculateR(table, personsMatrix, person1, spot1, person, spot)*prMatrix[person][spot]
    return support


