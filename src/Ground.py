import pygame.rect

class Ground:
    # ground will have a x,y, width, and height.
    # this will be a rectangle and will only be used to stop the player from falling
    def __init__(self, x=-10, y=550, width=120, height=50):
        # position
        self.x = x
        self.y = y

        # size
        self.width = width
        self.height = height

    # render the ground
    def render(self, rendered_screen, camera):
        # apply the camera transform
        draw_x, draw_y = camera.apply_camera_transform(self)

        # draw the ground
        pygame.draw.rect(
            rendered_screen, (255, 255, 255), (draw_x, draw_y, self.width, self.height)
        )

    def update(self):
        pass

    pass