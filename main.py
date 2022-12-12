#!/usr/bin/env python3
from tkinter import Tk, Canvas, Label
from time import sleep
from Grid import Grid

ROWS = COLS = 20
WIDTH = HEIGHT = 600
WINDOW_TITLE: str = 'Snake Game'
BACKGROUND_COLOR: str = 'black'
HIGHSCORE_FILE_PATH: str = 'highscore.txt'


class App:
    def __init__(self, title: str, width: int, height: int, *, background_color: str = BACKGROUND_COLOR, frame_rate: int = 10, highscore_file_path: str = HIGHSCORE_FILE_PATH):
        # Window setup
        window = Tk()
        window.title(title)
        window.resizable(False, False)
        self.window = window
        # Label Setup
        label = Label(window, text = f'Score: 0 | Highscore: 0', font = ('Hlevetica 30 bold'))
        label.pack()
        self.highscore_label = label
        # Canvas setup
        canvas = Canvas(window, width = width, height = height, bg = background_color)
        canvas.pack()
        self.canvas = canvas

        self.width = width
        self.height = height
        self.isRunning = True
        self.frame_rate = frame_rate
        self.highscore_file_path = highscore_file_path

    def create_grid(self, rows: int, cols: int):
        self.grid = Grid(rows, cols, self.highscore_file_path)
        self.highscore_label.config(text = f'Score: {self.grid.score} | Highscore: {self.grid.highscore}')
        self.window.bind('<Key>', self.grid.snake.change_direction)

    def update(self):
        return self.grid.update(self.canvas, self.highscore_label)

    def destroy(self):
        self.window.destroy()

    def mainloop(self):
        while self.isRunning:
            self.isRunning = self.update()
            sleep(1 / self.frame_rate)

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
    myApp = App(WINDOW_TITLE, WIDTH, HEIGHT, background_color = BACKGROUND_COLOR)
    myApp.create_grid(ROWS, COLS)

    myApp.mainloop()

    print('You Lose!!!')
    myApp.save_highscore()
