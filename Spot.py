import math


class Spot(object):
    def __init__(self, id, center_point, bbox, person="empty"):
        self.id = id
        self.location = center_point
        self.bounding_box = bbox # [x,y,w,h]
        self.person = person


    def __repr__(self):
        return f"Spot #{self.id} at {self.location}. {self.person if self.person is not None else 'no one'} sits here."

    def is_across(self, other, min_distance=800):
        return abs(self.location[1] - other.location[1]) < self.bounding_box[3] and math.dist(self.location, other.location) < min_distance