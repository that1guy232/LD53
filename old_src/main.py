import pygame
import asyncio

from game import Game


# main function
async def main():
    # initialize pygame
    pygame.init()
    pygame.font.init()

    # create a game object
    game = Game()


    while game.running:
        game.clock.tick(60)
        game.handle_events()
        game.update()
        game.render()
        game.draw()

        await asyncio.sleep(0)



if __name__ == "__main__":
    asyncio.run(main())
