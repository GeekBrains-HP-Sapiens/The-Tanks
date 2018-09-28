import pygame

import Utility.settings as settings


class InitWindows():

    def __init__(self):

        # *************** основное window ***************

        self.win_width = settings.WIDTH_WIN  # Ширина окна

        self.win_height = settings.HEIGHT_WIN  # Высота окна

        self.win_display = (self.win_width, self.win_height)  # Компановка

        self.screen = pygame.display.set_mode(self.win_display)  # Создаем окошко

        pygame.display.set_caption('Tanks')  # название шапки "капчи"

        pygame.init()  # Инициализация pygame