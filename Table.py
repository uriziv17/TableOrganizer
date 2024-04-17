import cv2
from collections import defaultdict


class Table(object):
    def __init__(self, image_path):
        self.image = cv2.imread(image_path)
        self.spots = defaultdict(list)

    def __repr__(self):
        return "Table:\n\t" + "\n\t".join([str(s) for s in self.spots.keys()])
    def extract_spots(self):
        """
        here we will infer the locations of all the spots using cv2
        :return:
        """
        pass

    def add_spot(self, spot):
        if spot not in self.spots:
            self.spots[spot] = []

    def add_connection(self, spot1, spot2, strength=1):
        self.spots[spot1].append((spot2, strength))
        self.spots[spot2].append((spot1, strength))
