HEIGHT = 650
WIDTH = 850
HEADER_HEIGHT = 60
BUTTON_PANEL_HEIGHT = 50
BUTTON_HEIGHT = 50
BUTTON_ASPECT_RATIO = float(150/130)  # w/h
SPACING = 5
PADDING = 5
WINDOW_NAME = "Wave Board"


SAVE_BUTTON  = 1
PEN_BUTTON   = 2
SHAPE_BUTTON = 3
COLOR_BUTTON = 4
BG_BUTTON    = 5
EXIT_BUTTON  = 6


GESTURE_DRAW   = 100
GESTURE_SELECT = 101
GESTURE_SAVE   = 102

WHITE = (255, 255, 255)
BLACK = ( 0, 0, 0)
GREEN_BGR = (0, 255, 0)
RED_BGR = (0, 0, 255)



BUTTONS = [
    {
        "text": "Pen",
        "toggle": False,
        "id": PEN_BUTTON
    },
    {
        "text": "Color",
        "toggle": False,
        "id": COLOR_BUTTON
    },
    {
        "text": "BG Color",
        "toggle": False,
        "id": SAVE_BUTTON
    },
    {
        "text": "Shapes",
        "toggle": False,
        "id": SAVE_BUTTON
    },
]


COLORS = [
    RED_BGR,
    GREEN_BGR
]