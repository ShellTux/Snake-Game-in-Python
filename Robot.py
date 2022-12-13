from Grid import Grid
from Vector import Vector
from random import choice

class Robot:
    def __init__(self, grid: Grid):
        self.grid = grid

    def play(self):
        # This function will return True if the next position is not colliding with
        # a wall or it's own body
        def is_valid_move(move: Vector):
            next_position = self.grid.snake.body[0] + move
            return (0 <= next_position.x < self.grid.rows and
                    0 <= next_position.y < self.grid.cols and
                    all([ next_position != segment for segment in self.grid.snake.body[1:] ])
                    )

        def distance_squared_to_food(move: Vector):
            next_position = self.grid.snake.body[0] + move
            food = self.grid.food
            return (next_position.x - food.x) ** 2 + (next_position.y - food.y) ** 2

        possible_moves = [
                Vector(1, 0),
                Vector(-1, 0),
                Vector(0, 1),
                Vector(0, -1)
                ]

        possible_moves = list(filter(is_valid_move, possible_moves))

        next_move = min(possible_moves, key = distance_squared_to_food)

        self.grid.snake.moves_buffer.append(next_move)
