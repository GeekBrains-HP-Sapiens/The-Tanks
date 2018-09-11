import pygame

import Utility.settings as settings


class SoundGame():

    def __init__(self, filename=None):

        self.filename = filename

        # self.music = pygame.mixer.music.load(self.filename)

        # self.play_music = pygame.mixer.music.play()


    def sound_shot(self):

        self.filename = settings.SOUND_SHOT_1

        sound = pygame.mixer.Sound(self.filename)

        sound.play()

    def soundtrack(self):

        self.filename = settings.SOUNDTRACK_1

        pygame.mixer.music.load(self.filename)

        pygame.mixer.music.play(-1)