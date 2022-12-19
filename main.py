#!/usr/bin/env python3
from tkinter import Tk, Canvas, Label, Checkbutton, OptionMenu, StringVar
from time import sleep
from Grid import Grid
from Robot import Robot, strategies

ROWS = COLS = 10
WIDTH = 800
WINDOW_TITLE: str = 'Snake Game'
BACKGROUND_COLOR: str = 'black'
HIGHSCORE_FILE_PATH: str = 'highscore.txt'

# Autoplay branch fingerprint

font = lambda *, family = 'Helvetica', size = 30, style = 'bold': f'{family} {size} {style}'

class App:
    def __init__(self, title: str, canvas_width: int, *, background_color: str = BACKGROUND_COLOR, fps: int = 10, highscore_file_path: str = HIGHSCORE_FILE_PATH):
        # Window setup
        window = Tk()
        window.title(title)
        window.resizable(False, False)
        self.window = window
        # Label Setup
        highscore_label = Label(window, text = f'Score: 0 | Highscore: 0', font = font(size = 30))
        self.highscore_label = highscore_label
        # Canvas setup
        canvas = Canvas(window, width = canvas_width, height = canvas_width, bg = background_color)
        self.canvas = canvas
        # Steps label setup
        steps_label: Label = Label(window, text = 'Movements: 0', font = font())
        self.steps_label = steps_label
        # Check button setup
        cpu_check_button: Checkbutton = Checkbutton(
                window,
                text = 'CPU', 
                font = font(size = 15),
                onvalue = True,
                offvalue = False,
                state = 'normal'
                )
        # Turn on the state of check button
        cpu_check_button.select()
        self.cpu_check_button: Checkbutton = cpu_check_button
        # Robot Strategies option menu setup
        strategies_menu: OptionMenu = OptionMenu(window, StringVar(window), *strategies)

        # Width and height of the canvas
        self.width = self.height = canvas_width
        self.fps: int = fps
        self.highscore_file_path: str = highscore_file_path
        self.is_robot_playing: bool = True
        self.choice: str = ''


        # Packing all elements into the window
        # Order is crucial
        highscore_label.pack()
        canvas.pack()
        steps_label.pack()
        cpu_check_button.pack()
        strategies_menu.pack()

    def update_steps_label(self, steps: int):
        self.steps_label.config(text = f'Number of Steps: {steps}')

    def update_highscore_label(self, score: int, highscore: int):
        self.highscore_label.config(text = f'Score: {score} | Highscore: {highscore}')

    def create_grid(self, rows: int, cols: int):
        self.grid = Grid(rows, cols, self.highscore_file_path, image_width = min(self.width, self.height) // cols) # quick temporary fix for image_width
        self.update_highscore_label(self.grid.score, self.grid.highscore)
        if not self.is_robot_playing:
            self.window.bind('<Key>', self.grid.snake.change_direction)
        else:
            self.robot = Robot(self.grid)

    def update(self):
        self.canvas.delete('all')
        is_running = self.grid.update(self.canvas, self.update_highscore_label)
        self.robot.play(self.grid.came_from_path)
        self.update_steps_label(self.grid.snake.steps)
        self.show()
        return is_running

    def show(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        dw: float = width / self.grid.cols
        dh: float = height / self.grid.rows

        for i in range(self.grid.rows):
            for j in range(self.grid.cols):
                x = j * dw
                y = i * dh
                self.canvas.create_rectangle(
                        x,
                        y,
                        x + dw,
                        y + dh,
                        fill = 'grey',
                        outline = 'white'
                        )
                
        # Showing lines
        for i in range(self.grid.rows):
            self.canvas.create_line(0, dh * i, width, dh * i, fill = 'white')

        # Showing columns
        for j in range(self.grid.cols):
            self.canvas.create_line(dw * j, 0, dw * j, height, fill = 'white')

        # Show food
        food_x = self.grid.food.y * dw
        food_y = self.grid.food.x * dh
        self.canvas.create_image(food_x, food_y, image = self.grid.food_image, anchor = 'nw')

        # Show snake
        self.grid.snake.show(self.canvas, dw, dh)
        self.canvas.update()

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

    def main_loop(self):
        while self.main_menu() != 'Quit':

            # Start playing
            # Disable cpu check button
            self.cpu_check_button.config(state = 'disabled')
            while self.update():
                sleep(1 / self.fps)

            # Lost
            print('You Lose!!!')
            self.save_highscore()
            # myApp.wait_for_quit()

    def main_menu(self):
        menu_entries = (
                'Play',
                'Quit'
                )
        font_size: int = 40
        spacing: int = 100
        font_family: str = font(size = font_size)
        for i, entry in enumerate(menu_entries):
            self.canvas.create_text(self.width * .5, self.height * .5 + i * spacing, text = entry, fill = 'white', font = font_family)


        # Mouse movement callback
        def move_cursor(event):
            # Skip highlight if cursor x position is not between these limits
            if abs(event.x - self.width * .5) > 50:
                return

            for i, entry in enumerate(menu_entries):
                text_y: float = self.height * .5 + i * spacing
                self.canvas.create_text(self.width * .5, text_y, text = entry, font = font_family, 
                                        fill = 'red' if abs(event.y - text_y) < .5 * font_size else 'white'
                                        )

        # Button Release callback
        def press_menu(event):
            choice: str = ''
            for i in range(len(menu_entries)):
                text_y: float = self.height * .5 + i * spacing
                if abs(event.y - text_y) < .5 * font_size:
                    choice = menu_entries[i]

            if choice == '':
                return
            elif choice == 'Play':
                # Exit main loop and proceed to play game in self.main_loop
                self.canvas.quit()
            elif choice == 'Quit':
                exit()

            self.choice = choice

        self.canvas.bind('<ButtonRelease>', lambda event: press_menu(event))
        self.canvas.bind('<Motion>', move_cursor)
        self.canvas.mainloop()
        self.canvas.unbind('<ButtonRelease>')
        self.canvas.unbind('<Motion>')
        return self.choice


if __name__ == '__main__':
    myApp = App(WINDOW_TITLE, WIDTH, background_color = BACKGROUND_COLOR, fps = 120)
    myApp.create_grid(ROWS, COLS)

    myApp.main_loop()
