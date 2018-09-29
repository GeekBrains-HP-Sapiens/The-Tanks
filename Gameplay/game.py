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


#****************************ID процессов игры

(MENU,NEW_GAME,CONTINUE,SETTINGS,EXIT,GAME_OVER)=(-1,0,1,2,3,4)


class Game():

    def __init__(self,screen):

        self.screen = screen

        # ФЛАГИ + ИГРОВЫЕ ПРОЦЕССЫ

        self.left = self.right = self.up = self.down = self.space = False # Флаги кнопок

        self.exit_ = None  # флаг для выхода

        self.shot_flag = False

        self.gameplay = NEW_GAME 

        # ID ПРОЦЕССОВ + ТАЙМЕР ПРОЦЕССОВ
        
        self.timer = pygame.time.Clock()  # Таймер игровых ID процессов

        self.TARGET = pygame.USEREVENT # таргет по ID пользователю

        self.SHOT_ENEMY = pygame.USEREVENT + 1 # ID выстрела бота 

        set_timer(self.TARGET, 500) # установка таймера процесса запуска ID

        set_timer(self.SHOT_ENEMY, 1000) # установка таймера процесса запуска ID shoot_enemy
 

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

        self.left = self.right = self.up = self.down = self.space = False # Флаги кнопок

        self.gameplay = NEW_GAME # первоначальный процесс игры

        # *************** Инициализация элементов карты ***************
        self.level = Level(settings.LEVEL_1[self.level_count % 3])  # Инициализируем level1

        self.level.load_level() # загрузка карты

        self.player = Player(self.level.ret_player())  # инициализируем Tank по карте

        self.platforms = self.level.ret_tiles() # загрузка блоков на карте

        # *************** блоки спрайтов ***************

        self.block_list = pygame.sprite.Group()  # Общий список блоков

        self.player_list = pygame.sprite.Group()  # Список игроков

        self.bullet_list_player = pygame.sprite.Group()  # Список пуль player

        self.bullet_list_enemy = pygame.sprite.Group()  # Список пуль enemy

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

    # *************** следующий уровень ***************

    def next_level(self):

        if len(self.enemy_list) <=0: # пока есть боты

            self.level_count += 1

            self.load_level()

            self.play_game()

        

    # *************** обработка event ***************

    def event_game(self):

        for itm in pygame.event.get():

            if len(self.enemy_list) >0: # пока есть боты

                if itm.type == self.TARGET:
                    self.target_player()
            
            self.next_level()
           
            if self.shot_flag:

                if itm.type == self.SHOT_ENEMY:
                    self.shot_bullet_enemy()

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
                self.shot_bullet_player()
                self.space = False 
                self.sound.sound(settings.SOUND_SHOT_1)  
                
            if itm.type == pygame.QUIT:
                sys.exit(0)
            
            if itm.type == pygame.KEYDOWN and itm.key == pygame.K_ESCAPE:
                self.gameplay = MENU
                self.exit_ = False
        

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

            if self.gameplay == GAME_OVER: # Процесс смерти игрока

                return

    # *************** отобрыжение процессов ***************

    def draw_game(self):

        self.game_window.draw_windows(self.screen)  # рисуем окна

        self.block_list.draw(self.screen)

        self.bullet_list_player.draw(self.screen)

        self.bullet_list_enemy.draw(self.screen)

        self.anim_explosions.blit(self.screen,self.topleft_anim)

        self.enemy_list.draw(self.screen)
       
        self.player_list.draw(self.screen)

        #  отрисовка счета (считает колличество сломанных блоков)
        self.show_score()

        self.show_fps()

        self.show_life()

        self.show_level()

        pygame.display.update()  # обновление и вывод всех изменений на экран

    # *************** player shot ***************

    def shot_bullet_player(self):

        self.bullet_list_player.add(self.player.ret_bullet())

    # *************** enemy shot ***************

    def shot_bullet_enemy(self):

        for enemy in self.enemy_list:

            self.bullet_list_enemy.add(enemy.ret_bullet())
        

    # *************** destroy objects + animation ***************

    def destroy_objects_game(self):

        # Разрушаемые блоки и пули игрока

        group_hit_list = pygame.sprite.groupcollide(self.block_list_destruct, self.bullet_list_player, False, True)

        # Не разрушаемые блоки и пули игрока

        pygame.sprite.groupcollide(self.block_list_undestruct, self.bullet_list_player, False, True)

        # Разрушаемые блоки и пули бота

        group_hit_list_2 = pygame.sprite.groupcollide(self.block_list_destruct, self.bullet_list_enemy, False, True)

        # Не разрушаемые блоки и пули бота

        pygame.sprite.groupcollide(self.block_list_undestruct, self.bullet_list_enemy, False, True)

        # Боты и пули игрока

        group_enemy_list = pygame.sprite.groupcollide(self.enemy_list, self.bullet_list_player, False, True)

        # Игрок и пули бота

        group_player_list = pygame.sprite.groupcollide(self.player_list, self.bullet_list_enemy, False, True)


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

                    self.init_walls()

        
        if group_hit_list_2:
            
            self.anim_explosions.play()# запуск анимации

            anim_stop = threading.Timer(1.0, self.anim_explosions.stop) #остановка анимации через 1 сек
            
            anim_stop.start()

            for block in group_hit_list_2:

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

                    self.init_walls()


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

                    for bul in self.bullet_list_enemy:#убиваем бота, убиваем и пулю

                        bul.kill()

        
        if group_player_list:

            self.anim_explosions.play()# запуск анимации

            anim_stop = threading.Timer(1.0, self.anim_explosions.stop) #остановка анимации через 1 сек
            
            anim_stop.start()
            
            for player in group_player_list:

                self.topleft_anim = player.ret_topleft()

                player.health -= 1

                if player.health <= 0:

                    player.kill()

                    self.player_list.remove(player)

                    for bul in self.bullet_list_player:#убиваем игрока, убиваем и пулю

                        bul.kill()

                    for bul in self.bullet_list_enemy:#убиваем и пулю бота

                        bul.kill()
                    
                    self.sound.sound(settings.SOUND_GAME_OVER)
                    
                    self.gameplay = GAME_OVER


    # *************** update ***************

    def update_game(self):

        self.player.tank_update(self.left, self.right, self.up, self.down, self.space, self.block_list)

        for index, enemy in enumerate(self.enemy_list): # Движение ботов
            
            enemy.enemy_move(self.path[index],self.block_list)

            if len(self.path[index]) <=5:

                self.shot_flag = True
            
            else:

                self.shot_flag =False

        self.destroy_objects_game()


        if len(self.bullet_list_player) >0: # если есть пули player

            self.player.bullet_move()


        if len(self.bullet_list_enemy) >0: # если есть пули enemy

            for enemy in self.enemy_list:

                enemy.bullet_move()

    # # *************** ЗАПУСК ИГРЫ ***************

    def play_game(self):

        self.action()

    
    # Теcт FPS

    def show_fps(self):

        fps = int(self.timer.get_fps())

        text = self.font.render("FPS: "+str(fps),True,settings.WHITE)

        s_rect = text.get_rect()

        s_rect.midtop = (900,0)

        self.screen.blit(text, s_rect)

    # функция отображения счета

    def show_score(self):

        self.font = pygame.font.SysFont('Arial', 24)

        text = self.font.render("Score: "+str(self.score),True,settings.WHITE)
        
        s_rect = text.get_rect()

        s_rect.midtop = (900, 50)

        self.screen.blit(text, s_rect)

    # Life player

    def show_life(self):

        life = self.player.ret_health()

        text = self.font.render("Life: "+str(life),True,settings.WHITE)

        s_rect = text.get_rect()

        s_rect.midtop = (900,100)

        self.screen.blit(text, s_rect)
    
    # Level

    def show_level(self):

        level = self.level_count

        text = self.font.render("Level: "+str(level+1),True,settings.WHITE)

        s_rect = text.get_rect()

        s_rect.midtop = (900,150)

        self.screen.blit(text, s_rect)


    #вспомогательные модули

    def get_id(self):

        return self.gameplay


    def set_exit(self,bool):

        self.exit_ = bool


    def set_level(self,lvl):

        self.level_count = lvl

    
    def set_score(self,score):

        self.score = score