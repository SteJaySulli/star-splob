import pygame
from math import sin, cos, pi
class Sprite(pygame.sprite.Sprite):
    def __init__(self, engine, states):
        super().__init__()
        self.engine = engine
        
        self.state = "default" # The sprite state
        self.images = {} # Image dictionary; key is state, content is an array of surfaces (frames)
        self.rects = {} # Rects keyed by state (to match self.images)
        self.frameCount = {} # Frame count keyed by states (to match self.images)
        self.frame = 0 # The current frame to display
        
        self.x = 0 # x position of sprite centre
        self.y = 0 # y position of sprite centre
        self.my = 0.0 # Vertical movement direction
        self.mx = 0.0 # Horizontal movement direction
        self.vy = 0.0 # Vertical movement velocity
        self.vx = 0.0 # Horizontal movement velocity
        self.vmax = 10.0
        self.accel = 70.0 # Pi divisor for acceleration calculation

        self.centre_on = False

        # How far off each screen edge the sprite can be before it wraps around
        self.space = {
            "left": 0,
            "right": 0,
            "top": 0,
            "bottom": 0
        }

        self.health = 100
        self.lives = 5
        self.energy = 0
        self.shield = 0
        # Build state details
        for stateName in states.keys():
            print("Loading state '{}'".format(stateName))
            self.loadImages(stateName, states[stateName]["frames"])
            if "default" in states[stateName].keys() and states[stateName]["default"]:
                self.state = stateName
        
        # Initialise to default state
        self.setState(self.state)
        self.animate()
    
    def loadImages(self, stateName, images):
        self.images[stateName] = []
        self.rects[stateName] = []
        self.frameCount[stateName] = 0
        for imageFile in images:
            image = pygame.image.load(imageFile).convert_alpha()
            self.images[stateName].append(image)
            self.rects[stateName].append(image.get_rect())
        self.frameCount[stateName] = len(self.images[stateName])

    def movement(self):
        # If no key pressed, we decelerate, otherwise we accelerate in the appropriate direction

        if self.my == 0.0:
            if self.vy > 0.0:
                self.vy -= pi / self.accel
            elif self.vy < 0.0:
                self.vy += pi / self.accel
            if abs(self.vy) <= pi / self.accel:
                self.vy = 0
        elif self.my * pi < self.vy:
            self.vy += pi / self.accel * self.my
        elif self.my * pi > self.vy:
            self.vy += pi / self.accel * self.my
        self.y += self.vy * self.vmax

        if self.y  > self.engine.screenHeight + self.space["bottom"]:
            self.onPastYEdge()
            self.y = 0
        if self.y < 0 - self.space["top"]:
            self.onPastYEdge()
            self.y = self.engine.screenHeight

        if not self.centre_on:
            if self.mx == 0.0:
                if self.vx > 0.0:
                    self.vx -= pi / self.accel
                elif self.vx < 0.0:
                    self.vx += pi / self.accel
                if abs(self.vx) <= pi / self.accel:
                    self.vx = 0
            elif self.mx * pi < self.vx:
                self.vx += pi / self.accel * self.mx
            elif self.mx * pi > self.vx:
                self.vx += pi / self.accel * self.mx
            self.x += self.vx * self.vmax

            if self.x  > self.engine.screenWidth + self.space["right"]:
                self.onPastXEdge()
                self.x = 0
            if self.x < 0 - self.space["left"]:
                self.onPastXEdge()
                self.x = self.engine.screenWidth



    def animate(self):
        self.image = self.images[self.state][self.frame]
        self.rect = self.rects[self.state][self.frame]
        self.movement()
        self.rect.x = self.x - self.rect.w / 2
        self.rect.y = self.y - self.rect.h / 2
        if self.frameCount[self.state] > 1:
            if self.frame + 1 >= self.frameCount[self.state]:
                self.frame = 0
            else:
                self.frame += 1
    
    
    def setState(self, state = None):
        if state in self.images.keys():
            if state != self.state:
                self.onStateEnd(self.state)
                self.frame = 0
                self.state = state
                self.onStateBegin(state)

    def onStateBegin(self, state):
        # Override this to provide a hook for when state changes
        pass
    def onStateEnd(self, state):
        # Override this to provide a hook for when state changes
        pass

    def onPastXEdge(self):
        pass
    def onPastYEdge(self):
        pass

    def update(self):
        self.animate()

