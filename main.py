#!/usr/bin/env python3
from tkinter import Tk, Canvas
from time import sleep
from random import randint, choice
from itertools import pairwise
from Grid import Grid

ROWS = COLS = 20
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


if __name__ == '__main__':
    myApp = App(WINDOW_TITLE, WIDTH, HEIGHT, background_color = BACKGROUND_COLOR)
    game_grid = Grid(myApp.window, ROWS, COLS)

    while myApp.isRunning:
        game_grid.update(myApp.canvas)
        sleep(0.1)
