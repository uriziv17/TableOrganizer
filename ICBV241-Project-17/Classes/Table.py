import math
import cv2
from actions.identifiers.PlateDetector import PlateDetector
from Classes.Spot import Spot
from collections import defaultdict

NEARBY_SCORE = 1.0
ACROSS_SCORE = 0.6
FAR_SCORE = 0.0
PURPLE = (255, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (0, 255, 255)


class Table(object):
    def __init__(self, image_path, scale_by=0.5, thresh=172):
        self.image_path = image_path
        self.image = cv2.imread(image_path)
        self.scale = scale_by
        self.image = cv2.resize(self.image, (0, 0), fx=scale_by, fy=scale_by)
        self.thresh = thresh
        self.spots = self.extract_spots()
        self.relations = self.build_relations(self.spots)

    def __repr__(self):
        return "Table:\n\t" + "\n\t".join([str(s) for s in self.spots.values()])

    def extract_spots(self):
        """
        here we will infer the locations of all the spots using cv2
        :return:
        """
        found_contours = PlateDetector.detect_plates(
            self.image_path, threshold=self.thresh, scale_by=self.scale
        )
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
            relations[spot_index] = {
                nearest_spot_1: NEARBY_SCORE,
                nearest_spot_2: NEARBY_SCORE,
            }

            for other_index, _ in distances[2:]:
                other = spots[other_index]
                if spot.is_across(other):
                    relations[spot_index][other_index] = ACROSS_SCORE
                else:
                    relations[spot_index][other_index] = FAR_SCORE
        return relations

    def get_relations_on_image(self):
        orig = self.image.copy()
        for spot_index, rels in self.relations.items():
            spot = self.spots[spot_index]
            cv2.circle(orig, spot.location, 5, PURPLE, cv2.FILLED)
            cv2.putText(
                orig,
                f"{spot_index}",
                spot.location,
                cv2.FONT_HERSHEY_COMPLEX,
                0.7,
                (0, 0, 0),
                2,
            )
            for other_index, score in rels.items():
                other = self.spots[other_index]
                if score == NEARBY_SCORE:
                    cv2.line(orig, spot.location, other.location, GREEN, 2)
                elif score == ACROSS_SCORE:
                    cv2.line(orig, spot.location, other.location, YELLOW, 2)

        return orig

    def get_relation_between(self, spot_id_1, spot_id_2):
        return self.relations[spot_id_1][spot_id_2]

    def populate_spots(self, names_ids, sitting_arrangement):
        for spot_index, id in enumerate(sitting_arrangement):
            if names_ids.get(id):
                name = names_ids[id]
            else:
                name = "no one"
            self.spots[spot_index].person = name

    def draw_sitting_arrangement(self, save_path):
        orig = self.image.copy()
        for index, spot in self.spots.items():
            cv2.putText(
                orig,
                spot.person,
                spot.location,
                cv2.FONT_HERSHEY_COMPLEX,
                0.7,
                (0, 0, 0),
                2,
            )
        try:
            cv2.imwrite(save_path, orig)
            return True
        except IOError:
            print(f"ERROR: failed to save result image to {save_path}")
            return False
