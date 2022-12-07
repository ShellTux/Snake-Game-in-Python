from tkinter import Tk, Canvas
from time import sleep
from functools import partial

ROWS = COLS = 30
WIDTH = HEIGHT = 600
WINDOW_TITLE: str = 'Snake Game'
BACKGROUND_COLOR: str = 'black'

class App:
    def __init__(self, title: str, width: int, height: int, *, background_color: str = BACKGROUND_COLOR):
        window = Tk()
        window.title(title)
        window.resizable(False, False)
        self.window = window
        canvas = Canvas(window, width = width, height = height, bg = background_color)
        canvas.pack()
        self.canvas = canvas
        self.width = width
        self.height = height
        self.isRunning = True

class Grid:
    def __init__(self, window: Tk, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.snake = Snake(window, 0, 0)
        self.food = Vector(10, 10)
        self.food_color = 'green'

    def show(self, canvas: Canvas):
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        dw = width / self.cols
        dh = height / self.rows
                
        # Showing lines
        for i in range(self.rows):
            canvas.create_line(0, dh * i, width, dh * i, fill = 'white')

        # Showing columns
        for j in range(self.cols):
            canvas.create_line(dw * j, 0, dw * j, height, fill = 'white')

        # Show snake
        for index, segment in enumerate(self.snake.body):
            fill_color = self.snake.head_color if index == 0 else self.snake.body_color 
            segment_row, segment_column = segment
            segment_x = segment_column * dw
            segment_y = segment_row * dh
            canvas.create_rectangle(
                    segment_x,
                    segment_y,
                    segment_x + dw,
                    segment_y + dh,
                    fill = fill_color,
                    outline = 'white'
                    )

        # Show food
        food_x = self.food.x * dw
        food_y = self.food.y * dh
        canvas.create_rectangle(
                food_x,
                food_y,
                food_x + dw,
                food_y + dh,
                fill = self.food_color,
                outline = 'white'
                )


    def update(self, canvas: Canvas):
        canvas.delete('all')
        self.show(canvas)
        self.snake.move()
        canvas.update()


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


class Snake:
    def __init__(self, window: Tk, row: int, col: int, *, head_color: str = 'red', body_color: str = 'green'):
        self.body = [Vector(row, col)]
        self.head_color = head_color
        self.body_color = body_color
        self.velocity = None
        window.bind('<Key>', self.change_direction)

    def change_direction(self, key_event):
        map_direction_to_velocity = {
                # Up
                'w': Vector(-1, 0),
                # Left
                'a': Vector(0, -1),
                # Down
                's': Vector(1, 0),
                # Right
                'd': Vector(0, 1)
                }

        # If dictionary doesn't have key for the key press then exit function
        if map_direction_to_velocity.get(key_event.char) == None:
            return

        new_velocity = map_direction_to_velocity[key_event.char]
        
        # First check if velocity is not None and
        # If current velocity and new velocity go in different directions
        # Then when we multiply each component it will give -1, so we will
        # Skip self.velocity update because both velocities go in opposite directions, which is not valid
        if self.velocity != None and (
                self.velocity.x * new_velocity.x == -1 or
                self.velocity.y * new_velocity.y == -1
                ):
            return

        self.velocity = new_velocity
        print(self.velocity)

    def move(self):
        if self.velocity == None:
            return

        # Move snake head by self.velocity
        self.body[0] += self.velocity 


if __name__ == '__main__':
    myApp = App(WINDOW_TITLE, WIDTH, HEIGHT, background_color = BACKGROUND_COLOR)
    game_grid = Grid(myApp.window, ROWS, COLS)

    while myApp.isRunning:
        game_grid.update(myApp.canvas)
        sleep(0.1)
