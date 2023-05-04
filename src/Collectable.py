import pygame
class Collectable:
    def __init__(self, x, y, width=32, height=32):
        self.x = x
        self.y = y
        self.old_y = y
        self.sprite = pygame.image.load("assets/collect.png")
        self.width = width
        self.height = height
        self.velocity = pygame.math.Vector2(0, 0)
        self.connected_to = None
        self.ground_friction = 0.002

        # Add a grounded state and a gravity acceleration
        self.grounded = False
        self.gravity = 0.00005

    def render(self, rendered_screen, camera):
        draw_x, draw_y = camera.apply_camera_transform(self)
        gold_color = (255, 215, 0)
        pygame.draw.circle(
            rendered_screen,
            gold_color,
            (int(draw_x + self.width / 2), int(draw_y + self.height / 2)),
            int(min(self.width, self.height) / 2),
        )
        rendered_screen.blit(self.sprite, (draw_x, draw_y))

    def update(self, delta_time):
        if not self.grounded:
            self.velocity.y = min(self.velocity.y, 1)
            self.y += self.velocity.y * delta_time

        if self.grounded:
            self.velocity.y = 0

        self.x += self.velocity.x * delta_time

        # friction to the x velocity
        self.velocity.x -= self.velocity.x * self.ground_friction * delta_time

        # if are velocity is less than 0.01, set it to 0
        if abs(self.velocity.x) < 0.05:
            self.velocity.x = 0

        self.velocity.y += self.gravity * delta_time
        if self.velocity.y > 0:
            self.grounded = False

        if self.connected_to:
            self.x = self.connected_to.x
            self.y = self.connected_to.y
            self.x += 0 - self.width / 2
            self.grounded = False

        # if are velocity is less than 0.01, set it to 0
        if abs(self.velocity.x) < 0.05:
            self.velocity.x = 0

        self.velocity.y += self.gravity * delta_time
        if self.velocity.y > 0:
            self.grounded = False

        if self.connected_to:
            self.x = self.connected_to.x
            self.y = self.connected_to.y
            self.x += 0 - self.width / 2
            self.grounded = False