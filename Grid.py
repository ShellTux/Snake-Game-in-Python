from tkinter import Canvas, PhotoImage
from Snake import Snake
from Vector import Vector
from random import randint, choice

class Grid:
    def __init__(self, rows: int, cols: int, highscore_file_path: str, *, image_width: int):
        self.rows = rows
        self.cols = cols
        self.snake = Snake(randint(0, rows - 1), randint(0, cols - 1))
        self.food = Vector(randint(0, rows - 1), randint(0, cols - 1))
        self.food_color = 'green'
        food_image = PhotoImage(file = 'apple.png')
        self.food_image = food_image.subsample(food_image.width() // image_width)
        self.score = 0
        self.win: bool = False

        max_highscore = 0
        try:
            with open(highscore_file_path, 'r') as file:
                def convert_string_to_number(frase: str):
                    try:
                        return int(frase.strip())
                    except ValueError:
                        return 0
                max_highscore = max(map(convert_string_to_number, file.readlines()))
        except FileNotFoundError:
            max_highscore = 0
        self.highscore = max_highscore

        self.generate_path()

    def check_if_eating_food(self, update_highscore_label):
        # Check if snake is eating the food
        if self.snake.body[0] != self.food:
            return False

        self.generate_food()
        self.generate_path()
        self.snake.bolus.append(0)
        self.snake.grow()
        self.score += 10
        if self.score > self.highscore:
            self.highscore = self.score
        update_highscore_label(self.score, self.highscore)
        return True


    def check_collision(self):
        # Check if snake body collided with walls
        if (
                self.snake.body[0].x < 0 or 
                self.snake.body[0].x > self.rows - 1 or 
                self.snake.body[0].y < 0 or 
                self.snake.body[0].y > self.cols - 1
                ):
            return True

        # Check if snake collided with it's own body
        for segment in self.snake.body[1:]:
            # Collision happened
            if self.snake.body[0] == segment:
                return True

        return False

    def generate_food(self):
        # Creating a list of all locations that doesn't contain
        # any of the snake body segments, so I can choose a random
        # free spot for the food
        possible_cels: list[tuple] = []
        for i in range(self.rows):
            for j in range(self.cols):
                possible_cels.append((i, j))

        # Remove snake body segments from possible cels
        for segment in self.snake.body:
            position = (segment.x, segment.y)
            if position in possible_cels:
                possible_cels.remove(position)

        if len(possible_cels) != 0:
            chosen_cell = choice(possible_cels)
            self.food = Vector(chosen_cell[0], chosen_cell[1])
        else:
            self.win = True

    def generate_path(self, start: tuple[int, int] = tuple(), goal: tuple[int, int] = tuple(), *, m: list[list[bool]] = [], ):
        # If matrix not defined, define matrix where the cell is True
        # if there is a snake body segment
        if len(m) == 0:
            m = [
                    [ False for j in range(self.cols) ] for i in range(self.rows)
                    ]
            for segment in self.snake.body[1:]:
                m[int(segment.x)][int(segment.y)] = True

        # If start not defined, define food as start
        if len(start) == 0:
            start = tuple(map(int, self.food.tuple()))

        # if goal not defined, define goal as snake head
        if len(goal) == 0:
            goal = tuple(map(int, self.snake.body[0].tuple()))
        self.came_from_path = A_star(m, start, goal)

    def update(self, canvas: Canvas, update_highscore_label):
        self.snake.move()
        # Check if collided with walls or with it's own body
        if (self.check_collision()):
            return False
        self.check_if_eating_food(update_highscore_label)
        return True


def reconstruct_path(came_from: dict[tuple[int, int], tuple[int, int]], current: tuple[int, int], start: tuple[int, int]) -> list[tuple[int, int]]:
    total_path = [current]
    while current != start:
        current = came_from[current]
        total_path.append(current)
    return total_path

def h(point1: tuple[int, int], point2: tuple[int, int]) -> int | float:
    # manhatan distance
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

def A_star(matrix: list[list[bool]], start: tuple[int, int], goal: tuple[int, int]) -> dict[tuple[int, int], tuple[int, int]]:
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
            return came_from
            # return reconstruct_path(came_from, current, start)

        open_set.remove(current)

        for neighbor in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor_pos: tuple[int, int] = (current[0] + neighbor[0], current[1] + neighbor[1])
            row, col = neighbor_pos

            # Invalid neighbor
            if not (0 <= row < matrix_rows and 0 <= col < matrix_cols):
                continue

            # Cell wall
            if matrix[row][col]:
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

    print('failed to find path')
    return {}


if __name__ == '__main__':
    m = [
            [0, 0, 0],
            [0, 1, 0],
            [0, 1, 0]
            ]
    # print(A_star(m, (2, 2), (2, 2))[::-1])
