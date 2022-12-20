from Grid import Grid
from Vector import Vector
from random import choice

strategies: tuple[str, str, str, str] = (
        'A* path finding algorithm',
        'Nearest Neighbor',
        'Random Walk',
        'Cycle'
        )

class Robot:
    def __init__(self, grid: Grid, strategy: str):
        self.grid = grid
        self.strategy: str = strategy
        if strategy == 'Cycle':
            def get_move_for_cycle(i: int, j: int) -> Vector:
                move: Vector = Vector(1 if j % 2 == 0 else -1, 0)
                if i == self.grid.rows - 1 and j % 2 == 0 and j < self.grid.cols - 1:
                    move = Vector(0, 1)
                elif i == 0 and j > 0:
                    move = Vector(0, -1)
                elif i == 1 and j % 2 == 1 and j < self.grid.cols - 1:
                    move = Vector(0, 1)
                return move
            self.cycle: list[list[Vector]] = [ [ get_move_for_cycle(i, j) for j in range(self.grid.cols) ] for i in range(self.grid.rows) ]


    def play(self):
        def valid_move(move: Vector) -> bool:
            rows = self.grid.rows
            cols = self.grid.cols
            snake_head = self.grid.snake.body[0]
            next_pos: Vector = snake_head + move
            return 0 <= next_pos.x < rows and 0 <= next_pos.y < cols and next_pos not in self.grid.snake.body[1:]

        def distance_square_to_food(move: Vector) -> int | float:
            next_pos = self.grid.snake.body[0] + move
            food = self.grid.food
            return (next_pos.x - food.x) ** 2 + (next_pos.y - food.y) ** 2

        def manhatan_distance_to_food(move: Vector) -> int | float:
            next_pos = self.grid.snake.body[0] + move
            food = self.grid.food
            return abs(next_pos.x - food.x) + abs(next_pos.y - food.y)

        next_move = None

        if self.strategy == 'A* path finding algorithm':
            came_from_path = self.grid.came_from_path
            if len(came_from_path) != 0:
                current_pos: tuple[int, int] = tuple(map(int, self.grid.snake.body[0].tuple())) 
                next_pos: tuple[int, int] = tuple(map(int, came_from_path[current_pos]))
                next_move = Vector(next_pos[0] - current_pos[0], next_pos[1] - current_pos[1])


        elif self.strategy == 'Nearest Neighbor':
            possible_neighbors = tuple(filter(valid_move, (
                Vector(1, 0),
                Vector(-1, 0),
                Vector(0, 1),
                Vector(0, -1)
                )))
            if len(possible_neighbors) != 0:
                next_move = min(possible_neighbors, key = manhatan_distance_to_food)


        elif self.strategy == 'Random Walk':
            possible_neighbors = tuple(filter(valid_move, (
                Vector(1, 0),
                Vector(-1, 0),
                Vector(0, 1),
                Vector(0, -1)
                )))
            if len(possible_neighbors) != 0:
                next_move = choice(possible_neighbors)


        elif self.strategy == 'Cycle':
            snake_i, snake_j = tuple(map(int, self.grid.snake.body[0].tuple()))
            next_move = self.cycle[snake_i][snake_j]


        if next_move:
            self.grid.snake.moves_buffer.append(next_move)
