from Compass import Compass
from Collectable import Collectable
from Cloud import Cloud
from Ground import Ground
from Camera import Camera
from Rope import Rope
from CollectionZone import CollectionZone
from Player import Player


import pygame
import random


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

        # collect sound
        self.collect_sound = pygame.mixer.Sound(
            "assets/8_BIT_Pickup_BY_jalastram/SFX_Pickup_08.wav"
        )
        pygame.mixer.music.load("assets/DST-RAILJet-LongSeamlessLoop.ogg")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)

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
<<<<<<< HEAD
        while len(self.grounds) < 50:
=======
        while len(self.grounds) < 100:
>>>>>>> 0c69e3ee2c2ee237562533e9393ad796a243ffb2
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
                    # does it collide with the player?
                    if self.check_collision(new_ground, self.player):
                        self.grounds.remove(new_ground)
                        break

        self.player_rope = Rope(self.player, 4, 10)


    # player collision response
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
            player.velocity.x *= -0.4  # Reverse the x-velocity
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
            if len(self.collectables) < 30:
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

                    # play the collect sound
                    self.collect_sound.play()
                    

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
