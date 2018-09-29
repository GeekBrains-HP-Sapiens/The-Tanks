# *************** settings window ***************

WIDTH_WIN = 1024

HEIGHT_WIN = 768

# *************** settings world_1 ***************

# *************** settings sprite

PLAYER_TANK = 'Image/world_1/tanks/tank-player-1.png'

ENEMY_TANK = 'Image/world_1/tanks/tank-enemy-1.png'

BLOCK_DESTRUCT_1 = 'Image/world_1/block/1.1.png'

BLOCK_DESTRUCT_2 = 'Image/world_1/block/1.2.png'

BLOCK_DESTRUCT_3 = 'Image/world_1/block/1.3.png'

BLOCK_UNDESTRUCT = 'Image/world_1/block/2.bmp'

BASE = 'Image/world_1/block/base2.png'

PLAYER_BULLET = 'Image/world_1/bullet/bulletBlue.png'

ENEMY_BULLET = 'Image/world_1/bullet/bulletRed.png'

WALLPAPER = 'Image/world_1/wallpaper/set8_example_5.png'

GAME_OVER = 'Image/gameplay/game_over.png'

MENU = 'Image/menu/menu_back1.jpg'

# *************** settings sprite button

BUTTON_ON = [('Image/button/button_ng_on.png'),
             ('Image/button/button_cont_on.png'),
             ('Image/button/button_settings_on.png'),
             ('Image/button/button_exit_on.png')]

BUTTON_OFF = [('Image/button/button_ng_off.png'),
             ('Image/button/button_cont_off.png'),
             ('Image/button/button_settings_off.png'),
             ('Image/button/button_exit_off.png')]

# *************** other settings

ANIMATION_EXPLOSIONS = [('Image/world_1/explosions/v_4/4.1.png'),
                        ('Image/world_1/explosions/v_4/4.2.png'),
                        ('Image/world_1/explosions/v_4/4.3.png'),
                        ('Image/world_1/explosions/v_4/4.4.png'),
                        ('Image/world_1/explosions/v_4/4.5.png'),
                        ('Image/world_1/explosions/v_4/4.6.png'),
                        ('Image/world_1/explosions/v_4/4.7.png'),
                        ('Image/world_1/explosions/v_4/4.8.png'),
                        ('Image/world_1/explosions/v_4/4.9.png'),
                        ('Image/world_1/explosions/v_4/4.10.png'),
                        ('Image/world_1/explosions/v_4/4.11.png'),
                        ('Image/world_1/explosions/v_4/4.12.png')]

BLOCK_LIFE = 3

ENEMY_HEALTH = 2

PLAER_HEALTH = 3

SPEED_PLAYER = 3

SPEED_ENEMY = 1

LEVEL_1 = ['Maps/level1.txt', 'Maps/level2.txt','Maps/level3.txt']

# *************** sound settings

SOUNDTRACK_1 = 'Sound/world_1/Target position.mp3'

SOUND_SHOT_1 = 'Sound/world_1/Bullet_shot.wav'

SOUND_BONUS_1 = 'Sound/world_1/Bonus_take.wav'

SOUND_GAME_OVER = 'Sound/world_1/GameOver.wav'

SOUND_MENU = 'Sound/menu/beep.wav'


# *************** size elems ***************

SIZE_BLOCK = 32

SIZE_H = 32

SIZE_W = 32

SIZE_ELEM = (SIZE_H, SIZE_W)

WHITE = (255, 255, 255)  # цвет текста для счета

