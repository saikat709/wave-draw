import cv2
import time
import numpy as np

from constants import *
from hand_detector import HandDetector
from drawing import Drawing
from ui import (
    add_text,
    draw_buttons,
    draw_color_selector, 
    draw_shape_selector
)
from utils import get_timestamp_filename

hand_detector = HandDetector()
drawing = Drawing()


current_gesture    = None
current_draw       = DRAW_POINT
show_finger_tip    = False
selected_btn_id    = BUTTON_PEN
previous_btn_id    = None
selected_shape     = "Pen"
is_shape_completed = True

show_notification       = False
notification_start_time = None
saved_filename          = None
notification_text       = "Drawing saved!"


shapes = ['Circle', 'Rect', 'Line', 'Pen']


def on_shape_selected(shape):
    global selected_shape, selected_btn_id, previous_btn_id
    selected_shape = shape



def on_color_selected(clr):
    global drawing, selected_btn_id, previous_btn_id, current_draw
    if selected_btn_id == BUTTON_BG:
        drawing.background_color = clr
    else:
        drawing.selected_color = clr


def on_tools_selected(btn_id):
    global selected_btn_id, current_gesture, current_draw, previous_btn_id 
    selected_btn_id = btn_id



def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Mouse click at: ({x}, {y})")


def save_drawing(frame):
    global drawing, saved_filename
    if not saved_filename:
        saved_filename = get_timestamp_filename()
    
    new_frame = np.zeros_like(frame)
    new_frame[:] = drawing.background_color
    
    new_frame = drawing.draw(new_frame)

    cv2.imwrite(saved_filename, new_frame)


def main():
    global current_gesture, selected_btn_id, selected_shape
    global show_notification, notification_start_time, saved_filename, notification_text

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

            if not hand_detector.is_thumbs_up():
                saved_filename = None

            if hand_detector.is_thumbs_up():
                add_text(image, "Save (Thumbs Up)", tx, ty)
                current_gesture = GESTURE_SAVE
                notification_start_time = time.time()
                show_notification = True
                notification_text = "Drawing saved!"
                save_drawing(image)
                drawing.clear_all()

            elif hand_detector.is_thumbs_down():
                add_text(image, "Clear (Thumbs Down)", tx, ty)
                drawing.clear_all()
                show_notification = True
                current_gesture = GESTURE_CLEAR
                notification_start_time = time.time()
                notification_text = "Drawing cleared!"

            elif hand_detector.hand_spread():

                add_text(image, "Spread Hand", tx, ty)
                current_gesture = None
                drawing.last_point = None


            elif hand_detector.hand_closed():
                add_text(image, "Hand Closed", tx, ty)
                current_gesture = None
                drawing.last_point = None
                selected_btn_id = BUTTON_PEN
                is_shape_completed = True


            elif hand_detector.tool_selection_mood():
                show_finger_tip = True
                add_text(image, "Tool Selection Mode", tx, ty)
                current_gesture = GESTURE_SELECT
                drawing.last_point = None

            elif hand_detector.drawing_mood() and current_draw == DRAW_POINT:
                
                show_finger_tip = True
                add_text(image, "Drawing Mode", tx, ty)
                center = hand_detector.find_index_tip_position()

                if selected_shape == "Pen":
                    if drawing.last_point is not None and drawing.last_point != center:
                        drawing.add_line(drawing.last_point.x, drawing.last_point.y, center[0], center[1])
                    drawing.add_point(center[0], center[1])
                
                elif selected_shape == "Line":
                    if is_shape_completed:
                        drawing.add_line(center[0], center[1], center[0], center[1])
                        is_shape_completed = False
                        print(f"Added line with start point: {center}")
                    else:
                        drawing.update_line(center[0], center[1])
                        print(f"Updated line with end point: {center}")

                elif selected_shape == "Rect":
                    if is_shape_completed:
                        drawing.add_rectangle(center[0], center[1], center[0], center[1])
                        is_shape_completed = False
                        print(f"Added rectangle with top-left: {center}")
                    else:
                        drawing.update_rectangle(center[0], center[1])
                        print(f"Updated rectangle with bottom-right: {center}")

                elif selected_shape == "Circle":
                    print(f"Selected shape: {selected_shape}, Is_shape_completed: {is_shape_completed}")
                    if is_shape_completed:
                        drawing.add_circle(center[0], center[1])
                        is_shape_completed = False
                        print(f"Added circle with center: {center}")
                    else:
                        drawing.update_circle(center[0], center[1])
                        print(f"Updated circle with center: {center}")

            else:
                is_shape_completed = True
                drawing.last_point = None
                selected_btn_id = BUTTON_PEN
                add_text(image, "Unknown gesture ", tx, ty)

        else:
            add_text(image, "No hand detected", 10, HEIGHT - 25)
            current_gesture = None
            selected_btn_id = BUTTON_PEN
            is_shape_completed = True

        
        image = drawing.draw(image)
        
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
                         on_select = on_tools_selected,
            )
            if selected_btn_id == BUTTON_COLOR or selected_btn_id == BUTTON_BG:
                clr = drawing.selected_color if selected_btn_id == BUTTON_COLOR else drawing.background_color
                draw_color_selector(image, COLORS, top=85, selected_clr = clr,
                                finger_tip_position = center, 
                                on_select = on_color_selected
                )
            if selected_btn_id == BUTTON_SHAPE:
                draw_shape_selector(image, shapes, 
                                selected_shape=selected_shape, 
                                finger_tip_position=center, 
                                on_select = on_shape_selected
                            )
        else:
            draw_buttons(image, BUTTONS, selected_btn_id = selected_btn_id, top=10)

        
        if show_notification:
            elasped_time = time.time() - notification_start_time
            if elasped_time < 3:
                add_text(image, "Drawing saved!", WIDTH/2 - 130, HEIGHT/2 - 25, text_color=(0, 255, 0))
            else:
                show_notification = False
                notification_start_time = None

        add_text(image, "Pen Color", 10, HEIGHT - 60, text_color=drawing.selected_color)
        add_text(image, "Background Color.", 10, HEIGHT - 95, text_color=drawing.background_color)
        add_text(image, "Selected drawing: " + ( "Pen" if selected_shape is None 
                                                else selected_shape.upper() ), 10, HEIGHT - 130)
        
        cv2.imshow(WINDOW_NAME, image)
        key = cv2.waitKey(1)

        if ( 
            key & 0xFF == ord('q') 
            or key == 27 
            or cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1 
        ):
            break

    hand_detector.close()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()