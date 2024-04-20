WIDTH = 816 # 1088
HEIGHT = 480
HONK_FONT = "fonts/Honk-Regular.ttf"
FRAMERATE = 10
GAME_NAME = "Log Raises Game"
GRAVITY = -20
INTERMISSION_BG_COLOR = (254, 252, 232)
TITLE_FONT_SIZE = 60
TEXT_FONT_SIZE = 40
# TEXT_FONT_COLOUR = (95, 127, 207)
TEXT_FONT_COLOUR = (69, 26, 3)
SCORE_FONT_COLOUR = (15, 31, 31)

START_GAME_INTERVAL = 3 # seconds
# SET_INTERVAL = 2
REP_INTERVAL = 3
REST_INTERVAL = 3
TIME_DELAY = 0.3 # to have time to see updated text

NUM_SETS = 2
NUM_REPS = 2

PLAYER_WALKING_IMAGES = ('graphics/player/walk/walk1.png', 'graphics/player/walk/walk3.png')
PLAYER_FLYING_IMAGE = 'graphics/player/jump/jump4.png'

# PARENT_FOLDER = '/home/12Cents/Desktop/DTI'
PARENT_FOLDER = '/Users/yongjun/Documents/Projects/DTI'
# PLAYER_WALKING_IMAGES = 'graphics/player/Cyborg_Walk.png'
PLAYER_WALK_NUM_IMGS = 10
PLAYER_WALK_IMG_PATH = 'graphics/player/walk/walk'
PLAYER_JUMP_NUM_IMGS = 4
PLAYER_JUMP_IMG_PATH = 'graphics/player/jump/jump'
PLAYER_IDLE_NUM_IMGS = 4
PLAYER_IDLE_IMG_PATH = 'graphics/player/idle/idle'
PLAYER_DUCK_NUM_IMGS = 5
PLAYER_DUCK_IMG_PATH = 'graphics/player/duck/duck'
# PLAYER_FLYING_IMAGE = 'graphics/player/jump.png'
PLAYER_MIDBOTTOM_X = 40
PLAYER_MIDBOTTOM_Y = 470

HORIZONTAL_OBSTACLE_IMG_PATH = 'graphics/obstacles/obstacle_horiz_stacked.png'
VERTICAL_OBSTACLE_IMG_PATH = 'graphics/obstacles/obstacle_vert.png'
HORIZONTAL_POLICE_OBSTACLE_IMG_PATH = 'graphics/obstacles/v-police.png'
VERTICAL_YELLOW_OBSTACLE_IMG_PATH = 'graphics/obstacles/v-yellow.png'

SKY_UPPER_Y = 200
GROUND_UPPER_Y = 470

# Encoder
# S1 = 7 # green - CE1
# S2 = 8 # yellow - CE0
S2 = 7 # green - CE1
S1 = 8 # yellow - CE0
# need to lift log faster for it to be more negative
LIFT = -5
WALK = -3
INITIAL = 0