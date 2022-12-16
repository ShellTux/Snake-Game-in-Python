from tkinter import Canvas
from itertools import pairwise
from Vector import Vector
from colorsys import hls_to_rgb

rgb_to_hex = lambda rgb: '#%02x%02x%02x' % rgb

class Snake:
    def __init__(self, row: int, col: int, *, head_color: str = 'red', body_color: str = 'black'):
        self.body = [Vector(row, col)]
        self.head_color = head_color
        self.body_color = body_color
        self.velocity = Vector(0, 0)
        self.moves_buffer: list[Vector] = []
        self.bolus: list[int] = []
        self.steps: int = 0

    def change_direction(self, key_event):
        map_direction_to_velocity = {
                # Up
                'w': Vector(-1, 0),
                'Up': Vector(-1, 0),
                # Left
                'a': Vector(0, -1),
                'Left': Vector(0, -1),
                # Down
                's': Vector(1, 0),
                'Down': Vector(1, 0),
                # Right
                'd': Vector(0, 1),
                'Right': Vector(0, 1)
                }

        # If dictionary doesn't have key for the key press then exit function
        if map_direction_to_velocity.get(key_event.char):
            new_velocity = map_direction_to_velocity[key_event.char]
        elif map_direction_to_velocity.get(key_event.keysym):
            new_velocity = map_direction_to_velocity[key_event.keysym]
        else:
            return
        
        # First check if velocity is not None and
        # If current velocity and new velocity go in different directions
        # Then when we multiply each component it will give -1, so we will
        # Skip self.velocity update because both velocities go in opposite directions, which is not valid
        if self.velocity == -new_velocity:
            return

        self.moves_buffer.append(new_velocity)

    def move(self):
        if len(self.moves_buffer) > 0:
            self.velocity = self.moves_buffer.pop(0)

        for segment, previous_segment in pairwise(self.body[::-1]):
            segment.x = previous_segment.x
            segment.y = previous_segment.y

        # Move snake head by self.velocity
        self.body[0] += self.velocity

        if self.velocity != Vector(0, 0):
            self.steps += 1

    def show(self, canvas: Canvas, dw: float, dh: float):
        for i in range(len(self.body) - 1, -1, -1):
            fill_color = self.head_color if i == 0 else rgb_to_hex(tuple(map(lambda x: int(x * 255), hls_to_rgb(1 / i, 0.5, 1)))) #self.body_color 
            width_scale: float = max(1 - i * 0.05, 0.85)
            segment_row, segment_column = self.body[i]
            segment_x = dw * (segment_column + (1 - width_scale) * .5)
            segment_y = dh * (segment_row    + (1 - width_scale) * .5)
            canvas.create_rectangle(
                    segment_x,
                    segment_y,
                    segment_x + dw * width_scale,
                    segment_y + dh * width_scale,
                    fill = fill_color,
                    )
            if i in self.bolus:
                # Constrain between 0.6 and 1
                width_scale: float = max(2**.5 - i * 0.08, 0.1)
                segment_x = dw * (segment_column + (1 - width_scale) * .5)
                segment_y = dh * (segment_row    + (1 - width_scale) * .5)
                canvas.create_oval(
                        segment_x,
                        segment_y,
                        segment_x + dw * width_scale,
                        segment_y + dh * width_scale,
                        fill = 'green',#fill_color,
                        outline = 'white'
                        )

        for i in range(len(self.bolus)):
            self.bolus[i] += 1

        self.bolus = list(filter(lambda bolus: bolus < len(self.body), self.bolus))

    def grow(self):
        previous_segment = self.body[-1]
        self.body.append(Vector(previous_segment.x, previous_segment.y))
