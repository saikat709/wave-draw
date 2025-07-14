WINDOW_NAME         = "Wave Board"

DEFAULT_FILE_NAME_PREFFIX = "/home/saikat/Downloads/wave_board_output"


HEIGHT              = 670
WIDTH               = 1080
HEADER_HEIGHT       = 60
BUTTON_PANEL_HEIGHT = 50
BUTTON_HEIGHT       = 50
BUTTON_ASPECT_RATIO = float(150/130)  # w/h
SPACING             = 5
PADDING             = 5


BUTTON_SAVE  = 1
BUTTON_PEN   = 2
BUTTON_SHAPE = 3
BUTTON_COLOR = 4
BUTTON_BG    = 5
BUTTON_EXIT  = 6


GESTURE_DRAW   = 100
GESTURE_SELECT = 101
GESTURE_SAVE   = 102
GESTURE_CLEAR  = 103


DRAW_RECT   = 201
DRAW_CIRCLE = 202
DRAW_LINE   = 203
DRAW_POINT  = 204
DRAW_NONE   = 205


COLOR_WHITE     = (255, 255, 255)
COLOR_BLACK     = (  0,   0,   0)
COLOR_GREEN_BGR = (  0, 255,   0)
COLOR_RED_BGR   = (  0,   0, 255)
COLOR_BLUE_BGR  = (255,   0,   0)



BUTTONS = [
    {
        "text": "PEN",
        "id": BUTTON_PEN
    },
    {
        "text": "COLOR",
        "id": BUTTON_COLOR
    },
    {
        "text": "BG COLOR",
        "id": BUTTON_BG
    },
    {
        "text": "SHAPES",
        "id": BUTTON_SHAPE
    },
]


COLORS = [
    COLOR_RED_BGR,
    COLOR_GREEN_BGR,
    COLOR_BLUE_BGR,
    COLOR_BLACK,
    COLOR_WHITE
]