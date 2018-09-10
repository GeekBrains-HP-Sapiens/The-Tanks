import pygame

from Objects.block import *

from Objects.bullet import *

import Utility.settings as settings


# direction constants
# (DIR_UP, DIR_DOWN, DIR_RIGHT, DIR_LEFT) = range(4)

# *************** Базовый класс Танк ***************

class Tank(pygame.sprite.Sprite):

    def __init__(self, topleft, ID=None):

        pygame.sprite.Sprite.__init__(self)

        self.id = ID

        self.tank_speedX = 0  # скорость перемещения X. 0 - стоять на месте

        self.tank_speedY = 0  # скорость перемещения Y. 0 - стоять на месте

        self.move_speed = 3  # базовая скорость

        self.tank_startX = topleft[0]  # Начальная позиция Х, пригодится когда будем переигрывать уровень

        self.tank_startY = topleft[1]  # ___----____----____

    # *************** проверка на столкновения с объектами карты ***************

    def collide(self, tank_speedX, tank_speedY, platforms):

        for p in platforms:

            if sprite.collide_rect(self, p):

                if tank_speedX > 0:
                    self.rect.right = p.rect.left

                if tank_speedX < 0:
                    self.rect.left = p.rect.right

                if tank_speedY > 0:
                    self.rect.bottom = p.rect.top

                if tank_speedY < 0:
                    self.rect.top = p.rect.bottom


# *************** Класс player наследум от базового класса Танк ***************

class Player(Tank):

    def __init__(self, topleft):

        Tank.__init__(self, topleft)

        self.direction = DIR_RIGHT  # положение танка (вверх,вниз и.т.д

        self.image = self.image2 = pygame.image.load(settings.PLAYER_TANK)

        self.rect = self.image.get_rect()

        self.rect.topleft = topleft

        self.bullet = pygame.sprite.Group()

    # *************** Возвращает координаты левого верхнего угла ***************

    def ret_topleft(self):

        return self.rect.topleft

    # *************** Заряжает спрайт снаряда ***************

    def shot_bull(self):

        self.bullet.add(Bullet((self.rect.center), self.direction))

    # *************** Возвращает снаряд ***************

    def ret_bull(self):

        return self.bullet

    # *************** Возвращает позицию центра квадрата ***************

    def ret_position(self):

        return self.rect.center

    # *************** Движение снаряда ***************

    def bull_move(self):

        for a in self.bullet:
            a.move()

    # *************** Удаление снаряда ***************

    def del_bullet(self):

        for a in self.bullet:

            if a.rect.left > (800 - a.rect.width):
                a.kill()

                return

            if a.rect.top < 0:
                a.kill()

                return

            if a.rect.left < 0:
                a.kill()

                return

            if a.rect.top > (768 - a.rect.height):
                a.kill()

                return

    # *************** Обновление данных танка ***************

    def tank_update(self, left, right, up, down, space, platforms):

        if left:
            self.tank_speedX = -self.move_speed  # Лево = x- n

            self.tank_speedY = 0

            self.direction = DIR_LEFT

            self.image = transform.rotate(self.image2, 180)

        if right:
            self.tank_speedX = self.move_speed  # Право = x + n

            self.tank_speedY = 0

            self.direction = DIR_RIGHT

            self.image = transform.rotate(self.image2, 0)

        if up:
            self.tank_speedY = -self.move_speed  # Вверх = у- п

            self.tank_speedX = 0

            self.direction = DIR_UP

            self.image = transform.rotate(self.image2, 90)

        if down:
            self.tank_speedY = self.move_speed  # Вниз = у+ п

            self.tank_speedX = 0

            self.direction = DIR_DOWN

            self.image = transform.rotate(self.image2, 270)

        if not (left or right):  # стоим, когда нет указаний идти

            self.tank_speedX = 0

        if not (up or down):  # стоим, когда нет указаний идти

            self.tank_speedY = 0

        self.rect.left += self.tank_speedX  # переносим свои положение на tank_speedX

        self.collide(self.tank_speedX, 0, platforms)

        self.rect.top += self.tank_speedY  # переносим свои положение на tank_speedY

        self.collide(0, self.tank_speedY, platforms)


# *************** Класс Enemy наследум от базового класса Танк ***************

class Enemy(Tank):

    def __init__(self, topleft):

        Tank.__init__(self, topleft)

        self.direction = None  # DIR_UP#DIR_DOWN# положение Enemy (вверх,вниз и.т.д

        self.image = self.image2 = pygame.image.load(settings.ENEMY_TANK)

        self.rect = self.image.get_rect()

        self.rect.topleft = topleft

        self.move_speed = 1  # базовая скорость

        self.enemy_life = True

    # *************** Возвращает координаты левого верхнего угла ***************

    def ret_topleft(self):

        return self.rect.left, self.rect.top

    # *************** Положение вверх ***************

    def DIR_UP(self):

        self.tank_speedY = -self.move_speed  # Вверх = у- п

        self.tank_speedX = 0

        self.image = transform.rotate(self.image2, 0)

    # *************** Положение вниз ***************

    def DIR_DOWN(self):

        self.tank_speedY = self.move_speed  # Вниз = у+ п

        self.tank_speedX = 0

        self.image = transform.rotate(self.image2, 180)

    # *************** Положение влево  ***************

    def DIR_LEFT(self):

        self.tank_speedX = -self.move_speed  # Лево = x- n

        self.tank_speedY = 0

        self.image = transform.rotate(self.image2, 90)

    # *************** Положение вправо ***************

    def DIR_RIGHT(self):

        self.tank_speedX = self.move_speed  # Право = x + n

        self.tank_speedY = 0

        self.image = transform.rotate(self.image2, 270)

    # *************** Положение остановки ***************

    def DIR_STOP(self):

        self.tank_speedX = 0

        self.tank_speedY = 0

    # *************** Движение enemy ***************


    def enemy_move(self, path):
        

        enemy_x2 = (path[1][0] * settings.SIZE_BLOCK)

        enemy_y2 = path[1][1] * settings.SIZE_BLOCK


        if self.rect.top == enemy_y2:

            if self.rect.left > enemy_x2:

                self.DIR_LEFT()
            
            if self.rect.left < enemy_x2:

                self.DIR_RIGHT()
            
            if self.rect.left == enemy_x2:

                return


        if self.rect.left == enemy_x2:

            if self.rect.top > enemy_y2:

                self.DIR_UP()
            
            if self.rect.top < enemy_y2:

                self.DIR_DOWN()
            
            if self.rect.top == enemy_y2:

                return


        self.rect.left += self.tank_speedX  # переносим свои положение на tank_speedX

        self.rect.top += self.tank_speedY  # переносим свои положение на tank_speedY

