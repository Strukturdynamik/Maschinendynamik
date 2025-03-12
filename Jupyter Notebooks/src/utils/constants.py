import math

# gui
NUM_TIME_UNITS = 20
NUM_DATAPOINTS = 500  # 1000
DEFAULT_FRAME = 0
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600
X_LIM_START = 0
X_LIM_END = NUM_TIME_UNITS
Y_LIM_START = -0.2
Y_LIME_END = 0.2

# calculations
START_DEFLECTION = math.pi / 18
START_VELOCITY = 0
MASS = 1
DEFAULT_C = 5.0
DEFAULT_C_MAX = 5.0
DEFAULT_D = 0.5
DEFAULT_M = 1
DEFAULT_M_MAX = 5.0

# drawing still modules
NUM_TICKS_X = 5
NUM_TICKS_Y = 6
DIRECTIONS = {
    "right": (-1, 1),
    "left": (-1, 1),
    "bottom": (-1, 1),
    "top": (1, -1),
}
# DIRECTION_FDE = {
#     "vertical": None,
#     "left_to_right": None,
#     "right_to_left": None,
# }
X_ORIGIN = 20
Y_ORIGIN = 55
Y_AX_TOP = 40  # 30
Y_AX_BOTTOM = 40  # 30
X_AX_RIGHT = 70
