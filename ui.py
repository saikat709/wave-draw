import cv2
from constants import COLOR_RED_BGR

def draw_white_header(img, height=70):
    bg_color       = ( 209, 55, 25 )
    text           = "Wave Draw"
    font           = cv2.FONT_HERSHEY_SIMPLEX
    font_scale     = 1
    font_thickness = 2

    cv2.line(img, (0, height - 1), (img.shape[1], 0), COLOR_RED_BGR, 2)
    cv2.rectangle(img, (0, 0), (img.shape[1], height), bg_color, -1)
    cv2.line(img, (0, height - 1), (img.shape[1], height - 1), COLOR_RED_BGR, 2)
    
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)

    text_x = (img.shape[1] - text_size[0]) // 2
    text_y = (height + text_size[1]) // 2

    cv2.putText(img, text, (text_x, text_y), font, font_scale, (0, 0, 0), font_thickness, cv2.LINE_AA)


def draw_buttons(img, buttons, finger_tip_position = None, on_select = None, selected_btn_id=None, 
                 top = 80, button_height=60, button_width=120, gap=30, 
                ):
    total_width = len(buttons) * button_width + (len(buttons) - 1) * gap
    start_x = (img.shape[1] - total_width) // 2

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    font_thickness = 2

    for i, button in enumerate(buttons):
        x1 = start_x + i * (button_width + gap)
        y1 = top
        x2 = x1 + button_width
        y2 = y1 + button_height

        if finger_tip_position and on_select and x1 <= finger_tip_position[0] <= x2 and y1 <= finger_tip_position[1] <= y2:
            on_select(button["id"])

        selected   = selected_btn_id == button["id"]
        thickness  = -1 if selected else 2
        color      = (0, 255, 0) 
        text_color = (255, 255, 255) if selected else (0, 255, 0 )

        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), thickness)  # border

        text_size, _ = cv2.getTextSize(button["text"], font, font_scale, font_thickness)
        text_x = x1 + (button_width - text_size[0]) // 2
        text_y = y1 + (button_height + text_size[1]) // 2

        cv2.putText(img, button["text"], 
                    (text_x, text_y), 
                    font, font_scale, text_color, 
                    font_thickness, cv2.LINE_AA
                )


def draw_color_selector(img, colors, top=150, size=65, gap=45, selected_clr=None, on_select=None, finger_tip_position=None):
    total_width = len(colors) * size + (len(colors) - 1) * gap
    start_x = (img.shape[1] - total_width) // 2

    for i, clr in enumerate(colors):
        x1 = start_x + i * (size + gap)
        y1 = top
        x2 = x1 + size + 30
        y2 = y1 + size

        if finger_tip_position and on_select and x1 <= finger_tip_position[0] <= x2 and y1 <= finger_tip_position[1] <= y2:
            on_select(clr)

        cv2.rectangle(img, (x1, y1), (x2, y2), clr, -1)

        border_color = (0, 0, 0) if selected_clr != clr else (0, 255, 0)
        cv2.rectangle(img, (x1, y1), (x2, y2), border_color, 3)
    

def draw_shape_selector(img, shapes, top=100, size=65, gap=45, selected_shape=None, on_select=None, finger_tip_position=None):
    """
    shapes = list of strings like ['Circle', 'Rectangle', 'Line']
    """

    total_width = len(shapes) * size + (len(shapes) - 1) * gap
    start_x = (img.shape[1] - total_width) // 2

    for i, shape in enumerate(shapes):
        x1 = start_x + i * (size + gap)
        y1 = top
        x2 = x1 + size + 20
        y2 = y1 + size

        if finger_tip_position and on_select and x1 <= finger_tip_position[0] <= x2 and y1 <= finger_tip_position[1] <= y2:
            on_select(shape)

        cv2.rectangle(img, (x1, y1), (x2, y2), (200, 250, 205), -1)

        center = (x1 + size // 2, y1 + size // 2)
        if shape.lower() == "circle":
            cv2.circle(img, center, size // 3, (0, 0, 255), 2)
        elif shape.lower() == "rectangle":
            cv2.rectangle(img, (x1 + 10, y1 + 10), (x2 - 10, y2 - 10), (0, 255, 0), 2)
        elif shape.lower() == "line":
            cv2.line(img, (x1 + 10, y2 - 10), (x2 - 10, y1 + 10), (255, 0, 0), 2)
        elif shape.lower() == "pen":
            cv2.line(img, (x1 + 10, y2 - 10), (x2 - 10, y1 + 10), (255, 0, 0), 2)
            cv2.line(img, (x1 + size // 2, y1 + size // 2), (x2 - size // 2, y1 + size // 2), (255, 0, 0), 2)

        text_size = cv2.getTextSize(shape, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
        text_x = x1 + (size - text_size[0]) // 2
        text_y = y2 + 20
        cv2.putText(img, shape, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 250, 50), 1)

        border_color = (0, 0, 0) if selected_shape != shape else (0, 255, 0)
        cv2.rectangle(img, (x1, y1), (x2, y2), border_color, 3)




def add_text(img, text, x, y, text_color=(0, 255, 0)):
    font           = cv2.FONT_HERSHEY_SIMPLEX
    font_scale     = 0.8
    font_thickness = 2
    cv2.putText(img, text, (int(x), int(y)), font, font_scale, text_color, font_thickness, cv2.LINE_AA)