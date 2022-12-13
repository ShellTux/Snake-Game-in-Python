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

    def show(self, canvas: Canvas):
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        dw = width // self.cols
        dh = height // self.rows

        for i in range(self.rows):
            for j in range(self.cols):
                x = j * dw
                y = i * dh
                canvas.create_rectangle(
                        x,
                        y,
                        x + dw,
                        y + dh,
                        fill = 'grey',
                        outline = 'white'
                        )
                
        # Showing lines
        for i in range(self.rows):
            canvas.create_line(0, dh * i, width, dh * i, fill = 'white')

        # Showing columns
        for j in range(self.cols):
            canvas.create_line(dw * j, 0, dw * j, height, fill = 'white')

        # Show food
        food_x = self.food.y * dw
        food_y = self.food.x * dh
        canvas.create_image(food_x, food_y, image = self.food_image, anchor = 'nw')

        # Show snake
        self.snake.show(canvas, dw, dh)

    def check_if_eating_food(self, update_highscore_label):
        # Check if snake is eating the food
        if self.snake.body[0] != self.food:
            return False

        self.generate_food()
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

        chosen_cell = choice(possible_cels)
        self.food = Vector(chosen_cell[0], chosen_cell[1])

    def update(self, canvas: Canvas, update_highscore_label):
        # Clear screen
        canvas.delete('all')
        self.snake.move()
        # Check if collided with walls or with it's own body
        if (self.check_collision()):
            return False
        self.check_if_eating_food(update_highscore_label)
        self.show(canvas)
        canvas.update()
        return True
