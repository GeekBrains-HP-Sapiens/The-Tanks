
import sys, os, random

import heapq

import pygame 

from Block import *

from Bullet import *

import settings


# direction constants
#(DIR_UP, DIR_DOWN, DIR_RIGHT, DIR_LEFT) = range(4)

#*************** Базовый класс Танк ***************

class Tank(pygame.sprite.Sprite):

    def __init__(self,topleft, ID = None):

        pygame.sprite.Sprite.__init__(self)

        self.id = ID

        self.tank_speedX = 0 #скорость перемещения X. 0 - стоять на месте
        
        self.tank_speedY = 0 #скорость перемещения Y. 0 - стоять на месте
        
        self.move_speed = 3 #базовая скорость
        
        self.tank_startX = topleft [0] # Начальная позиция Х, пригодится когда будем переигрывать уровень
        
        self.tank_startY = topleft [1] #___----____----____

    
    #*************** проверка на столкновения с объектами карты ***************


    def collide(self,tank_speedX,tank_speedY,platforms):

        for p in platforms :

            if sprite.collide_rect(self, p):

                if tank_speedX > 0:

                    self.rect.right = p.rect.left

                if tank_speedX < 0:

                    self.rect.left = p.rect.right

                if tank_speedY > 0:

                    self.rect.bottom = p.rect.top

                if tank_speedY < 0:

                    self.rect.top = p.rect.bottom

#*************** Класс player наследум от базового класса Танк ***************

class Player(Tank):

    def __init__(self,topleft):

        Tank.__init__(self,topleft)

        self.direction = DIR_RIGHT# положение танка (вверх,вниз и.т.д

        self.image = self.image2 = pygame.image.load(settings.PLAYER_TANK)

        self.rect = self.image.get_rect()

        self.rect.topleft = topleft

        self.bullet = pygame.sprite.Group()

    #*************** Возвращает координаты левого верхнего угла ***************

    def ret_topleft(self):

        return self.rect.topleft

    #*************** Заряжает спрайт снаряда ***************

    def shot_bull(self):

        self.bullet.add(Bullet((self.rect.center),self.direction))

    #*************** Возвращает снаряд ***************

    def ret_bull(self):

        return self.bullet

    #*************** Возвращает позицию центра квадрата ***************

    def ret_position(self):

        return self.rect.center

    #*************** Движение снаряда ***************

    def bull_move(self):

        for a in self.bullet:

            a.move()

    #*************** Удаление снаряда ***************

    def del_bull (self):

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

    #*************** Обновление данных танка ***************

    def tank_update(self,left,right,up,down,space,platforms):

        if left:

            self.tank_speedX = -self.move_speed # Лево = x- n

            self.tank_speedY = 0

            self.direction = DIR_LEFT
            
            self.image = transform.rotate(self.image2,180)

        if right:

            self.tank_speedX = self.move_speed # Право = x + n

            self.tank_speedY = 0

            self.direction = DIR_RIGHT

            self.image = transform.rotate(self.image2,0)

        if up:

            self.tank_speedY = -self.move_speed # Вверх = у- п

            self.tank_speedX = 0

            self.direction = DIR_UP

            self.image = transform.rotate(self.image2,90)

        if down:

            self.tank_speedY = self.move_speed # Вниз = у+ п

            self.tank_speedX = 0

            self.direction = DIR_DOWN

            self.image = transform.rotate(self.image2,270)

        if not(left or right): # стоим, когда нет указаний идти

            self.tank_speedX = 0

        if not(up or down): # стоим, когда нет указаний идти

            self.tank_speedY = 0


        self.rect.left += self.tank_speedX # переносим свои положение на tank_speedX

        self.collide(self.tank_speedX,0,platforms)

        self.rect.top += self.tank_speedY # переносим свои положение на tank_speedY

        self.collide(0,self.tank_speedY,platforms)


#*************** Класс Enemy наследум от базового класса Танк ***************

class Enemy(Tank):

    def __init__(self,topleft):

        Tank.__init__(self,topleft)

        self.direction = None #DIR_UP#DIR_DOWN# положение Enemy (вверх,вниз и.т.д

        self.image = self.image2 = pygame.image.load(settings.ENEMY_TANK)

        self.rect = self.image.get_rect()

        self.rect.topleft = topleft

        self.move_speed = 1 #базовая скорость

        self.enemy_life = True

    #*************** Возвращает координаты левого верхнего угла ***************

    def ret_topleft(self):

        return self.rect.left, self.rect.top

    #*************** Положение вверх ***************

    def DIR_UP(self):

        self.tank_speedY = -self.move_speed # Вверх = у- п

        self.tank_speedX = 0

        self.image = transform.rotate(self.image2,0)

    #*************** Положение вниз ***************

    def DIR_DOWN(self):

        self.tank_speedY = self.move_speed # Вниз = у+ п

        self.tank_speedX = 0

        self.image = transform.rotate(self.image2,180)

    #*************** Положение влево  ***************

    def DIR_LEFT(self):

        self.tank_speedX = -self.move_speed # Лево = x- n

        self.tank_speedY = 0

        self.image = transform.rotate(self.image2,90)
    
    #*************** Положение вправо ***************

    def DIR_RIGHT(self):

        self.tank_speedX = self.move_speed # Право = x + n

        self.tank_speedY = 0

        self.image = transform.rotate(self.image2,270)

    #*************** Положение остановки ***************

    def DIR_STOP(self):

        self.tank_speedX = 0

        self.tank_speedY = 0
        
    #*************** Столкновение с объектами платформы ***************

    def collide_OBJ(self,platforms):

        x=self.rect.left

        y=self.rect.top

        new_pos_rect = Rect((x-1,y-1),(42,42))

        for p in platforms:

            if Rect.colliderect(new_pos_rect,p.rect):

                return True

    def collide_UP(self,tank_speedX,tank_speedY,platforms):

        self.new_pos_rect.left = self.rect.left

        self.new_pos_rect.top = self.rect.top

        for p in platforms :

            if Rect.colliderect(self.new_pos_rect,p.rect):

                if tank_speedY < 0:#if tank_speedX < 0 or tank_speedX > 0 or tank_speedY < 0:

                    self.new_pos_rect.top = p.rect.bottom

                    return True

    def collide_DOWN(self,tank_speedX,tank_speedY,platforms):

        self.new_pos_rect.left = self.rect.left

        self.new_pos_rect.top = self.rect.top

        for p in platforms :

            if Rect.colliderect(self.new_pos_rect,p.rect):

                if tank_speedY > 0:#if tank_speedX < 0 or tank_speedX > 0 or tank_speedY > 0:

                    self.new_pos_rect.bottom = p.rect.top

                    return True

    def collide_LEFT(self,tank_speedX,tank_speedY,platforms):

        self.new_pos_rect.left = self.rect.left

        self.new_pos_rect.top = self.rect.top

        for p in platforms :

            if Rect.colliderect(self.new_pos_rect,p.rect):

                if tank_speedX < 0:

                    self.new_pos_rect.left = p.rect.right

                    return True

    def collide_RIGHT(self,tank_speedX,tank_speedY,platforms):

        self.new_pos_rect.left = self.rect.left

        self.new_pos_rect.top = self.rect.top

        for p in platforms :

            if Rect.colliderect(self.new_pos_rect,p.rect):

                if tank_speedX > 0:

                    self.new_pos_rect.right = p.rect.left

                    return True

    #*************** Движение enemy ***************

    def enemy_move(self,path):

        print (len(path))

        if len(path) <=1:

            return


        x=self.rect.left

        y=self.rect.top

        Ex=x

        Ey=y

        Px= path[1][0]*32

        Py= path[1][1]*32

        A=True

        print ('!!!!','Px ',Px,' Py ',Py, ' x ',x,' y ',y)

        if (x,y) not in path:

            self.DIR_STOP()

            print ("OUT OF PATH") 

        move_x = move_y = False

        if Ey == Py:

            move_x = True

            move_y = False

        if Ex == Px:

            move_y = True

            move_x = False

        print (move_x, '    ',move_y)

        if move_x:

            print ("IN MOVE_X IF")

            if Ex > Px:

                    self.DIR_LEFT()

                    print ('DIR_LEFT - ','Ex- ',Ex,'Px- ',Px)

            if Ex < Px:

                    self.DIR_RIGHT()

                    print ('DIR_RIGHT - ','Ex- ',Ex,'Px- ',Px)

            if Ex == Px:

                    print ('Ex == Px')

                    move_x=False

                    if len(path)>1:

                        path.pop(0)

                    else:

                        self.DIR_STOP()

        if Ey == Py:

            move_x = True

            move_y = False

            print ('move_x = ',move_x)

        if Ex == Px:

            move_y = True

            move_x = False

#ЕСЛИ ДОШЕЛ ДО КОНЦА ПУТИ, ТО ИСКАТЬ НОВЫЙ!!!
        if move_y:

            if Ey > Py:

                self.DIR_UP()

                print ('DIR_UP - ','Ey- ',Ey,'Py- ',Py)

            if Ey < Py:

                self.DIR_DOWN()

                print ('DIR_DOWN - ','Ey- ',Ey,'Py- ',Py)

            if Ey == Px:

                if len(path)>1:

                    path.pop(0)

                else:

                    self.DIR_STOP()

        if Px == Ex and Py ==Ey:

            path.pop(0)

            return
                            #if Ey == Py:
            #    path.pop(0)
            #    print 'POP - ','Ey- ',Ey,'Py- ',Py




        self.rect.left += self.tank_speedX # переносим свои положение на tank_speedX
        
        self.rect.top += self.tank_speedY # переносим свои положение на tank_speedY
        #return True
