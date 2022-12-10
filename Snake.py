from itertools import pairwise
from tkinter import Tk
from Vector import Vector

class Snake:
    def __init__(self, window: Tk, row: int, col: int, *, head_color: str = 'red', body_color: str = 'grey'):
        self.body = [Vector(row, col)]
        self.head_color = head_color
        self.body_color = body_color
        self.velocity = None
        window.bind('<Key>', self.change_direction)

    def change_direction(self, key_event):
        map_direction_to_velocity = {
                # Up
                'w': Vector(-1, 0),
                # Left
                'a': Vector(0, -1),
                # Down
                's': Vector(1, 0),
                # Right
                'd': Vector(0, 1)
                }

        # If dictionary doesn't have key for the key press then exit function
        if map_direction_to_velocity.get(key_event.char) == None:
            return

        new_velocity = map_direction_to_velocity[key_event.char]
        
        # First check if velocity is not None and
        # If current velocity and new velocity go in different directions
        # Then when we multiply each component it will give -1, so we will
        # Skip self.velocity update because both velocities go in opposite directions, which is not valid
        if self.velocity != None and (
                self.velocity.x * new_velocity.x == -1 or
                self.velocity.y * new_velocity.y == -1
                ):
            return

        self.velocity = new_velocity

    def move(self):
        if self.velocity == None:
            return

        for segment, previous_segment in pairwise(self.body[::-1]):
            segment.x = previous_segment.x
            segment.y = previous_segment.y

        # Move snake head by self.velocity
        self.body[0] += self.velocity 


    def grow(self):
        previous_segment = self.body[-1]
        self.body.append(Vector(previous_segment.x, previous_segment.y))
