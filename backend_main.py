import random
import cv2
import numpy as np
from actions.relaxtionLabel.relaxtion import findSitting
from Table import *

if __name__ == "__main__":
    table = Table("Images/table8NoMap.jpg")
    print(len(table.spots))
    people = {
        0: "uri",
        1: "mom",
        2: "michal",
        3: "claire",
        4: "daniel",
        5: "nuriel",
        6: "ben",
        7: "dad",
    }
    person_matrix = [
        [0.5, 1, 1, 0, 0.5, 0.5, 0, 1],
        [1, 0.5, 0, 1, 0, 0.5, 0.5, 0],
        [1, 0, 0.5, 0.5, 0.5, 0, 1, 1],
        [0, 1, 0.5, 0.5, 0.5, 1, 0.5, 0.5],
        [0.5, 0, 0.5, 0.5, 0.5, 1, 0.5, 1],
        [0.5, 0.5, 0, 1, 1, 0.5, 0, 0.5],
        [0, 0.5, 1, 0.5, 0.5, 0, 0.5, 0.5],
        [1, 0, 1, 0.5, 1, 0.5, 0.5, 0.5],
    ]

    want = set()
    dont_want = set()
    for i in range(len(people)):
        for j in range(i + 1):
            if person_matrix[i][j] == 1:
                want.add((people[i], people[j]))
            elif person_matrix[i][j] == 0:
                dont_want.add((people[i], people[j]))

    print(want)
    print(dont_want)

    arrangement = findSitting(table, person_matrix)
    table.populate_spots(people, arrangement)
    table.draw_sitting_arrangement("./result.jpg")
