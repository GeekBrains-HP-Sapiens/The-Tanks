import sys

import pygame

from pygame.time import set_timer

import threading

from Utility.init_win import InitWindows

import Utility.settings as settings

from Utility.a_star import *

from Utility.animation_object import anim_object as anim

from Objects.game_window import GameWindow

from Objects.level import Level

from Objects.tank import Tank, Player, Enemy

from Objects.sound import SoundGame


class AppGame(InitWindows):

    def __init__(self):

        super(AppGame, self).__init__()

        # ФЛАГИ

        self.left = self.right = self.up = self.down = self.space = False # Флаги кнопок

        self.exit_ = True  # флаг для выхода


        # ID ПРОЦЕССОВ + ТАЙМЕР ПРОЦЕССОВ
        
        self.timer = pygame.time.Clock()  # Таймер игровых ID процессов

        self.TARGET = pygame.USEREVENT # таргет по ID пользователю

        # self.UPDATE = pygame.USEREVENT + 1 # таргет по ID пользователю 

        set_timer(self.TARGET, 500) # установка таймера процесса запуска ID

        # set_timer(self.UPDATE, 1) # установка таймера процесса запуска ID
        

        # ЗВУКИ В ИГРЕ + ФОН

        self.sound = SoundGame() #загрузка базового класса звуков

        self.sound.soundtrack() # инициализация фоновой музыки


        # АНИМАЦИИ

        self.anim_explosions = anim(settings.ANIMATION_EXPLOSIONS) # загрузка анимации взрыва

        self.topleft_anim = None # topleft анимации


        # ИНОЕ

        self.game_window = GameWindow()  # инизиализация GameWindow

        self.level_count = 0 #счетчик уровня

        self.score = 0 # иницилизация счета

        self.path = [] 



    #ЗАГРУЗКА УРОВНЯ

    def load_level(self):

        # *************** Инициализация элементов карты ***************
        self.level = Level(settings.LEVEL_1[self.level_count])  # Инициализируем level1

        self.level.load_level() # загрузка карты

        self.player = Player(self.level.ret_player())  # инициализируем Tank по карте

        # self.enemy = Enemy(self.level.ret_B()) # загрузка Enemy на карте +++++++++++++++++++++

        self.platforms = self.level.ret_tiles() # загрузка блоков на карте

        # *************** блоки спрайтов ***************

        self.block_list = pygame.sprite.Group()  # Общий список блоков

        self.player_list = pygame.sprite.Group()  # Список игроков

        self.bullet_list = pygame.sprite.Group()  # Список пуль

        self.block_list_destruct = pygame.sprite.Group()  # Список разрушающихся блоков

        self.block_list_undestruct = pygame.sprite.Group()  # Список неразрушающихся блоков

        self.enemy_list = pygame.sprite.Group() # Список ботов

        self.block_list.add(self.platforms) # Загрузка всех блоков

        self.player_list.add(self.player) # Загрузка игроков

        if len(self.level.ret_enemy()) > 0: # Загрузка ботов

            for enemy in self.level.ret_enemy(): # --__--__--__--

                self.enemy_list.add(Enemy(enemy)) # --__--__--__--

        self.init_walls() # Инициализация cтены
       
        for enemy in self.enemy_list: # Инициализация поиска пути A_star
            
            self.path.append(enemy.ret_path(self.player.ret_end(),self.walls)) # --__--__--__--

    # Инициализация cтены
    def init_walls(self):

        self.walls = []

        for block in self.block_list:

            x, y = block.rect.topleft

            self.walls.append((x // settings.SIZE_H, y // settings.SIZE_W))

            if block.destructibility:

                self.block_list_destruct.add(block)

            else:

                self.block_list_undestruct.add(block)


     # *************** обработка event ***************

    def event_game(self):

        for itm in pygame.event.get():

            if len(self.enemy_list) >0: # пока есть боты

                if itm.type == self.TARGET:
                    self.target_player()

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
                self.sound.sound_shot()   
                
            if (itm.type == pygame.QUIT) or (itm.type == pygame.KEYDOWN and itm.key == pygame.K_ESCAPE):
                sys.exit(0)

    # *************** Трассер обновления пути от Enemy к Player ***************

    def target_player(self):

        self.path.clear()

        for enemy in self.enemy_list: # Инициализация поиска пути A_star
            
            self.path.append(enemy.ret_path(self.player.ret_end(),self.walls)) # --__--__--__--
        
    # *************** обработка процессов и действий (обработка нажатий (mouse and keyboard и др.))

    def action(self):

        while self.exit_:

            self.timer.tick(60)

            self.event_game()

            self.update_game()

            self.draw_game()
            

    # *************** отобрыжение процессов ***************

    def draw_game(self):

        self.game_window.draw_windows(self.screen)  # рисуем окна

        self.block_list.draw(self.screen)

        self.bullet_list.draw(self.screen)

        self.anim_explosions.blit(self.screen,self.topleft_anim)

        self.enemy_list.draw(self.screen)
       
        self.player_list.draw(self.screen)

        #  отрисовка счета (считает колличество сломанных блоков)
        self.show_score()

        self.show_fps()

        pygame.display.update()  # обновление и вывод всех изменений на экран

    # *************** player shot ***************

    def shot_bull_game(self):

        self.player.shot_bull()

        self.bullet_list.add(self.player.ret_bull())

    # *************** destroy objects + animation ***************

    def destroy_objects_game(self):

        group_hit_list = pygame.sprite.groupcollide(self.block_list_destruct, self.bullet_list, False, True)

        if group_hit_list:
            
            self.anim_explosions.play()# запуск анимации

            anim_stop = threading.Timer(1.0, self.anim_explosions.stop) #остановка анимации через 1 сек
            
            anim_stop.start()

            for block in group_hit_list:

                # self.topleft_anim = bullet[0].ret_center()#  передаем координаты взрыва
                self.topleft_anim = block.ret_topleft()

                block.health -= 1

                if block.health == 2:

                    tmp_topleft = block.ret_topleft()

                    block.set_image(tmp_topleft,settings.BLOCK_DESTRUCT_2)

                if block.health == 1:
        
                    tmp_topleft = block.ret_topleft()

                    block.set_image(tmp_topleft,settings.BLOCK_DESTRUCT_3)

                if block.health <= 0:

                    self.block_list_destruct.remove(block)
                    
                    self.block_list.remove(block)

                # переход на другой уровень
                if hasattr(block, 'end_lvl'):

                    self.score += 1

                    try: 

                        self.level_count += 1

                        self.play_game()

                    except IndexError:

                        self.level_count = 0

                        self.play_game()
        
        group_enemy_list = pygame.sprite.groupcollide(self.enemy_list, self.bullet_list, False, True)

        if group_enemy_list:

            self.anim_explosions.play()# запуск анимации

            anim_stop = threading.Timer(1.0, self.anim_explosions.stop) #остановка анимации через 1 сек
            
            anim_stop.start()

            
            for enemy in group_enemy_list:

                self.topleft_anim = enemy.ret_topleft()

                enemy.health -= 1

                if enemy.health <= 0:

                    self.score += 1

                    enemy.kill()

                    self.enemy_list.remove(enemy)
                  

        pygame.sprite.groupcollide(self.block_list_undestruct, self.bullet_list, False, True)

        self.player.del_bullet()  # проверка выхода пули за экран и удаление

    # *************** update ***************

    def update_game(self):

        self.init_walls()

        self.player.tank_update(self.left, self.right, self.up, self.down, self.space, self.block_list)

        for index, enemy in enumerate(self.enemy_list): # Движение ботов
            
            enemy.enemy_move(self.path[index])

        self.destroy_objects_game()

        self.player.bull_move()

    # *************** удаление данных (destroy data here) ***************

    def end_pygame():

        pygame.quit()

    # *************** ЗАПУСК ИГРЫ ***************

    def play_game(self):

        self.load_level()

        self.action()

        self.end_pygame()

    # функция отображения счета
    def show_score(self):

        s_font = pygame.font.SysFont('Arial', 24)

        text = s_font.render("Score: "+str(self.score),True,settings.WHITE)
        
        s_rect = text.get_rect()

        s_rect.midtop = (900, 0)

        self.screen.blit(text, s_rect)


    # Теcт FPS

    def show_fps(self):

        s_font = pygame.font.SysFont('Arial', 24)

        fps = int(self.timer.get_fps())

        text = s_font.render("FPS: "+str(fps),True,settings.WHITE)

        s_rect = text.get_rect()

        s_rect.midtop = (900, 50)

        self.screen.blit(text, s_rect)


if __name__ == '__main__':

    game = AppGame()

    game.play_game()
