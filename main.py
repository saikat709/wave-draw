import cv2
import mediapipe as mp
from constants import *
from math import hypot


def is_click_gesture(landmarks):
    x1, y1 = landmarks[8].x, landmarks[8].y  # index tip
    x2, y2 = landmarks[4].x, landmarks[4].y  # thumb tip
    distance = hypot(x2 - x1, y2 - y1)
    return distance < 0.05

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

cv2.namedWindow(WINDOW_NAME)
cap = cv2.VideoCapture(0)


click_events = []  # { x1, x2, y1, y2 }


def draw_white_header(img, height=70):
    bg_color = (209, 55, 25)
    cv2.line(img, (0, height - 1), (img.shape[1], 0), RED_BGR, 2)
    cv2.rectangle(img, (0, 0), (img.shape[1], height), bg_color, -1)
    cv2.line(img, (0, height - 1), (img.shape[1], height - 1), RED_BGR, 2)
    text = "Wave Draw"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)

    text_x = (img.shape[1] - text_size[0]) // 2
    text_y = (height + text_size[1]) // 2

    cv2.putText(img, text, (text_x, text_y), font, font_scale, (0, 0, 0), font_thickness, cv2.LINE_AA)


def draw_buttons(img, buttons, top=80, button_height=60, button_width=120, gap=20, color=(220, 220, 220), text_color=(0, 0, 0)):
    total_width = len(buttons) * button_width + (len(buttons) - 1) * gap
    start_x = (img.shape[1] - total_width) // 2

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    font_thickness = 1

    for i, button in enumerate(buttons):
        x1 = start_x + i * (button_width + gap)
        y1 = top
        x2 = x1 + button_width
        y2 = y1 + button_height

        # Draw button rectangle
        cv2.rectangle(img, (x1, y1), (x2, y2), color, -1)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), 1)  # border

        # Calculate centered text
        text_size, _ = cv2.getTextSize(button["text"], font, font_scale, font_thickness)
        text_x = x1 + (button_width - text_size[0]) // 2
        text_y = y1 + (button_height + text_size[1]) // 2

        cv2.putText(img, button["text"], (text_x, text_y), font, font_scale, text_color, font_thickness, cv2.LINE_AA)


def draw_color_selector(img, colors, top=150, size=40, gap=20, selected_index=None):
    total_width = len(colors) * size + (len(colors) - 1) * gap
    start_x = (img.shape[1] - total_width) // 2

    for i, clr in enumerate(colors):
        x1 = start_x + i * (size + gap)
        y1 = top
        x2 = x1 + size
        y2 = y1 + size

        # Draw filled color box
        cv2.rectangle(img, (x1, y1), (x2, y2), clr, -1)

        # Border: highlight if selected
        border_color = (0, 0, 0) if selected_index != i else (0, 255, 0)
        cv2.rectangle(img, (x1, y1), (x2, y2), border_color, 2)

        # Optionally, you can store the bounding box for click detection
        # e.g. color_boxes.append((x1, y1, x2, y2))

def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"🖱️ Click at: ({x}, {y})")

cv2.setMouseCallback(WINDOW_NAME, on_mouse)


while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    image = cv2.resize(image, (WIDTH, HEIGHT))
    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

    results = hands.process(image_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # print(hand_landmarks)
            if is_click_gesture(hand_landmarks.landmark):
                print("This is a click gesture")
            mp_drawing.draw_landmarks(
                image_bgr, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    h = HEADER_HEIGHT + SPACING + BUTTON_PANEL_HEIGHT
    color = (255, 255, 255)
    # cv2.rectangle(image_bgr, (0, 0), (image_bgr.shape[1], h), color, -1)
    draw_white_header(image_bgr)
    draw_buttons(image_bgr, BUTTONS)
    draw_color_selector(image_bgr, COLORS)

     # showing
    cv2.imshow(WINDOW_NAME, image_bgr)
    key = cv2.waitKey(1)

    # Quit on 'q', ESC, or window close button
    if key & 0xFF == ord('q') or key == 27 or cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
        break

hands.close()
cap.release()
cv2.destroyAllWindows()