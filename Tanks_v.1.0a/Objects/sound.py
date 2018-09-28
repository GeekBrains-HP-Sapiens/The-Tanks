import pygame

import Utility.settings as settings


class SoundGame():

    def __init__(self, filename=None):

        self.filename = filename


    def sound(self,filename):


        sound = pygame.mixer.Sound(filename)

        sound.play()

    def soundtrack(self):

        self.filename = settings.SOUNDTRACK_1

        pygame.mixer.music.load(self.filename)

        pygame.mixer.music.play(-1)