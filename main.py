#!/usr/bin/env python3
from tkinter import Tk, Canvas, Label
from time import sleep
from Grid import Grid

ROWS = COLS = 20
WIDTH = 600
WINDOW_TITLE: str = 'Snake Game'
BACKGROUND_COLOR: str = 'black'
HIGHSCORE_FILE_PATH: str = 'highscore.txt'


class App:
    def __init__(self, title: str, canvas_width: int, *, background_color: str = BACKGROUND_COLOR, frame_rate: int = 10, highscore_file_path: str = HIGHSCORE_FILE_PATH):
        # Window setup
        window = Tk()
        window.title(title)
        window.resizable(False, False)
        self.window = window
        # Label Setup
        highscore_label = Label(window, text = f'Score: 0 | Highscore: 0', font = ('Hlevetica 30 bold'))
        self.highscore_label = highscore_label
        # Canvas setup
        canvas = Canvas(window, width = canvas_width, height = canvas_width, bg = background_color)
        self.canvas = canvas

        self.width = self.height = canvas_width
        self.isRunning = True
        self.frame_rate = frame_rate
        self.highscore_file_path = highscore_file_path

        # Steps label
        steps_label = Label(window, text = 'Movements: 0', font = ('Helvetica 30 bold'))
        self.steps_label = steps_label

        # Packing all elements into the window
        # Order is crucial
        highscore_label.pack()
        canvas.pack()
        steps_label.pack()

    def update_steps_label(self, steps: int):
        self.steps_label.config(text = f'Number of Steps: {steps}')

    def update_highscore_label(self, score: int, highscore: int):
        self.highscore_label.config(text = f'Score: {score} | Highscore: {highscore}')

    def create_grid(self, rows: int, cols: int):
        self.grid = Grid(rows, cols, self.highscore_file_path, image_width = min(self.width, self.height) // cols) # quick temporary fix for image_width
        self.update_highscore_label(self.grid.score, self.grid.highscore)
        self.window.bind('<Key>', self.grid.snake.change_direction)

    def update(self):
        self.canvas.delete('all')
        is_running = self.grid.update(self.canvas, self.update_highscore_label)
        self.update_steps_label(self.grid.snake.steps)
        return is_running

    def mainloop(self):
        while self.update():
            sleep(1 / self.frame_rate)

        # Bind button release event to canvas element to close window
        self.canvas.bind('<ButtonRelease>', lambda _: self.window.destroy())
        # Bind q key press to window element to close window
        self.window.bind('q', lambda _: self.window.destroy())

        self.canvas.mainloop()

    def save_highscore(self):
        all_highscores: list[int] = []
        try:
            with open(self.highscore_file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    # Remove blank spaces or new lines
                    stripped_line = line.strip()
                    # Ignore empty lines
                    if stripped_line == '':
                        continue
                    all_highscores.append(int(stripped_line))
        except FileNotFoundError:
            all_highscores = []

        # Open highscore file in append mode to add a new line with the highscore
        with open(self.highscore_file_path, 'a') as file:
            # Only write to the file if already doesn't contain the highscore
            if self.grid.highscore not in all_highscores:
                file.write(f'{self.grid.highscore}\n')


if __name__ == '__main__':
    myApp = App(WINDOW_TITLE, WIDTH, background_color = BACKGROUND_COLOR)
    myApp.create_grid(ROWS, COLS)

    myApp.mainloop()

    print('You Lose!!!')
    myApp.save_highscore()
