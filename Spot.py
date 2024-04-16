class Spot(object):
    def __init__(self, image_x, image_y, person=None):
        self.location = (image_x, image_y)
        self.person = person
        self.relations = {}

    def __repr__(self):
        return f"Spot at {self.location}. {self.person if self.person is not None else 'no one'} sits here."
    def add_nearby_spot(self, other_spot, strength=1):
        self.relations[other_spot] = strength
