import pygame
from menu_engine import MenuEngine
from game_engine import GameEngine

class Main:
    def __init__(self, *args, **wargs):
        self.width = 0
        self.height = 0
        for key in wargs.keys():
            setattr(self, key, wargs[key])

    def init(self):
        pygame.init()
        # pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.NOFRAME | pygame.HWSURFACE
        self.display = pygame.display.set_mode((self.width, self.height), pygame.NOFRAME )
        pygame.display.set_caption("STAR SPLOB")
        self.clock = pygame.time.Clock()
        self.fonts = []
        for size in [8, 16,16,32,48]:
            self.fonts.append(pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", size))
        pygame.key.set_repeat(1,1)
        return self
    
    def destroy(self):
        pygame.display.quit()
        return self
    
    def run(self):
        game = GameEngine(self)
        while game.run():
            pygame.display.flip()
            self.clock.tick(60)
        self.destroy()
        return self

Main().init().run().destroy()
quit()

