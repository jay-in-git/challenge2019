# Window hyperparameters
import os.path
from pygame.math import Vector2

game_caption = "Challenge 2019"
screen_size  = (1280, 800)
game_size    = (800, 800)

frame_per_sec = 60

# Table of colors
# Using these monotone colors is discouraged
COLOR_WHITE     = (255, 255, 255)
COLOR_GRAY      = (128, 128, 128)
COLOR_BLACK     = (0, 0, 0)
COLOR_LAVENDER  = (230, 190, 255)
COLOR_NAVY      = (0, 0, 128)
COLOR_BLUE      = (0, 130, 200)
COLOR_TEAL      = (0, 128, 128)
COLOR_CYAN      = (70, 240, 240)
COLOR_GREEN     = (60, 180, 75)
COLOR_MINT      = (170, 255, 195)
COLOR_LIME      = (210, 245, 60)
COLOR_OLIVE     = (128, 128, 0)
COLOR_YELLOW    = (255, 255, 25)
COLOR_BEIGE     = (255, 255, 200)
COLOR_BROWN     = (170, 110, 40)
COLOR_ORANGE    = (245, 130, 48)
COLOR_APRICOT   = (255, 215, 180)
COLOR_MAROON    = (128, 0, 0)
COLOR_RED       = (230, 25, 75)
COLOR_PINK      = (250, 190, 190)
COLOR_GOLD      = (255, 212, 76)
COLOR_KHAKI     = (233, 178, 138)




# Colors of four players
COLOR_PLAYER_BLUE    = (  0, 162, 232)
COLOR_PLAYER_GREEN   = (  6, 203,  56)
COLOR_PLAYER_RED     = (237,  28,  35)
COLOR_PLAYER_ORANGE  = (255, 127,  39)


PLAYER_COLORS=[
    COLOR_WHITE,
    COLOR_GRAY,
    COLOR_LAVENDER,
    COLOR_NAVY,
    COLOR_BLUE,
    COLOR_TEAL,
    COLOR_CYAN,
    COLOR_GREEN,
    COLOR_MINT,
    COLOR_LIME,
    COLOR_OLIVE,
    COLOR_YELLOW,
    COLOR_BEIGE,
    COLOR_BROWN,
    COLOR_ORANGE,
    COLOR_APRICOT,
    COLOR_MAROON,
    COLOR_RED,
    COLOR_PINK
]




# Size
player_height = 100
player_width = 100

# Font
notosans_font = os.path.join('Font', 'Noto', 'NotoSansCJK-Black.ttc')
digitalt_font = os.path.join('Font', 'digitalt', 'Digitalt.ttf')

# Path
IMAGE_PATH = os.path.join('View', 'image')
SOUND_PATH = os.path.join('View', 'sound')
VIDEO_PATH = os.path.join('View', 'video')

# Cut-in parameters
CUTIN_BACKGROUND_PHASE1_TOPLEFT = Vector2(-800, 200)
CUTIN_BACKGROUND_PHASE2_TOPLEFT = Vector2(CUTIN_BACKGROUND_PHASE1_TOPLEFT[0] + 800, CUTIN_BACKGROUND_PHASE1_TOPLEFT[1])
CUTIN_PHASE2_SHIFT = 50
CUTIN_FRONT_PLAYER_PHASE1_TOPLEFT = Vector2(-400, 227)
CUTIN_FRONT_PLAYER_PHASE2_TOPLEFT = Vector2(CUTIN_FRONT_PLAYER_PHASE1_TOPLEFT[0] + 800, CUTIN_FRONT_PLAYER_PHASE1_TOPLEFT[1])
CUTIN_FRONT_PLAYER_PHASE3_TOPLEFT = Vector2(CUTIN_FRONT_PLAYER_PHASE2_TOPLEFT[0] + CUTIN_PHASE2_SHIFT, CUTIN_FRONT_PLAYER_PHASE2_TOPLEFT[1])
CUTIN_FRONT_SKILL_PHASE1_TOPLEFT = Vector2(-890, 235)
CUTIN_FRONT_SKILL_PHASE2_TOPLEFT = Vector2(CUTIN_FRONT_SKILL_PHASE1_TOPLEFT[0] + 800, CUTIN_FRONT_SKILL_PHASE1_TOPLEFT[1])
CUTIN_FRONT_SKILL_PHASE3_TOPLEFT = Vector2(CUTIN_FRONT_SKILL_PHASE2_TOPLEFT[0] + CUTIN_PHASE2_SHIFT, CUTIN_FRONT_SKILL_PHASE2_TOPLEFT[1])
CUTIN_PLAYER_OFFSET = (
    Vector2(-70, 0),
    Vector2(-40, 20),
    Vector2(-70, -5),
    Vector2(-80, -100),
    Vector2(-50, -45),
    Vector2(-110, -150),
    Vector2(-20, 0),
    Vector2(-20, -20),
    Vector2(-90, -45),
    Vector2(-320, -160),
    Vector2(-30, 0),
    Vector2(0, 0),
)
CUTIN_SKILL_OFFSET = {
    'TheWorld': Vector2(0, 0),
    'ShuffleBases': Vector2(20, -30),
    'RadiusNotMove': Vector2(20, -35),
    'FaDaCai': Vector2(110, -10),
}


corner=[
    [0, 0],
    [800, 0],
    [0, 800],
    [800, 800]
]


# RadiationOil
RADIATIONOIL_STAGE1_DURATION = 28
RADIATIONOIL_STAGE2_DURATION = 180
RADIATIONOIL_CENTER_OFFSET = Vector2(-10, -10)
