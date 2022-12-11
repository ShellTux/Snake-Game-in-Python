from tkinter import Canvas, Label
from Snake import Snake
from Vector import Vector
from random import randint, choice

class Grid:
    def __init__(self, rows: int, cols: int, highscore_file_path: str):
        self.rows = rows
        self.cols = cols
        self.snake = Snake(randint(0, rows - 1), randint(0, cols - 1))
        self.food = Vector(randint(0, rows - 1), randint(0, cols - 1))
        self.food_color = 'green'
        self.score = 0

        # Getting highest highscore from file
        all_highscores: list[int] = []
        try:
            with open(highscore_file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    stripped_line = line.strip()
                    if stripped_line == '':
                        continue
                    all_highscores.append(int(stripped_line))
        except FileNotFoundError:
            all_highscores: list[int] = []
        self.highscore = max(all_highscores) if len(all_highscores) > 0 else 0

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

    def check_if_eating_food(self, label: Label):
        # Check if snake is eating the food
        if self.snake.body[0] == self.food:
            self.generate_food()
            self.snake.grow()
            self.score += 10
            if self.score > self.highscore:
                self.highscore = self.score
            label.config(text = f'Score: {self.score} | Highscore: {self.highscore}')


    def check_collision(self):
        # Check if snake body collided with walls
        if (
                self.snake.body[0].x < 0 or 
                self.snake.body[0].y > self.rows - 1 or 
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

    def update(self, canvas: Canvas, label: Label):
        # Clear screen
        canvas.delete('all')
        self.snake.move()
        # Check if collided with walls or with it's own body
        if (self.check_collision()):
            return False
        self.check_if_eating_food(label)
        self.snake.body[0].constrain(Vector(0, 0), Vector(self.rows - 1, self.cols - 1))
        self.show(canvas)
        canvas.update()
        return True
