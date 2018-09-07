
import sys, os

import pygame

from pygame.time import set_timer

from Windows import Windows

from Level import Level

from Tank import Tank, Player, Enemy

import settings

from A_star import *


class AppGame():

    def __init__(self):

        #*************** основное window ***************

        self.win_width =  settings.WIDTH_WIN # Ширина окна

        self.win_height = settings.HEIGHT_WIN  # Высота окна

        self.win_display = (self.win_width, self.win_height)  # Компановка

        self.timer = pygame.time.Clock()  # Таймер кадров
      
        #*************** инициализация объектов ***************

        self.left = self.right = self.up = self.down = self.space = False

        self.exit_ = True  # флаг для выхода

        self.windows = Windows()  # инициализируем Windows

        self.TARGET = pygame.USEREVENT

        self.level1 = Level(settings.LEVEL_1)# Инициализируем level1

        self.level1.load_level()

        self.player = Player(self.level1.ret_A())# инициализируем Tank по карте
        
        self.enemy = Enemy(self.level1.ret_B())
        
        self.platforms = self.level1.ret_tiles()

        self.end = (self.player.ret_topleft()[0]/32,self.player.ret_topleft()[1]/32)
        
        self.start = (self.level1.ret_B()[0]/32, self.level1.ret_B()[1]/32)
       

        #*************** блоки спрайтов ***************

        self.block_list = pygame.sprite.Group() #Это список спрайтов. Каждый блок добавляется в этот список.
        
        self.all_sprites_list = pygame.sprite.Group()# # Это список каждого спрайта. Все блоки, а также блок игрока.
        
        self.bullet_list = pygame.sprite.Group()#тес массив спрайтов пули

        self.block_list.add(self.platforms)
        
        self.all_sprites_list.add(self.player,self.enemy)


        self.walls = []

        for i in self.block_list:

            x,y = i.rect.topleft
            
            self.walls.append((x/32,y/32))


        #*************** инициализируем pygame (получаем screen) ***************

    def init_window(self):

        pygame.init()  # Инициализация pygame

        self.screen = pygame.display.set_mode(self.win_display)  # Создаем окошко

        pygame.display.set_caption('Tanks')  # название шапки "капчи"

        set_timer(self.TARGET, 2000)

    #*************** обработка процессов и действий (обработка нажатий (mouse and keyboard и др.))
    
    def action(self):

        while self.exit_:

            self.timer.tick(60)

    #*************** обработка ***************

            for itm in pygame.event.get():

                if itm.type == pygame.KEYDOWN and itm.key == pygame.K_LEFT:
                    self.left = True

                if itm.type == pygame.KEYUP and itm.key == pygame.K_LEFT:
                    self.left = False

                if itm.type == pygame.KEYDOWN and itm.key == pygame.K_RIGHT:
                    self.right = True

                if itm.type == pygame.KEYUP and itm.key == pygame.K_RIGHT:
                    self.right = False

                if itm.type == pygame.KEYDOWN and itm.key == pygame.K_UP:
                    self.up = True

                if itm.type == pygame.KEYUP and itm.key == pygame.K_UP:
                    self.up = False

                if itm.type == pygame.KEYDOWN and itm.key == pygame.K_DOWN:
                    self.down = True

                if itm.type == pygame.KEYUP and itm.key == pygame.K_DOWN:
                    self.down = False

                if itm.type == pygame.KEYDOWN and itm.key == pygame.K_SPACE:
                    self.space = True

                if itm.type == pygame.KEYUP and itm.key == pygame.K_SPACE:
                    self.shot_bull_game()
                    self.space = False

                if (itm.type == pygame.QUIT) or (itm.type == pygame.KEYDOWN and itm.key == pygame.K_ESCAPE):
                    sys.exit(0)

            self.draw_game()

            self.update_game()


    #*************** отобрыжение процессов ***************

    def draw_game(self):

        self.windows.draw_windows(self.screen)#рисуем окна

        self.block_list.draw(self.screen)

        self.bullet_list.draw(self.screen)

        self.all_sprites_list.draw(self.screen)

        pygame.display.update()# обновление и вывод всех изменений на экран

    #*************** player shot ***************

    def shot_bull_game(self):

        self.player.shot_bull()

        self.bullet_list.add(self.player.ret_bull())

    #*************** destroy bullet ***************

    def destroy_bull_game(self):

        # print ('start', len(self.block_list))

        pygame.sprite.groupcollide(self.block_list,self.bullet_list,True,True)

        self.player.del_bull()#проверка выхода пули за экран и удаление

    #*************** update ***************

    def update_game(self):
        
        self.player.tank_update(self.left,self.right,self.up,self.down,self.space,self.block_list)
        
        # self.enemy.enemy_move(self.path)
        
        self.destroy_bull_game()
        
        self.player.bull_move()
    #*************** удаление данных (destroy data here) ***************

    def end_pygame():

        pygame.quit()

    #*************** ЗАПУСК ИГРЫ ***************

    def play_game(self):

        self.init_window()

        self.action()

        self.end_pygame()


if __name__ == '__main__':

    game = AppGame()

    game.play_game()