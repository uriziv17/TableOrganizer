import math
import cv2
from PlateDetector import PlateDetector
from Spot import Spot
from collections import defaultdict

NEARBY_SCORE = 1.0
ACROSS_SCORE = 0.5
FAR_SCORE = -1.0
PURPLE = (255, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (0, 255, 255)


class Table(object):
    def __init__(self, image_path, scale_by=0.5):
        self.image_path = image_path
        self.image = cv2.imread(image_path)
        self.scale = scale_by
        self.image = image = cv2.resize(self.image, (0, 0), fx=scale_by, fy=scale_by)
        self.spots = self.extract_spots()
        self.relations = self.build_relations(self.spots)

    def __repr__(self):
        return "Table:\n\t" + "\n\t".join([str(s) for s in self.spots.values()])

    def extract_spots(self):
        """
        here we will infer the locations of all the spots using cv2
        :return:
        """
        found_contours = PlateDetector.detect_plates(self.image_path, scale_by=self.scale)
        spots = {}
        for i in range(len(found_contours)):
            spots[i] = Spot(i, found_contours[i]["center"], found_contours[i]["bbox"])
        return spots

    def build_relations(self, spots):
        relations = {}
        for spot_index, spot in spots.items():
            distances = []
            for other_index, other in spots.items():
                if spot_index != other_index:
                    dist = math.dist(spot.location, other.location)
                    distances.append((other_index, round(dist, 3)))
            distances.sort(key=lambda x: x[1])
            nearest_spot_1 = distances[0][0]
            nearest_spot_2 = distances[1][0]
            relations[spot_index] = [(nearest_spot_1, NEARBY_SCORE), (nearest_spot_2, NEARBY_SCORE)]

            for other_index, _ in distances[2:]:
                other = spots[other_index]
                if spot.is_across(other):
                    relations[spot_index].append((other_index, ACROSS_SCORE))
                else:
                    relations[spot_index].append((other_index, FAR_SCORE))
        return relations

    def get_relations_on_image(self):
        orig = self.image.copy()
        for spot_index, rels in self.relations.items():
            spot = self.spots[spot_index]
            cv2.circle(orig, spot.location, 5, PURPLE, cv2.FILLED)
            for other_index, score in rels:
                other = self.spots[other_index]
                if score == NEARBY_SCORE:
                    cv2.line(orig, spot.location, other.location, GREEN, 2)
                elif score == ACROSS_SCORE:
                    cv2.line(orig, spot.location, other.location, YELLOW, 2)

        return orig
