
import sys

import os

import pygame

import settings


# *************** Класс окна (основное window, окно Game_Window, окно Results_Window, окно Chat_Window) ***************

class Windows():

    def __init__(self):

        # *************** окно Game_Window ***************

        self.bg = pygame.image.load(settings.WALLPAPER)

    # *************** окно Results_Window ***************

        self.rect_color_RW = (0, 0, 139)  # цвет окна

        self.rect_rect_RW = ((800, 0), (224, 384))  # расположение и размер

        self.rect_width_RW = 0  # заливка

    # *************** окно Chat_Window ***************

        self.rect_color_CW = (152, 251, 152)  # цвет окна

        self.rect_rect_CW = ((800, 384), (224, 384))  # расположение и размер

        self.rect_width_CW = 0  # заливка

    # *************** рисуем окна ***************

    def draw_windows(self, screen):

        screen.blit(self.bg, (0,0))

        pygame.draw.rect(screen, self.rect_color_RW, self.rect_rect_RW,
                        self.rect_width_RW)  # рисуем окно Results_Window

        pygame.draw.rect(screen, self.rect_color_CW, self.rect_rect_CW,
                        self.rect_width_CW)  # рисуем окно Chat_Window
