import pygame
from random import Random

class Engine:
    def __init__(self, game, keys = {}):
        self._random = Random()
        self.game = game
        self.clock = game.clock
        self.display = game.display
        self.fonts = game.fonts
        self.keyHandler = {}
        for key in keys.keys():
            fn = "in__" + keys[key]
            if hasattr(self, fn):
                self.keyHandler[key] = getattr(self, fn)

    def random(self,start, end):
        return self._random.randint(start,end)

    def events(self):
        for event in pygame.event.get():
            # Process key press events
            if event.type == pygame.KEYDOWN:
                handler = self.keyHandler.get(event.key)
                if handler != None:
                    handler(True)
            if event.type == pygame.KEYUP:
                handler = self.keyHandler.get(event.key)
                if handler != None:
                    handler(False)

    def draw(self):
        pass

    def run(self):
        self.events()
        self.draw()