
import sys

import pygame

import Utility.settings as settings



class GameOver():

    def __init__(self):

        self.bg = pygame.image.load(settings.GAME_OVER).convert_alpha()

        self.n = None

        self.GAME = 2

    def draw(self, screen):

        screen.blit(self.bg, (170, 350))

        pygame.display.update()

    def event(self):

        self.n = None

        for itm in pygame.event.get():

            if itm.type == pygame.QUIT:
                sys.exit(0)
            
            if itm.type == pygame.KEYDOWN and itm.key == pygame.K_ESCAPE:

                self.n = self.GAME

                break
        
        return self.n