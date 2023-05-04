import pygame
import math


class RopeSegment:
    # rope segment will have a x, y, and length.
    # This will be a line that will be made up of segments
    # the top segment will be attached to the player and the bottom will be able to attach to other objects
    def __init__(self, x, y, length=8, sway_offset=0):
        # position
        self.x = x
        self.y = y

        self.old_x = x
        self.old_y = y
        self.ax = 0
        self.ay = 0

        # length
        self.length = length

        self.sway_offset = sway_offset

        pass

    # render the rope segment
    def render(self, rendered_screen, camera):
        # apply the camera transform
        draw_x, draw_y = camera.apply_camera_transform(self)

        # draw the rope segment
        pygame.draw.line(
            rendered_screen,
            (255, 255, 255),
            (draw_x, draw_y),
            (draw_x, draw_y + self.length),
        )

    # Modify the RopeSegment update method
    def update(self, parent_x, parent_y, delta_time):
        # Apply gravity
        self.ay += 0.5

        # Verlet integration
        temp_x, temp_y = self.x, self.y
        self.x += (self.x - self.old_x) + self.ax * delta_time**2
        self.y += (self.y - self.old_y) + self.ay * delta_time**2
        self.old_x, self.old_y = temp_x, temp_y
        self.ax, self.ay = 0, 0

        # Constrain the segment to the parent position
        dx, dy = self.x - parent_x, self.y - parent_y
        distance = math.sqrt(dx**2 + dy**2)
        # make sure we do not divide by 0
        if distance == 0:
            distance = 0.0001
        target_x = parent_x - (dx / distance) * self.length
        target_y = parent_y + (dy / distance) * self.length
        self.x = target_x
        self.y = target_y

    pass
