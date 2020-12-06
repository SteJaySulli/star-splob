import pygame
from engine import Engine
from player_ship import PlayerShip
from star import Star

class GameEngine(Engine):
    def __init__(self,game):
        super().__init__(game, {
            pygame.K_LEFT: "move_left",
            pygame.K_RIGHT: "move_right",
            pygame.K_UP: "move_up",
            pygame.K_DOWN: "move_down",
            pygame.K_SPACE: "fire",
            pygame.K_ESCAPE: "quit"
        })

        self.players = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.all = pygame.sprite.Group()

        self.mx = 0
        self.my = 0

        self.screenWidth, self.screenHeight = self.display.get_size()

        self.player = PlayerShip(self)
        self.player.x = self.screenWidth / 2
        self.player.y = self.screenHeight / 2
        
        self.player.centre_on = True

        for i in range(0,100):
            star = Star(self)
            star.x = self.random(star.space["left"] * -1,self.screenWidth + star.space["left"])
            star.y = self.random(0,self.screenHeight)
            self.stars.add(star)
            self.all.add(star)

        self.velocity = 0
        self.position = 0

        self.players.add(self.player)
        self.all.add(self.player)
        self.done = False
    
    def in__quit(self, down):
        self.done = down
    
    def in__move_up(self, down):
        if down:
            self.player.my = -1.0
        elif self.player.my < 0:
            self.player.my = 0.0
    
    def in__move_down(self, down):
        if down:
            self.player.my = 1.0
        elif self.player.my > 0:
            self.player.my = 0.0
        

    def in__move_left(self, down):
        if down:
            self.player.setState('left')
            for sprite in self.all.sprites():
                sprite.mx = 1
        elif self.player.mx > 0:
            for sprite in self.all.sprites():
                sprite.mx = 0

    def in__move_right(self, down):
        if down:
            self.player.setState('right')
            for sprite in self.all.sprites():
                sprite.mx = -1
        elif self.player.mx < 0:
            for sprite in self.all.sprites():
                sprite.mx = 0

    def in__fire(self):
        pass

    def draw_bar(self, surface, rect, value, bg, fg):
        innerRect = (
            rect[0] +2,
            rect[1] +2,
            float(rect[2] - 4) * float(value) / 100.0,
            rect[3] - 4
        )
        pygame.draw.rect(surface, bg, rect)
        if(innerRect[2] > 0):
            pygame.draw.rect(surface, fg, innerRect)

    def draw_overlay(self):
        surface = pygame.Surface((210,120))
        surface.set_alpha(128)
        surface.fill((255,255,255))
        barTop = 5
        # Draw FPS
        fps = self.fonts[0].render("FPS: {}".format(int(self.clock.get_fps())), 0, (0,0,0))
        surface.blit(fps, (105 - fps.get_rect().w / 2,barTop))

        # Draw Lives
        barTop += 16
        lives = self.fonts[1].render("{} {}".format(self.player.lives, "LIFE" if self.player.lives == 1 else "LIVES"), 0, (0,0,0))
        surface.blit(lives, (105 - lives.get_rect().w / 2,barTop))
        
        # Draw Health
        barTop += 24
        self.draw_bar(surface, (5,barTop,200,20), self.player.health, (0,0,0), (0,255,0) )

        # Draw Shield
        barTop += 24
        self.draw_bar(surface, (5,barTop,200,20), self.player.shield, (0,0,0), (0,192,255) )
        
        # Draw Energy
        barTop += 24
        self.draw_bar(surface, (5,barTop,200,20), self.player.energy, (0,0,0), (255,255,0) )

        self.display.blit(surface, (5, 5))

    def draw(self):
        self.display.fill((0,0,0))
        self.stars.draw(self.display)
        self.enemies.draw(self.display)
        self.players.draw(self.display)
        self.draw_overlay()
        

    def run(self):
        super().run()
        self.players.update()
        self.enemies.update()
        self.stars.update()
        return not self.done