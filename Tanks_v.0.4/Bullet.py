
import sys, os, math

import pygame

import settings


# direction constants
(DIR_UP, DIR_DOWN, DIR_RIGHT, DIR_LEFT) = range(4)

class Bullet(pygame.sprite.Sprite):

    def __init__(self,center,direction,filename = settings.PLAYER_BULLET):

        pygame.sprite.Sprite.__init__(self)

        self.filename = filename

        self.image = self.image2 = pygame.image.load(self.filename)

        self.rect = self.image.get_rect()

        self.rect.center = center

        self.speed = 5

        self.direction = direction


    def move (self):

        if self.direction == DIR_UP:

            self.image = pygame.transform.rotate(self.image2,90)

            self.rect.top -= self.speed

        if self.direction == DIR_RIGHT:

            self.rect.left += self.speed

        if self.direction == DIR_LEFT:

            self.image = pygame.transform.flip(self.image2, 1, 0)

            self.rect.left -= self.speed

        if self.direction == DIR_DOWN:

            self.image = pygame.transform.rotate(self.image2,270)
            
            self.rect.top += self.speed
