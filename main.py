from tkinter import Tk, Canvas

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
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols

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

    def update(self, canvas: Canvas):
        self.show(canvas)
        canvas.update()


if __name__ == '__main__':
    myApp = App(WINDOW_TITLE, WIDTH, HEIGHT, background_color = BACKGROUND_COLOR)
    game_grid = Grid(ROWS, COLS)

    while myApp.isRunning:
        game_grid.update(myApp.canvas)
    # myApp.window.mainloop()
