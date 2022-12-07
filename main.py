from tkinter import Tk, Canvas
from random import randint

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
        self.width = width
        self.height = height

class Grid:
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.snake = [
                (randint(0, rows - 1), randint(0, cols - 1))
                ]


if __name__ == '__main__':
    myApp = App(WINDOW_TITLE, WIDTH, HEIGHT, background_color = BACKGROUND_COLOR)

    myApp.window.mainloop()
