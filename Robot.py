from Grid import Grid
from Vector import Vector
from random import choice

class Robot:
    def __init__(self, grid: Grid):
        self.grid = grid

    def play(self):
        self.grid.snake.moves_buffer.append(
                choice([
                    Vector(1, 0),
                    Vector(-1, 0),
                    Vector(0, 1),
                    Vector(0, -1)
                    ]),
                )
