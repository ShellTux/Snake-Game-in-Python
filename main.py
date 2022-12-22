#!/usr/bin/env python3
from tkinter import Tk, Canvas, Label, Checkbutton, OptionMenu, Scale
from tkinter import DoubleVar, StringVar, BooleanVar, HORIZONTAL
from colorsys import hls_to_rgb
from time import sleep
from Grid import Grid
from Robot import Robot, strategies
from PIL import Image

ROWS = COLS = 30
WIDTH = 800
WINDOW_TITLE: str = 'Snake Game'
BACKGROUND_COLOR: str = 'black'
HIGHSCORE_FILE_PATH: str = 'highscore.txt'

BACKGROUND_IMAGE = Image.new('RGB', (WIDTH, WIDTH), color = 'black')

# Autoplay branch fingerprint

font = lambda *, family = 'Helvetica', size = 30, style = 'bold': f'{family} {size} {style}'
rgb_to_hex = lambda rgb: '#%02x%02x%02x' % rgb

class App:
    def __init__(self, title: str, canvas_width: int, *, background_color: str = BACKGROUND_COLOR, fps: int = 10, highscore_file_path: str = HIGHSCORE_FILE_PATH):
        # Window setup
        window = Tk()
        window.title(title)
        window.resizable(False, False)
        self.window = window

        # Some other variables
        # Width and height of the canvas
        self.width = self.height = canvas_width
        self.highscore_file_path: str = highscore_file_path
        self.elements_to_delete = []
        self.is_robot_playing: BooleanVar = BooleanVar()
        self.strategy: StringVar = StringVar()
        self.fps: DoubleVar = DoubleVar()
        self.fps.set(120)

        # Label Setup
        highscore_label = Label(window, text = f'Score: 0 | Highscore: 0', font = font(size = 30))
        self.highscore_label = highscore_label

        # Canvas setup
        canvas = Canvas(window, width = canvas_width, height = canvas_width, bg = background_color)
        self.canvas: Canvas = canvas

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
                variable = self.is_robot_playing,
                state = 'normal',
                )
        # Turn on the state of check button
        cpu_check_button.select()
        self.cpu_check_button: Checkbutton = cpu_check_button

        # Robot Strategies option menu setup
        # Set choice to be first element on strategies
        self.strategy.set(strategies[0])
        strategies_menu: OptionMenu = OptionMenu(window, self.strategy, *strategies)

        # Scale/Slide element
        fps_slider: Scale = Scale(window, {
            'variable': self.fps,
            'from_': 1,
            'to': 240,
            'orient' : HORIZONTAL
            })
        self.fps_slider: Scale = fps_slider

        # Packing all elements into the window
        # Order is crucial
        highscore_label.pack()
        canvas.pack()
        steps_label.pack()
        cpu_check_button.pack()
        strategies_menu.pack()
        fps_slider.pack()

    def update_steps_label(self, steps: int):
        self.steps_label.config(text = f'Number of Steps: {steps}')

    def update_highscore_label(self, score: int, highscore: int):
        self.highscore_label.config(text = f'Score: {score} | Highscore: {highscore}')

    def create_grid(self, rows: int, cols: int):
        self.grid = Grid(rows, cols, self.highscore_file_path, image_width = min(self.width, self.height) // cols) # quick temporary fix for image_width
        self.update_highscore_label(self.grid.score, self.grid.highscore)
        # Draw grid on the canvas
        dw = dh = self.width / self.grid.rows
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
        if self.is_robot_playing.get():
            self.robot = Robot(self.grid, self.strategy.get())
        else:
            self.window.bind('<Key>', self.grid.snake.change_direction)

    def update(self):
        self.canvas.delete(*self.elements_to_delete)
        is_running = self.grid.update(self.canvas, self.update_highscore_label)
        if self.is_robot_playing.get():
            self.robot.play()
        self.update_steps_label(self.grid.snake.steps)
        self.show()
        return is_running

    def show(self):
        self.elements_to_delete = []
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        dw: float = width / self.grid.cols
        dh: float = height / self.grid.rows

        # Show food
        food_x = self.grid.food.y * dw
        food_y = self.grid.food.x * dh
        id_ = self.canvas.create_image(food_x, food_y, image = self.grid.food_image, anchor = 'nw')
        self.elements_to_delete.append(id_)

        # Show snake
        for i in range(len(self.grid.snake.body) - 1, -1, -1):
            fill_color = self.grid.snake.head_color if i == 0 else rgb_to_hex(tuple(map(lambda x: int(x * 255), hls_to_rgb(1 / i, 0.5, 1)))) #self.grid.snake.body_color 
            width_scale: float = max(1 - i * 0.05, 0.85)
            segment_row, segment_column = self.grid.snake.body[i]
            segment_x = dw * (segment_column + (1 - width_scale) * .5)
            segment_y = dh * (segment_row    + (1 - width_scale) * .5)
            id_ = self.canvas.create_rectangle(
                    segment_x,
                    segment_y,
                    segment_x + dw * width_scale,
                    segment_y + dh * width_scale,
                    fill = fill_color,
                    )
            self.elements_to_delete.append(id_)
            if i in self.grid.snake.bolus:
                # Constrain between 0.6 and 1
                width_scale: float = max(2**.5 - i * 0.08, 0.1)
                segment_x = dw * (segment_column + (1 - width_scale) * .5)
                segment_y = dh * (segment_row    + (1 - width_scale) * .5)
                id_ = self.canvas.create_oval(
                        segment_x,
                        segment_y,
                        segment_x + dw * width_scale,
                        segment_y + dh * width_scale,
                        fill = 'green',#fill_color,
                        outline = 'white'
                        )
                self.elements_to_delete.append(id_)

        for i in range(len(self.grid.snake.bolus)):
            self.grid.snake.bolus[i] += 1

        self.grid.snake.bolus = list(filter(lambda bolus: bolus < len(self.grid.snake.body), self.grid.snake.bolus))
        self.canvas.update()
        self.canvas.delete(*self.elements_to_delete)

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
            # Create Grid
            self.create_grid(ROWS, COLS)
            while self.update():
                fps: float = self.fps.get()
                if fps < 240:
                    sleep(1 / fps)

            if self.grid.win:
                print('You won!!!')
            else:
                print('You Lost!!!')
            self.save_highscore()
            # Re-enable cpu check button
            self.cpu_check_button.config(state = 'normal')

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

        self.canvas.bind('<ButtonRelease>', lambda event: press_menu(event))
        self.canvas.bind('<Motion>', move_cursor)
        self.canvas.mainloop()
        self.canvas.unbind('<ButtonRelease>')
        self.canvas.unbind('<Motion>')


if __name__ == '__main__':
    myApp = App(WINDOW_TITLE, WIDTH, background_color = BACKGROUND_COLOR, fps = 120)

    myApp.main_loop()
