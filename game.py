import pygame
import random
import math
import asyncio
class Collectable:
    def __init__(self, x, y, width=32, height=32):
        self.x = x
        self.y = y
        # self.y_velocity = 0
        self.sprite = pygame.image.load("collect.png")
        self.width = width
        self.height = height
        self.velocity = pygame.math.Vector2(0, 0)
        self.connected_to = None

        # Add a grounded state and a gravity acceleration
        self.grounded = False
        self.gravity = 0.008

    def render(self, rendered_screen, camera):
        draw_x, draw_y = camera.apply_camera_transform(self)
        # Use a gold color for the circle (R, G, B)
        gold_color = (255, 215, 0)

        # Draw the circle
        pygame.draw.circle(
            rendered_screen,
            gold_color,
            (int(draw_x + self.width / 2), int(draw_y + self.height / 2)),
            int(min(self.width, self.height) / 2),
        )

        # draw the sprite
        rendered_screen.blit(self.sprite, (draw_x, draw_y))

    def update(self, delta_time):
        # Apply gravity
        # if we are not grounded, apply gravity
        if not self.grounded:
            # self.y_velocity += self.gravity * delta_time
            self.velocity.y += self.gravity * delta_time

            # limit the y velocity to 1
            self.velocity.y = min(self.velocity.y, 1)

            # Update position
            self.y += self.velocity.y * delta_time

        # if we are connected to something, move with it
        if self.connected_to:
            self.x = self.connected_to.x
            self.y = self.connected_to.y

        pass


class Camera:
    def __init__(self, anchor):
        # position
        self.x = 0
        self.y = 0

        self.width = 800
        self.height = 600

        self.anchor = anchor

    def update(self):
        # update the camera position based on the anchor
        self.x = self.anchor.x - self.width / 2
        self.y = self.anchor.y - self.height / 2
        pass

    def apply_camera_transform(self, object):
        obj_x, obj_y = object.x, object.y

        # apply the camera transform
        obj_x -= self.x
        obj_y -= self.y

        # return the transfrom
        return obj_x, obj_y

    pass


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


class Ground:
    # ground will have a x,y, width, and height.
    # this will be a rectangle and will only be used to stop the player from falling
    def __init__(self, x=0, y=550, width=800, height=50):
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


class Rope:
    # rope will have a x, y, and length.
    # This will be a line that will be made up of segments
    # the top segment will be attached to the player and the bottom will be able to attach to other objects
    def __init__(self, anchor, segment_lenght=8, segment_count=5):
        self.anchor = anchor
        # position
        self.x = anchor.x
        self.y = anchor.y

        # length
        self.segment_length = segment_lenght
        self.segment_count = segment_count

        # set up a collider x, y, width, height

        # create the rope segments
        self.rope_segments = []
        for i in range(self.segment_count):
            self.rope_segments.append(
                RopeSegment(self.x, self.y + i * self.segment_length, sway_offset=i * 8)
            )
        pass

        # collider around the last rope segment
        self.collder_width = 32
        self.collder_height = 32
        self.collider = Collider(
            self.rope_segments[-1].x - self.collder_width / 2,
            self.rope_segments[-1].y - self.collder_height / 2,
            self.collder_width,
            self.collder_height,
        )

    def render(self, rendered_screen, camera):
        # apply the camera transform
        draw_x, draw_y = camera.apply_camera_transform(self)

        # draw the rope collider wire frame
        self.collider.render(rendered_screen, camera)

        # draw the rope segments
        for segment in self.rope_segments:
            segment.render(rendered_screen, camera)

        pass

    def update(self, delta_time):
        # update the rope position based on the anchor
        self.x = self.anchor.x + self.anchor.width / 2
        self.y = self.anchor.y + self.anchor.height

        # update the rope segments
        for i in range(self.segment_count):
            self.rope_segments[i].x = self.x
            self.rope_segments[i].y = self.y + i * self.segment_length

            if i == 0:
                parent_x, parent_y = self.x, self.y - self.segment_length
            else:
                parent_x, parent_y = (
                    self.rope_segments[i - 1].x,
                    self.rope_segments[i - 1].y,
                )
                self.rope_segments[i].update(parent_x, parent_y, delta_time)

        # update the collider position to keep it around the last rope segment
        self.collider.x = self.rope_segments[-1].x - self.collder_width / 2
        self.collider.y = self.rope_segments[-1].y - self.collder_height / 2

        pass


    def attach_collectable(self, collectable):
        collectable.connected_to = self.rope_segments[-1] 
        pass

    def check_collision(self, obj):
        pass

    def handle_events(self, delta_time):
        pass


class Player:
    def __init__(self):
        # position
        self.x = 300
        self.y = 350

        # load the drone sprite
        self.sprite = pygame.image.load("drone.png")

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
            print(self.velocity.y)
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
        if keys[pygame.K_e] and self.time_since_last_attach_detach >= self.attach_detach_cooldown:
            # if the player is not already trying to attach a collectable to the rope
            if not self.trying_to_attach:
                # set the trying_to_attach variable to True
                self.trying_to_attach = True
        else:
            self.trying_to_attach = False

    def on_over_collectable(self, collectable, rope):
        # if the player has pressed the button to pick up the collectable
        if self.trying_to_attach:
            # If we are already attached to a collectable
            if collectable.connected_to:
                # detach the collectable from the rope
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
                # set the trying_to_attach variable to False
                self.trying_to_attach = False
                print("attached")

            # Reset the timer for attach/detach actions
            self.time_since_last_attach_detach = 0
        pass

class Game:
    def __init__(self):
        # create a screen object
        self.screen = pygame.display.set_mode((800, 600))
        # set the title of the window
        pygame.display.set_caption("My Game")

        # create a clock object
        self.clock = pygame.time.Clock()

        # set the running variable to True
        self.running = True

        self.rendered_screen = pygame.Surface((800, 600))

        self.player = Player()

        self.ground = Ground()

        self.camera = Camera(self.player)

        self.collectables = []
        # add 1 collectable
        self.collectables.append(Collectable(200, 200))

        # a list of all grounds, so we can loop through them and deal with them all at once
        self.grounds = [self.ground]

        self.player_rope = Rope(self.player, 4, 10)

    #     # call the main loop function
    #     self.main_loop()

    # def main_loop(self):
    #     # main loop
    #     while self.running:
    #         # set the framerate
    #         self.clock.tick(60)

    #         # handle events
    #         self.handle_events()

    #         # update
    #         self.update()

    #         # render
    #         self.render()

    #         # draw
    #         self.draw()

    def update(self):
        # update the player
        self.player.update(self.clock.get_time())

        self.player_rope.update(self.clock.get_time())

        # update the collectables
        for self.collectable in self.collectables:
            self.collectable.update(self.clock.get_time())

        # update the camera
        self.camera.update()

        # check for collisions between the player and the ground

        for self.ground in self.grounds:
            # if the player is not grounded, check for collisions between the ground and the player
            if not self.player.grounded:
                if self.check_collision(self.ground, self.player):
                    self.player.y = self.ground.y - self.player.height
                    # set all velocity to 0
                    self.player.velocity.x = 0
                    self.player.velocity.y = 0
                    self.player.grounded = True

            # check for collisions between the ground and the collectables
            for self.collectable in self.collectables:
                if self.check_collision(self.ground, self.collectable):
                    self.collectable.y = self.ground.y - self.collectable.height
                    self.collectable.y_velocity = 0
                    self.collectable.grounded = True

                # check for collisions between the player rope and the collectables
                if self.check_collision(self.player_rope.collider, self.collectable):
                    print("player rope collided with collectable")
                    # allow the player to pick up the collectable
                    self.player.on_over_collectable(self.collectable, self.player_rope)
                    self.player.trying_to_attach = False
                    pass

        pass

    def check_collision(self, obj1, obj2):
        if (
            obj1.x < obj2.x + obj2.width
            and obj1.x + obj1.width > obj2.x
            and obj1.y < obj2.y + obj2.height
            and obj1.y + obj1.height > obj2.y
        ):
            return True
        return False

    def render(self):
        # clear the screen
        self.rendered_screen.fill((0, 0, 0))

        # render the player
        self.player.render(self.rendered_screen, self.camera)
        self.player_rope.render(self.rendered_screen, self.camera)

        # render the collectables
        for self.collectable in self.collectables:
            self.collectable.render(self.rendered_screen, self.camera)

        # render the ground
        for self.ground in self.grounds:
            self.ground.render(self.rendered_screen, self.camera)

        pass

    def draw(self):
        # clear the screen
        self.screen.fill((0, 0, 0))
        # draw the screen
        self.screen.blit(self.rendered_screen, (0, 0))
        # update the display
        pygame.display.flip()

        pass

    def handle_events(self):
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        # handle events for the player
        self.player.handle_events(self.clock.get_time())
