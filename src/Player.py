import pygame
import random


class Player:
    def __init__(self):
        # position
        self.x = 300
        self.y = 350

        # load the drone sprite
        self.sprite = pygame.image.load("assets\drone.png")

        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()

        self.gravity = 0.000
        self.wind = 0.0000
        self.friction = 0.000
        self.movement_speed = 0.0007

        self.velocity = pygame.math.Vector2(0, 0)
        self.grounded = False

        # a variable to keep track of weather the player is trying to attack a collectable to the rope or not
        self.trying_to_attach = False
        self.attach_detach_cooldown = 500  # in milliseconds
        self.time_since_last_attach_detach = 0  # in milliseconds
        self.connected_collectable = False

    # render the player
    def render(self, rendered_screen, camera):
        # apply the camera transform
        draw_x, draw_y = camera.apply_camera_transform(self)
        # draw the player
        # pygame.draw.rect(
        #     rendered_screen, (255, 255, 255), (draw_x, draw_y, self.width, self.height)
        # )

        # draw the player sprite
        rendered_screen.blit(self.sprite, (draw_x, draw_y))

    def update(self, delta_time):
        if not self.grounded:
            # Apply gravity to velocity
            self.velocity.y += self.gravity * delta_time

            # Apply wind to x_velocity
            self.velocity.x += random.uniform(-self.wind, self.wind) * delta_time

            # Apply friction to x_velocity
            if self.velocity.x > 0:
                self.velocity.x -= self.friction * delta_time
                if self.velocity.x < 0:
                    self.velocity.x = 0

            if self.velocity.x < 0:
                self.velocity.x += self.friction * delta_time
                if self.velocity.x > 0:
                    self.velocity.x = 0

            # Apply velocity to the player
            self.x += self.velocity.x * delta_time
            self.y += self.velocity.y * delta_time

        # Update the timer for attach/detach actions
        self.time_since_last_attach_detach += delta_time

    def handle_events(self, delta_time):
        keys = pygame.key.get_pressed()

        # w and s to control vertical movement
        if keys[pygame.K_w]:
            self.velocity.y -= self.movement_speed * delta_time
            # print(self.velocity.y)
            if self.grounded:
                self.grounded = False
                self.velocity.x = 0

        if keys[pygame.K_s]:
            self.velocity.y += self.movement_speed * delta_time

        # a and d to control horizontal movement
        if keys[pygame.K_a]:
            self.velocity.x -= self.movement_speed * delta_time

        if keys[pygame.K_d]:
            self.velocity.x += self.movement_speed * delta_time

        # if the E key is pressed and enough time has passed since the last attach/detach action
        if (
            keys[pygame.K_e]
            and self.time_since_last_attach_detach >= self.attach_detach_cooldown
        ):
            # if the player is not already trying to attach a collectable to the rope
            if not self.trying_to_attach:
                # set the trying_to_attach variable to True
                self.trying_to_attach = True
        else:
            self.trying_to_attach = False

        # if the r key is pressed reset the player position
        if keys[pygame.K_r]:
            self.x = 300
            self.y = 350
            self.velocity.x = 0
            self.velocity.y = 0
            self.grounded = False

    def on_over_collectable(self, collectable, rope):
        # if the player has pressed the button to pick up the collectable
        if self.trying_to_attach:
            # If we are already attached to a collectable
            if collectable.connected_to:
                # detach the collectable from the rope
                self.connected_collectable = False
                collectable.connected_to = None
                # set the collectable to not grounded
                collectable.grounded = False
                self.trying_to_attach = False
                collectable.velocity.x = self.velocity.x
                collectable.velocity.y = self.velocity.y
                print("detached")
            else:
                # attach the collectable to the rope
                rope.attach_collectable(collectable)
                self.connected_collectable = True
                # set the trying_to_attach variable to False
                self.trying_to_attach = False
                print("attached")

            # Reset the timer for attach/detach actions
            self.time_since_last_attach_detach = 0
        pass
