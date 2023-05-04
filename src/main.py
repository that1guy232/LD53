
from Game import Game

import pygame

import pygame
import asyncio


# main function
async def main():
    # initialize pygame
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    # create a game object
    game = Game()


    while game.running:
        game.clock.tick(60)
        game.handle_events()
        game.update()
        game.render()
        game.draw()

        # set the title of the window to are fps
        pygame.display.set_caption(f"FPS: {game.clock.get_fps():.2f}")

        await asyncio.sleep(0)



if __name__ == "__main__":
    asyncio.run(main())
