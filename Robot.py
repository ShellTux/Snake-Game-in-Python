from Grid import Grid
from Vector import Vector
from itertools import pairwise

class Robot:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.generate_path()
        self.path = []

    def play(self):
        # This function will return True if the next position is not colliding with
        # a wall or it's own body
        def is_valid_move(move: Vector) -> bool:
            next_position = self.grid.snake.body[0] + move
            return (0 <= next_position.x < self.grid.rows and
                    0 <= next_position.y < self.grid.cols and
                    next_position not in self.grid.snake.body[1:]
                    )

        def distance_squared_to_food(move: Vector) -> int | float:
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

        if len(possible_moves) == 0:
            return

        next_move = min(possible_moves, key = distance_squared_to_food)

        self.grid.snake.moves_buffer.append(next_move)

    def generate_path(self):
        m = [
                [int(Vector(i, j) in self.grid.snake.body[1:]) for j in range(self.grid.cols)] for i in range(self.grid.rows)
                ]

        food_pos = (int(self.grid.food.x), int(self.grid.food.y))
        snake_head_pos = (int(self.grid.snake.body[0].x), int(self.grid.snake.body[0].y))
        path = A_star(m, food_pos, snake_head_pos)[::-1]
        print(food_pos)
        print(snake_head_pos)
        print(path)
        self.grid.snake.moves_buffer.extend(
                [ 
                 Vector(next_pos[0] - current_pos[0], next_pos[1] - current_pos[1])
                 for next_pos, current_pos in pairwise(path)
                 ]
                )

def reconstruct_path(came_from: dict[tuple[int, int], tuple[int, int]], current: tuple[int, int], start: tuple[int, int]) -> list[tuple[int, int]]:
    total_path = [current]
    while current != start:
        current = came_from[current]
        total_path.append(current)
    return total_path

def h(point1: tuple[int, int], point2: tuple[int, int]) -> int | float:
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

def A_star(matrix: list[list[int]], start: tuple[int, int], goal: tuple[int, int]) -> list[tuple[int, int]]:
    matrix_rows = len(matrix)
    matrix_cols = len(matrix[0]) # Assuming that the matrix is square
    open_set: list[tuple[int, int]] = [start]
    came_from: dict[tuple[int, int], tuple[int, int]] = {}

    g_score: dict[tuple[int, int], int | float] = {}
    g_score[start] = 0


    f_score: dict[tuple[int, int], int | float] = {}
    f_score[start] = g_score[start] + h(start, goal)

    while len(open_set) > 0:
        current = min(open_set, key = lambda k: f_score[k])

        if current == goal:
            return reconstruct_path(came_from, current, start)

        open_set.remove(current)

        for neighbor in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor_pos: tuple[int, int] = (current[0] + neighbor[0], current[1] + neighbor[1])
            row, col = neighbor_pos

            # Invalid neighbor
            if not (0 <= row < matrix_rows and 0 <= col < matrix_cols):
                continue

            if matrix[row][col] == 1:
                continue

            tentative_g_score = g_score[current] + 10 # d(current, neighbor_pos)

            if g_score.get(neighbor_pos) == None:
                g_score[neighbor_pos] = float('inf')

            if tentative_g_score < g_score[neighbor_pos]:
                came_from[neighbor_pos] = current
                g_score[neighbor_pos] = tentative_g_score
                f_score[neighbor_pos] = tentative_g_score + h(neighbor, goal)
                if neighbor_pos not in open_set:
                    open_set.append(neighbor_pos)

    return []


if __name__ == '__main__':
    m = [
            [0, 0, 0],
            [0, 1, 0],
            [0, 1, 0]
            ]
    print(A_star(m, (2, 2), (2, 2))[::-1])
