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

(MENU,NEW_GAME,CONTINUE,SETTINGS,EXIT,GAME_OVER)=(-1,0,1,2,3,4)


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

            #********** Процесс Меню **********  

            if self.gameplay == MENU: 

                self.game_menu.draw(self.screen)

                event = self.game_menu.event()   

                if event == NEW_GAME:

                    self.gameplay = NEW_GAME   

                if event == CONTINUE:

                    self.gameplay = CONTINUE  

                # if event == SETTINGS:

                #     self.gameplay = SETTINGS 
                
                if event == EXIT:

                    self.gameplay = EXIT  

                    
            #********** Процесс новой игры ********** 

            if self.gameplay == NEW_GAME:
                    
                self.game.set_exit(True)

                self.game.load_level()

                self.game.play_game()

                if self.game.get_id() == MENU:

                    self.gameplay = MENU

                if self.game.get_id() == GAME_OVER:

                    self.gameplay = GAME_OVER

            #********** Процесс продолжение игры **********
            
            if self.gameplay == CONTINUE:

                self.game.set_exit(True)

                self.game.play_game()

                if self.game.get_id() == MENU:

                    self.gameplay = MENU
                
                if self.game.get_id() == GAME_OVER:

                    self.gameplay = GAME_OVER
            
            #********** Процесс выхода из игры ********** 

            if self.gameplay == EXIT:

                sys.exit(0)

            #********** Процесс смерти игрока **********

            if self.gameplay == GAME_OVER:

                self.game_over.draw(self.screen)

                if self.game_over.event() == MENU:

                    self.gameplay = MENU

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
