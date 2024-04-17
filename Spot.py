class Spot(object):
    def __init__(self, image_x, image_y, person=None):
        self.location = (image_x, image_y)
        self.person = person


    def __repr__(self):
        return f"Spot at {self.location}. {self.person if self.person is not None else 'no one'} sits here."

