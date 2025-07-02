import cv2
from constants import *
import matplotlib.pyplot as plt
from hand_detector import HandDetector
from drawing import Drawing
from ui import draw_white_header, draw_buttons, draw_color_selector, add_text


hand_detector = HandDetector()
drawing = Drawing()

current_draw    = DRAW_POINT
selected_color  = COLOR_GREEN_BGR
show_finger_tip = False
selected_btn_id = BUTTON_PEN


def on_tools_selected(btn_id):
        global selected_btn_id, current_gesture, current_draw
        selected_btn_id = btn_id


        if btn_id == BUTTON_PEN:
            current_draw = DRAW_POINT
        if btn_id == BUTTON_COLOR:
            current_gesture = GESTURE_SELECT
        if btn_id == BUTTON_BG: 
            current_gesture = GESTURE_SELECT
        if btn_id == BUTTON_SHAPE:
            current_gesture = GESTURE_SELECT


def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Mouse click at: ({x}, {y})")


def main():

    cv2.namedWindow(WINDOW_NAME)
    cv2.setMouseCallback(WINDOW_NAME, on_mouse)
    cap = cv2.VideoCapture(0)


    while cap.isOpened():
        show_finger_tip = False
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        image = cv2.resize(image, (WIDTH, HEIGHT))
        image = cv2.flip(image, 1)

        hand_detector.load_hands(image, True)

        if hand_detector.has_hand:
            tx, ty = 10, HEIGHT - 25

            add_text(image, "Finger count: " + str(hand_detector.get_finger_count()), WIDTH - 250, ty)

            if hand_detector.is_thumbs_up():
                add_text(image, "Thumbs Up", tx, ty)
                current_gesture = GESTURE_SAVE
                drawing.last_point = None

            elif hand_detector.hand_spread():

                add_text(image, "Spread Hand", tx, ty)
                current_gesture = None
                drawing.last_point = None


            elif hand_detector.hand_closed():
                add_text(image, "Hand Closed", tx, ty)
                current_gesture = None
                drawing.last_point = None


            elif hand_detector.tool_selection_mood():
                show_finger_tip = True
                add_text(image, "Tool Selection Mode", tx, ty)
                current_gesture = GESTURE_SELECT
                drawing.last_point = None

            elif hand_detector.drawing_mood():
                
                show_finger_tip = True
                add_text(image, "Drawing Mode", tx, ty)
                center = hand_detector.find_index_tip_position()

                if drawing.last_point is not None and drawing.last_point != center:
                    drawing.add_line(drawing.last_point.x, drawing.last_point.y, center[0], center[1])
                
                drawing.add_point(center[0], center[1])

            else:
                drawing.last_point = None
                add_text(image, "Unknown gesture ", tx, ty)

        else:
            add_text(image, "No hand detected", 10, HEIGHT - 25)
            current_gesture = None

        
        image = drawing.draw(image)
        # draw ui
        # draw_white_header(image)

        if show_finger_tip:
            center = hand_detector.find_index_tip_position()
            cv2.circle(image, center=center, 
                       radius=10, 
                       color=(0, 250, 0), 
                       thickness=cv2.FILLED
                    )

        if current_gesture == GESTURE_SELECT:
            center = hand_detector.find_index_tip_position()
            draw_buttons(image, BUTTONS, top=10,  selected_btn_id = selected_btn_id,
                         finger_tip_position = center, 
                         on_select = lambda x: on_tools_selected(x),
            )
        else:
            draw_buttons(image, BUTTONS, selected_btn_id = selected_btn_id, top=10)

        draw_color_selector(image, COLORS, top=85)



        # showing
        cv2.imshow(WINDOW_NAME, image)
        key = cv2.waitKey(1)

        # Quit on 'q', ESC, or window close button
        if ( 
            key & 0xFF == ord('q') 
            or key == 27 
            or cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1 
        ):
            break

    hand_detector.close()
    cap.release()
    # cv2.destroyAllWindows()

if __name__ == "__main__":
    main()