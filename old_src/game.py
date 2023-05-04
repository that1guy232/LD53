import pygame
import random
import math

DEBUG = False


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


class CollectionZone:
    def __init__(self, x, y):
        self.sprite = pygame.image.load("collection_zone.png")
        # scale the sprite
        # self.sprite = pygame.transform.scale(self.sprite, (100, 100))
        self.x = x
        self.y = y

        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()

        self.collider = Collider(self.x, self.y, self.width, self.height)

    def render(self, rendered_screen, camera):
        draw_x, draw_y = camera.apply_camera_transform(self)
        # render the collider
        if DEBUG:
            self.collider.render(rendered_screen, camera)
        rendered_screen.blit(self.sprite, (draw_x, draw_y))

    pass


class Collectable:
    def __init__(self, x, y, width=32, height=32):
        self.x = x
        self.y = y
        self.old_y = y
        self.sprite = pygame.image.load("collect.png")
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


class Camera:
    def __init__(self, anchor):
        # position
        self.x = 0
        self.y = 0

        self.width = 800
        self.height = 600

        # lerp speed (between 0 and 1)
        self.lerp_speed = 0.25

        self.anchor = anchor

    def lerp(self, start, end, speed):
        return start + (end - start) * speed

    def update(self):
        # update the camera position based on the anchor

        target_x = self.anchor.x - self.width / 2
        target_y = self.anchor.y - self.height / 2
        # apply the lerp function to smoothly move the camera
        self.x = self.lerp(self.x, target_x, self.lerp_speed)
        self.y = self.lerp(self.y, target_y, self.lerp_speed)

        pass

    def apply_camera_transform(self, object):
        obj_x, obj_y = object.x, object.y

        # apply the camera transform
        obj_x -= self.x
        obj_y -= self.y

        # return the transfrom
        return obj_x, obj_y

    pass


class Compass:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.original_sprite = pygame.image.load("arrow.png")
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
        if DEBUG:
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


class Cloud:
    def __init__(self, x, y, spr=random.randint(1, 3), rotation=0):
        self.x = x
        self.y = y
        self.spr = spr
        self.rotation = rotation

        # scale from .5 to 3x the original size
        self.scale = random.uniform(0.5, 3)

        self.sprite = pygame.image.load("cloud_" + str(self.spr) + ".png")

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


class Game:
    def __init__(self):
        # create a screen object
        self.screen = pygame.display.set_mode((800, 600))
        # set the title of the window
        pygame.display.set_caption("My Game")
        self.font = pygame.font.SysFont("Arial", 30)

        # create a clock object
        self.clock = pygame.time.Clock()

        self.score = 0
        self.score_multiplier = 1
        self.last_score_time = 0

        # 10 clouds in a grid
        self.clouds = []
        for i in range(40):
            self.clouds.append(
                Cloud(
                    random.randint(-800 * 4, 1600 * 4),
                    random.randint(-600 * 4, 1200 * 4),
                    random.randint(1, 3),
                    # random rotation
                    random.randint(0, 360),
                )
            )

        # set the running variable to True
        self.running = True

        self.rendered_screen = pygame.Surface((800, 600))

        self.player = Player()

        self.ground = Ground()

        self.camera = Camera(self.player)

        # compass
        self.compass = Compass(30, 20)

        self.collectables = []
        # add 1 collectable
        self.collectables.append(Collectable(200, 200))

        # a list of all grounds, so we can loop through them and deal with them all at once
        self.grounds = [self.ground]
        # collection zone
        self.collection_zone = CollectionZone(0, 450)
        # while we have less than x grounds
        while len(self.grounds) < 25:
            # create a new ground
            new_ground = Ground(
                random.randint(-800 * 4, 1600 * 4),
                random.randint(0, 600 * 4),
                random.randint(100, 400),
                random.randint(100, 400),
            )
            # add it to the list of grounds
            self.grounds.append(new_ground)
            # does it collide with any other grounds? or the collection zone?
            for ground in self.grounds:
                if new_ground != ground:
                    if self.check_collision(new_ground, ground):
                        # remove the ground
                        self.grounds.remove(new_ground)
                        break
                    if self.check_collision(new_ground, self.collection_zone):
                        self.grounds.remove(new_ground)

                        break

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

    def collision_response(self, ground, player):
        # Calculate the collision depth on each axis
        depth_x = min(
            ground.x + ground.width - player.x,
            player.x + player.width - ground.x,
        )
        depth_y = min(
            ground.y + ground.height - player.y,
            player.y + player.height - ground.y,
        )

        # Resolve the collision based on the smallest depth
        if depth_x < depth_y:
            if player.x + player.width / 2 < ground.x + ground.width / 2:
                player.x -= depth_x
            else:
                player.x += depth_x
            player.velocity.x *= -1  # Reverse the x-velocity
        else:
            if player.y + player.height / 2 < ground.y + ground.height / 2:
                player.y -= depth_y
                player.velocity.y = 0
                player.grounded = True
            else:
                player.y += depth_y
                player.velocity.y = 0

    def update(self):
        # print the player time in min and seconds, get the time in ms from self.clock.get_time()

        # if we took longer than 10 seconds sense are last score, reset the multiplier to 1
        # print(pygame.time.get_ticks() - self.last_score_time)
        rest_time = 10000
        if pygame.time.get_ticks() - self.last_score_time > rest_time:
            # print("reset")
            self.score_multiplier = 1

        self.player.update(self.clock.get_time())

        self.player_rope.update(self.clock.get_time())

        # update the collectables
        for self.collectable in self.collectables:
            self.collectable.update(self.clock.get_time())

        # update the camera
        self.camera.update()

        # check for collisions between the player and the ground
        for self.ground in self.grounds:
            if self.check_collision(self.ground, self.player):
                self.collision_response(self.ground, self.player)
            # if we have less than 10 collectables, add another one
            if len(self.collectables) < 20:
                # 2 screen width on either side of the player
                r_x = random.randint(-800 * 4, 1600 * 4)
                # the screen height is 600, so we want the collectable to be above the screen se get a positive random number from 600 to 4 times the screen height, than we flip so it's at the top of the screen
                r_y = -random.randint(600, 600 * 4)
                # flip the y position so it's above the screen
                r_y = r_y
                self.collectables.append(Collectable(r_x, r_y))

            # check for collisions between the ground and the collectables
            for self.collectable in self.collectables:
                if self.check_collision(self.ground, self.collectable):
                    self.collectable.y = self.ground.y - self.collectable.height
                    self.collectable.y_velocity = 0
                    self.collectable.grounded = True

                # if the collectable's y position way below the ground, delete it
                if self.collectable.y > self.screen.get_height() * 4:
                    self.collectables.remove(self.collectable)
                # check for collisions between the player rope and the collectables
                if self.check_collision(self.player_rope.collider, self.collectable):
                    # print("player rope collided with collectable")
                    # allow the player to pick up the collectable
                    self.player.on_over_collectable(self.collectable, self.player_rope)
                    self.player.trying_to_attach = False
                    pass

                # check for collisions between the collection zone and the collectables
                if self.check_collision(self.collection_zone, self.collectable):
                    print("collectable in collection zone")
                    # remove the collectable
                    self.collectables.remove(self.collectable)
                    # make sure if it's connected to the player, it's not anymore
                    if self.player.connected_collectable:
                        self.player.connected_collectable = False

                        # set are last score time because we just scored!
                        self.last_score_time = pygame.time.get_ticks()
                        # increase the score
                        self.score += 1 * self.score_multiplier
                        # increase the score multiplier
                        self.score_multiplier += 0.25

                    # allow the player to pick up the collectable
                    # self.player.on_over_collectable(self.collectable, self.player_rope)
                    # self.player.trying_to_attach = False

        # update the compass
        # if the rope is not attached to anything, update the compass
        if not self.player.connected_collectable:
            self.compass.update(self.clock.get_time(), self.player, self.collectables)
        else:  # point towards the collection zone
            self.compass.update(
                self.clock.get_time(), self.player, [self.collection_zone]
            )
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
        self.rendered_screen.fill((125, 200, 255))

        # render the clouds
        for self.cloud in self.clouds:
            self.cloud.render(self.rendered_screen, self.camera)

        # render the player
        self.player.render(self.rendered_screen, self.camera)
        self.player_rope.render(self.rendered_screen, self.camera)

        # render the collectables
        for self.collectable in self.collectables:
            self.collectable.render(self.rendered_screen, self.camera)

        # render the ground
        for self.ground in self.grounds:
            self.ground.render(self.rendered_screen, self.camera)

        # render the collection zone
        self.collection_zone.render(self.rendered_screen, self.camera)

        self.compass.render(self.rendered_screen, self.camera)

        time_ms = pygame.time.get_ticks()

        time_seconds = int(time_ms / 1000)
        # how long in minutes
        time_minutes = int(time_ms / 1000 / 60)

        # render the time the player has been playing at the top of the screen (00:00)
        self.rendered_screen.blit(
            self.font.render(
                str(time_minutes).zfill(2) + ":" + str(time_seconds % 60).zfill(2),
                True,
                (0, 0, 0),
            ),
            (self.screen.get_width() / 2 - 20, 10),
        )

        # render the score to the left of the screen
        self.rendered_screen.blit(
            self.font.render("Score: " + str(self.score), True, (0, 0, 0)),
            (10, 10),
        )

        # render the score multi next to the score
        # print(self.score_multiplier)
        r = self.font.render("x" + str(self.score_multiplier), True, (0, 0, 0))
        # scale it down
        r = pygame.transform.scale(r, (int(r.get_width() / 2), int(r.get_height() / 2)))
        self.rendered_screen.blit(
            r,
            (10 + self.font.size("Score: " + str(self.score))[0], 6),
        )

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
