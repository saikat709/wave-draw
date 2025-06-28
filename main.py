import cv2
from constants import *
import matplotlib.pyplot as plt
from hand_detector import HandDetector
from ui import draw_white_header, draw_buttons, draw_color_selector, add_text


def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"🖱️ Click at: ({x}, {y})")


def main():

    cv2.namedWindow(WINDOW_NAME)
    cv2.setMouseCallback(WINDOW_NAME, on_mouse)
    cap = cv2.VideoCapture(0)
    success, image = cap.read()

    hand_detector = HandDetector()

    click_events = []  # { x1, x2, y1, y2 }

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        image = cv2.resize(image, (WIDTH, HEIGHT))
        image = cv2.flip(image, 1)

        hand_detector.load_hands(image, True)

        if hand_detector.has_hand:
            tx, ty = 10, HEIGHT - 25

            add_text(image, "Finger count: "+ str(hand_detector.get_finger_count()), WIDTH - 250, ty)

            if hand_detector.is_thumbs_up():
                add_text(image, "Thumbs Up", tx, ty)
            if hand_detector.hand_spread():
                add_text(image, "Spread Hand", tx, ty)
            if hand_detector.hand_closed():
                add_text(image, "Hand Closed", tx, ty)
            if hand_detector.tool_selection_mood():
                add_text(image, "Tool Selection Mode", tx, ty)
            if hand_detector.drawing_mood():
                add_text(image, "Drawing Mode", tx, ty)



        # draw ui
        draw_white_header(image)
        draw_buttons(image, BUTTONS)
        draw_color_selector(image, COLORS)

        # showing
        cv2.imshow(WINDOW_NAME, image)
        key = cv2.waitKey(1)

        # Quit on 'q', ESC, or window close button
        if key & 0xFF == ord('q') or key == 27 or cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
            break

    hand_detector.close()
    cap.release()
    # cv2.destroyAllWindows()

if __name__ == "__main__":
    main()