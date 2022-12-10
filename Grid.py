from tkinter import Tk, Canvas
from Snake import Snake
from Vector import Vector
from random import randint, choice

class Grid:
    def __init__(self, window: Tk, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.snake = Snake(window, randint(0, rows - 1), randint(0, cols - 1))
        self.food = Vector(randint(0, rows - 1), randint(0, cols - 1))
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

        # Show food
        food_x = self.food.y * dw
        food_y = self.food.x * dh
        canvas.create_rectangle(
                food_x,
                food_y,
                food_x + dw,
                food_y + dh,
                fill = self.food_color,
                outline = 'white'
                )

        # Show snake
        # for index, segment in enumerate(self.snake.body):
        for i in range(len(self.snake.body) - 1, -1, -1):
            segment = self.snake.body[i]
            fill_color = self.snake.head_color if i == 0 else self.snake.body_color 
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

    def check_collision(self):
        # Check if snake is eating the food
        if self.snake.body[0] == self.food:
            self.generate_food()
            self.snake.grow()


        # Check if snake body collided with walls
        if (
                self.snake.body[0].x < 0 or 
                self.snake.body[0].y > self.rows or 
                self.snake.body[0].y < 0 or 
                self.snake.body[0].y > self.cols
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
        possible_cels = []
        for i in range(self.rows):
            for j in range(self.cols):
                possible_cels.append((i, j))

        # Remove snake body segments from possible cels
        for segment in self.snake.body:
            position = (segment.x, segment.y)
            if position in possible_cels:
                possible_cels.remove(position)

        chosen_cell = choice(possible_cels)
        self.food = Vector(chosen_cell[0], chosen_cell[1])

    def update(self, canvas: Canvas):
        canvas.delete('all')
        self.snake.move()
        self.snake.body[0].constrain(Vector(0, 0), Vector(self.rows - 1, self.cols - 1))
        if (self.check_collision()):
            print('collision')
            # self.window.destroy()
        self.show(canvas)
        canvas.update()
