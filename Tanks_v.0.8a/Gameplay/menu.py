import sys

import pygame

import Utility.settings as settings


class Button(pygame.sprite.Sprite):

    def __init__(self,topleft,filename,text='555'):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(filename)

        self.rect = self.image.get_rect()

        self.rect.topleft = topleft


    def set_image(self,filename):

        self.filename = filename

        self.image = pygame.image.load(self.filename)

    
    def collidepoint(self,topleft):

        if self.rect.collidepoint(topleft):

            return True

        return False


class Menu():

    def __init__(self):

        self.ID = -1

        self.background = pygame.image.load(settings.MENU)

        self.button_1 = Button((384,200),settings.BUTTON_OFF[0])

        self.button_2 = Button((384,300),settings.BUTTON_OFF[1])

        self.button_3 = Button((384,400),settings.BUTTON_OFF[2])

        self.button_4 = Button((384,500),settings.BUTTON_OFF[3])

        self.button_list = pygame.sprite.Group()

        self.button_list.add(self.button_1,self.button_2,self.button_3,self.button_4)

    def draw(self,screen):

        screen.blit(self.background, (0, 0))

        self.button_list.draw(screen)

        pygame.display.update()


    def event(self):

        mp = pygame.mouse.get_pos()

        for itm in pygame.event.get():

            for index, btn in enumerate(self.button_list):

                if btn.collidepoint(mp):

                    btn.set_image(settings.BUTTON_ON[index])

                    if itm.type == pygame.MOUSEBUTTONDOWN and itm.button == 1:

                        self.ID = index  
                
                else: btn.set_image(settings.BUTTON_OFF[index])

            if itm.type == pygame.QUIT:
                sys.exit(0)

    def ret_id(self):

        return self.ID
    
    def set_id(self,ID):

        self.ID = ID