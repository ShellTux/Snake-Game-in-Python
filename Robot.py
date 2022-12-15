from Grid import Grid
from Vector import Vector

class Robot:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.came_from: dict[tuple[int, int], tuple[int, int]] = {}

    def play(self, came_from_path: dict[tuple[int, int], tuple[int, int]]):

        if len(came_from_path) != 0:
            current_pos = tuple(map(int, self.grid.snake.body[0].tuple())) 
            next_pos = tuple(map(int, came_from_path[current_pos]))
            move = Vector(next_pos[0] - current_pos[0], next_pos[1] - current_pos[1])
            
            self.grid.snake.moves_buffer.append(move)
        else:
            pass
