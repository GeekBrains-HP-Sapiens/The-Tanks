import sys

import pygame

from pygame.time import set_timer

from threading import Thread

from Objects.windows import Windows

from Objects.level import Level

from Objects.tank import Tank, Player, Enemy

from Objects.sound import SoundGame

import Utility.settings as settings

from Utility.a_star import *


class AppGame():

    def __init__(self):

        # *************** основное window ***************

        self.win_width = settings.WIDTH_WIN  # Ширина окна

        self.win_height = settings.HEIGHT_WIN  # Высота окна

        self.win_display = (self.win_width, self.win_height)  # Компановка

        self.timer = pygame.time.Clock()  # Таймер кадров

        # *************** инициализация объектов ***************

        self.left = self.right = self.up = self.down = self.space = False

        self.exit_ = True  # флаг для выхода

        self.windows = Windows()  # инициализируем Windows

        self.TARGET = pygame.USEREVENT # таргет по пользователю

        self.level_count = 0

        self.sound = SoundGame()

        self.score = 0 # иницилизация счета

        self.init_window()

    #загрузка уровня
    def load_level(self):
        # *************** Инициализация блоков ***************
        self.level = Level(settings.LEVEL_1[self.level_count])  # Инициализируем level1

        self.level.load_level() # загрузка карты

        self.player = Player(self.level.ret_A())  # инициализируем Tank по карте

        self.enemy = Enemy(self.level.ret_B()) # загрузка Enemy на карте

        self.platforms = self.level.ret_tiles() # загрузка блоков на карте

        self.end = (self.player.ret_topleft()[0] // settings.SIZE_BLOCK, self.player.ret_topleft()[1] // settings.SIZE_BLOCK)

        self.start = (self.level.ret_B()[0] // settings.SIZE_BLOCK, self.level.ret_B()[1] // settings.SIZE_BLOCK)

        # *************** блоки спрайтов ***************

        self.block_list = pygame.sprite.Group()  # Это список спрайтов. Каждый блок добавляется в этот список.

        self.all_sprites_list = pygame.sprite.Group()  # # Это список каждого спрайта. Все блоки, а также блок игрока.

        self.bullet_list = pygame.sprite.Group()  # тес массив спрайтов пули

        self.block_list_destruct = pygame.sprite.Group()  # Массив разрушающихся блоков

        self.block_list_undestruct = pygame.sprite.Group()  # Массив неразрушающихся блоков

        self.block_list.add(self.platforms)

        self.all_sprites_list.add(self.player, self.enemy)
        
        self.init_walls() # Инициализация блоков
        
    # *************** Инициализация поиска пути A_star ***************

        self.path = AStar(self.start,self.end,self.walls,settings.SIZE_ELEM)

    def init_walls(self):

        self.walls = []

        for block in self.block_list:

            x, y = block.rect.topleft

            self.walls.append((x // settings.SIZE_H, y // settings.SIZE_W))

            if block.destructibility:

                self.block_list_destruct.add(block)

            else:

                self.block_list_undestruct.add(block)

    # *************** инициализируем pygame (получаем screen) ***************

    def init_window(self):

        pygame.init()  # Инициализация pygame

        self.screen = pygame.display.set_mode(self.win_display)  # Создаем окошко

        pygame.display.set_caption('Tanks')  # название шапки "капчи"

        self.sound.soundtrack()

        set_timer(self.TARGET, 2000)

     # *************** обработка event ***************

    def event_game(self):

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
                self.sound.sound_shot()   
                
            if (itm.type == pygame.QUIT) or (itm.type == pygame.KEYDOWN and itm.key == pygame.K_ESCAPE):
                sys.exit(0)

    # *************** Трассер обновления пути от Enemy к Player ***************

    def target_player(self):

        self.end = (self.player.ret_topleft()[
            0]//settings.SIZE_BLOCK, self.player.ret_topleft()[1]//settings.SIZE_BLOCK)

        self.start = (self.enemy.ret_topleft()[
            0]//settings.SIZE_BLOCK, self.enemy.ret_topleft()[1]//settings.SIZE_BLOCK)

        self.path = AStar(self.start, self.end,self.walls, settings.SIZE_ELEM)


    # *************** обработка процессов и действий (обработка нажатий (mouse and keyboard и др.))

    def action(self):

        while self.exit_:

            self.timer.tick(80)

            target_thread = Thread(target=self.target_player, daemon=True)

            target_thread.start()

            self.event_game()

            self.draw_game()

            self.update_game()

    # *************** отобрыжение процессов ***************

    def draw_game(self):

        self.windows.draw_windows(self.screen)  # рисуем окна

        self.block_list.draw(self.screen)

        self.bullet_list.draw(self.screen)

        # Отрисовка пути/***** ВРЕМЕННО - ТЕСТ !!! *****/

        # for i in self.path:
            
        #     pf = pygame.Surface((32,32))

        #     pf.fill(pygame.Color('#FF6262'))

        #     self.screen.blit(pf,(i[0]*32,i[1]*32))

        self.all_sprites_list.draw(self.screen)

        #  отрисовка счета (считает колличество сломанных блоков)
        self.show_score()

        pygame.display.update()  # обновление и вывод всех изменений на экран

    # *************** player shot ***************

    def shot_bull_game(self):

        self.player.shot_bull()

        self.bullet_list.add(self.player.ret_bull())

    # *************** destroy objects + animation ***************

    def destroy_objects_game(self):

        group_hit_list = pygame.sprite.groupcollide(self.block_list_destruct, self.bullet_list, False, True)

        for block in group_hit_list:

            block.health -= 1

            if block.health == 2:

                tmp_topleft = block.get_topleft()

                block.set_image(tmp_topleft,settings.BLOCK_DESTRUCT_2)

            if block.health == 1:
    
                tmp_topleft = block.get_topleft()

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
                


        pygame.sprite.groupcollide(self.block_list_destruct, self.bullet_list, True, True)

        pygame.sprite.groupcollide(self.block_list_undestruct, self.bullet_list, False, True)

        self.player.del_bullet()  # проверка выхода пули за экран и удаление

    # *************** update ***************

    def update_game(self):

        self.init_walls()

        self.player.tank_update(self.left, self.right, self.up, self.down, self.space, self.block_list)

        self.enemy.enemy_move(self.path)

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


if __name__ == '__main__':

    game = AppGame()

    game.play_game()
