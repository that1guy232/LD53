class Collider:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def render(self, rendered_screen, camera):
        draw_x, draw_y = camera.apply_camera_transform(self)

        # draw the collider
        pygame.draw.rect(
            rendered_screen, (255, 0, 0), (draw_x, draw_y, self.width, self.height)
        )

    def update(self):
        pass

    pass