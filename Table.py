import cv2


class Table(object):
    def __init__(self, image_path):
        self.image = cv2.imread(image_path)

    def extract_spots(self):
        """
        here we will infer the locations of all the spots using cv2
        :return:
        """
        pass
