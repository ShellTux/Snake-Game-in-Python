class Vector:
    def __init__(self, x: int | float, y: int | float):
        self.x = x
        self.y = y

    def __add__(self, other_vector):
        return Vector(self.x + other_vector.x, self.y + other_vector.y)

    def __repr__(self):
        return str((self.x, self.y))

    def __eq__(self, other_vector):
        if other_vector == None:
            return False
        return self.x == other_vector.x and self.y == other_vector.y

    def __iter__(self):
        return iter((self.x, self.y))

    def copy(self):
        return Vector(self.x, self.y)

    def constrain(self, minimum_vector, maximum_vector):
        self.x = min(max(self.x, minimum_vector.x), maximum_vector.x)
        self.y = min(max(self.y, minimum_vector.y), maximum_vector.y)
        return Vector(self.x, self.y)
