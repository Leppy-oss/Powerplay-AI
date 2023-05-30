DEBUG = True # renders bounding boxes, vectors, etc.

RES_URL = 'game/res/'
FPS = 60
GAME_DIM = 1000
GAME_DIM_FT = 12 # how wide the screen is in real life ft. (field dimensions)
PX_PER_INCH = GAME_DIM / GAME_DIM_FT / 12
WALL_THICKNESS = 10
ACC = 100
DEFAULT_BB_OFFSET_X_SCALE = 0.25
DEFAULT_BB_OFFSET_Y_SCALE = 0.5
MAX_ROBOT_SPEED = 300 # in units/s
GOAL_RADIUS = 50 # px, obviously
JUNCTION_RADIUS = 10
FORCE_SCALING_FACTOR = 100 # scales forces so they have a sensible magnitude
RED_ALLIANCE = 'RED'
BLUE_ALLIANCE = 'BLUE'
RED_COLOR = (237, 73, 62, 255)
BLUE_COLOR = (62, 103, 237, 255)
GRAY_COLOR = (34, 35, 38)
CONE_RADIUS = 15
WORLD_COLLIDE_TYPE = 0 # basically just the walls
ROBOT_COLLIDE_TYPE = 1
ROBOT_BB_COLLIDE_TYPE = 2
CONE_COLLIDE_TYPE = 3
JUNCTION_COLLIDE_TYPE = 1000
DEFAULT_ROBOT_WIDTH = 14
DEFAULT_ROBOT_HEIGHT = 14
# rounded figures for gobilda 96mm
DEFAULT_WHEEL_WIDTH = 3
DEFAULT_WHEEL_HEIGHT = 5
ROBOT_BB_SCALING_FACTOR = 3

def PX(inches: float) -> float:
    return PX_PER_INCH * inches

def NORM_ROBOT(dim: float, robot_width: float) -> float:
    return robot_width / DEFAULT_ROBOT_WIDTH * dim

def INCHES(px: float) -> float:
    return px / PX_PER_INCH