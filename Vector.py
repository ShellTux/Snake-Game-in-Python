class Vector:
    def __init__(self, x: int | float = 0, y: int | float = 0):
        self.x = x
        self.y = y

    def __add__(self, other_vector):
        return Vector(self.x + other_vector.x, self.y + other_vector.y)

    def __mul__(self, scalar: int | float):
        return Vector(self.x * scalar, self.y * scalar)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def scale(self, scalar: int | float):
        self.x *= scalar
        self.y *= scalar
        return Vector(self.x, self.y)

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

def lerp(vector1: Vector, vector2: Vector, interpolation: float):
    return Vector(
            vector1.x + (vector2.x - vector1.x) * interpolation,
            vector1.y + (vector2.y - vector1.y) * interpolation
            )
