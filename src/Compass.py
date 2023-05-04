import pygame
import math


class Compass:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.original_sprite = pygame.image.load("assets/arrow.png")
        self.sprite = self.original_sprite.copy()
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()

    def render(self, rendered_screen, camera):
        draw_x, draw_y = (
            self.x,
            self.y,
        )
        rendered_screen.blit(self.sprite, (draw_x, draw_y))

        # pygame.draw.circle(
        #     rendered_screen,
        #     (255, 255, 255),
        #     (draw_x + self.width // 2, draw_y + self.height // 2),
        #     50,
        #     1,
        # )

    def update(self, delta_time, player, collectables):
        closest_collectable = None
        closest_distance = float("inf")
        for collectable in collectables:
            distance = math.sqrt(
                (player.x - collectable.x) ** 2 + (player.y - collectable.y) ** 2
            )
            if distance < closest_distance:
                closest_collectable = collectable
                closest_distance = distance

        if closest_collectable:
            angle = math.atan2(
                player.y - closest_collectable.y, player.x - closest_collectable.x
            )

            # Rotate the sprite and adjust the anchor point
            self.sprite = pygame.transform.rotate(
                self.original_sprite, -math.degrees(angle) + 90
            )
            self.sprite.get_rect(
                center=self.original_sprite.get_rect(topleft=(self.x, self.y)).center
            )
