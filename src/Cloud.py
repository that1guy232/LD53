import pygame
import random


class Cloud:
    def __init__(self, x, y, spr=random.randint(1, 3), rotation=0):
        self.x = x
        self.y = y
        self.spr = spr
        self.rotation = rotation

        # scale from .5 to 3x the original size
        self.scale = random.uniform(0.5, 3)

        self.sprite = pygame.image.load("assets/cloud_" + str(self.spr) + ".png")

        # scale the sprite
        self.sprite = pygame.transform.scale(
            self.sprite,
            (
                int(self.sprite.get_width() * self.scale),
                int(self.sprite.get_height() * self.scale),
            ),
        )
        # rotate the sprite
        self.sprite = pygame.transform.rotate(self.sprite, self.rotation)

        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()

    # render the cloud
    def render(self, rendered_screen, camera):
        # apply the camera transform
        draw_x, draw_y = camera.apply_camera_transform(self)
        # draw the cloud
        rendered_screen.blit(self.sprite, (draw_x, draw_y))

    pass
