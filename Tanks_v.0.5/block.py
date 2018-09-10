from pygame import *


class Block(sprite.Sprite):

    def __init__(self, topleft, filename, destructibility, health_point=None):
        sprite.Sprite.__init__(self)

        self.filename = filename

        self.image = image.load(self.filename)

        self.rect = self.image.get_rect()

        self.rect.topleft = topleft

        self.destructibility = destructibility

        if self.destructibility:

            self.health = health_point

    def get_topleft(self):

        return self.rect.topleft
    
    def set_image(self,topleft, filename):

        self.filename = filename

        self.image = image.load(self.filename)

        self.rect = self.image.get_rect()

        self.rect.topleft = topleft


class Base(Block):

    def __init__(self, topleft, filename, destructibility, health_point=None):
        Block.__init__(self, topleft, filename, destructibility, health_point)

        self.end_lvl = True
