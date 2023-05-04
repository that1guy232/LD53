import pygame

from Collider import Collider


class CollectionZone:
    def __init__(self, x, y):
        self.sprite = pygame.image.load("assets/collection_zone.png")
        # scale the sprite
        # self.sprite = pygame.transform.scale(self.sprite, (100, 100))
        self.x = x
        self.y = y

        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()

        self.collider = Collider(self.x, self.y, self.width, self.height)

    def render(self, rendered_screen, camera):
        draw_x, draw_y = camera.apply_camera_transform(self)

        rendered_screen.blit(self.sprite, (draw_x, draw_y))

    pass
