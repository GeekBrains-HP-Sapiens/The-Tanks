import os

import pygame

from block import *

import settings


# *************** Класс Level ***************

class Level():

    def __init__(self, filename):

        self.filename = filename

        self.title_size = 32

        self.data = []

        self.cell = []  # для передачи разметки клеток координат

        self.tiles = pygame.sprite.Group()  # Массив всех тайлов уровня(тайл - в данном случае, кирпич из которого строятся стенки уровня)"""

        self.Ax = self.Ay = self.Bx = self.By = self.Hx = self.Hy = 0

    # *************** Загрузка Level из файла ***************

    def load_level(self):  # Загружает уровень из файла уровня

        if (not os.path.isfile(self.filename)):  # Выходим из программы, если файла нет
            pygame.quit()

        f = open(self.filename, "r")

        self.data = f.read().split("\n")  # data - массив строчек файла

        x, y = 0, 0

        for row in self.data:

            for col in row:

                if col == "*":
                    self.tiles.add(Block((x, y), settings.BLOCK_1, False))

                    self.cell.append((x, y))

                if col == "#":
                    self.tiles.add(Block((x, y), settings.BLOCK_2, True, 2))

                    self.cell.append((x, y))

                if col == "H":
                    self.tiles.add(Base((x, y), settings.BASE, True, 1))

                    self.cell.append((x, y))

                if col == "A":
                    self.Ax = x  # self.A.append((x,y))

                    self.Ay = y

                if col == "B":
                    self.Bx = x  # self.A.append((x,y))

                    self.By = y

                x += self.title_size

            y += self.title_size

            x = 0

        f.close()

    # *************** Возвращает title ***************

    def ret_tiles(self):

        return self.tiles

    # *************** Возвращает cell ***************

    def ret_cell(self):

        return tuple(self.cell)

    # *************** Возвращает положение клетки нахождения players ***************

    def ret_A(self):

        return self.Ax, self.Ay

    # *************** Возвращает положение клетки нахождения enemy ***************

    def ret_B(self):

        return self.Bx, self.By
