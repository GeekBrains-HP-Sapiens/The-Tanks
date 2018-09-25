import sys

import pygame

from pygame.time import set_timer

from Utility.init_win import InitWindows

import Utility.settings as settings

from Objects.sound import SoundGame

from Gameplay.game_over import GameOver

from Gameplay.menu import Menu

from Gameplay.game import Game


#****************************ID процессов игры

(MENU,GAME,CONTINUE,SETTINGS,EXIT,GAME_OVER)=(-1,0,1,2,3,4)


class AppGame(InitWindows):

    def __init__(self):

        super(AppGame, self).__init__()

        # ФЛАГИ + ИГРОВЫЕ ПРОЦЕССЫ

        self.timer = pygame.time.Clock()  # Таймер игровых ID процессов

        self.exit_ = True  # флаг для выхода

        self.gameplay = MENU # процесс игры

        self.game_over = GameOver()

        self.game_menu = Menu()

        self.game = Game(self.screen)

    def action(self):

        while self.exit_:

            self.timer.tick(60) 

            if self.gameplay is MENU:

                self.game_menu.draw(self.screen)

                self.game_menu.event()

                if self.game_menu.ret_id() is GAME:

                    self.gameplay = GAME

                if self.game_menu.ret_id() is MENU:

                    self.gameplay = MENU
                
                if self.game_menu.ret_id() is EXIT:

                    sys.exit(0)

                # print(self.game_menu.ret_id())

            if self.gameplay is GAME: # Игровой процесс 

                self.game.play_game()

                if self.game.ret_id() is MENU:

                    self.gameplay = MENU
            
            if self.gameplay is GAME_OVER: # Процесс смерти игрока

                self.game_over.draw(self.screen)

                if self.game_over.event() is GAME:

                    self.gameplay = GAME
                    
                    # self.load_level()

                    # self.score = 0



    # *************** удаление данных (destroy data here) ***************

    def end_pygame(self):

        pygame.quit()

    # *************** ЗАПУСК ИГРЫ ***************

    def play_game(self):

        self.action()

        self.end_pygame()


if __name__ == '__main__':

    game = AppGame()

    game.play_game()
