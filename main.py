import cv2
import mediapipe as mp

HEIGHT = 650
WIDTH = 850
HEADER_HEIGHT = 70
WINDOW_NAME = "Wave Board"


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                      max_num_hands=2,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

cv2.namedWindow(WINDOW_NAME)
cap = cv2.VideoCapture(0)

def draw_white_header(img, height=70, color=(255, 234, 101)):
    title_w, title_h = 250, 55
    padding_y, padding_x = int( (height - title_h ) / 2 ), 10
    cv2.rectangle(img, (0, 0), (img.shape[1], height), color, -1)
    title = cv2.imread("./images/title_bg.png", cv2.IMREAD_COLOR)
    title_resized = cv2.resize(title, (title_w, title_h))
    img[padding_y: padding_y + title_h, padding_x: padding_x + title_w] = title_resized


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
            mp_drawing.draw_landmarks(
                image_bgr, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    draw_white_header(image_bgr)
    cv2.imshow(WINDOW_NAME, image_bgr)
    key = cv2.waitKey(1)

    # Quit on 'q', ESC, or window close button
    if key & 0xFF == ord('q') or key == 27 or cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
        break

hands.close()
cap.release()
cv2.destroyAllWindows()