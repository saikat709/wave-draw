import cv2
import mediapipe as mp
from mediapipe.tasks import python
import numpy as np

HEIGHT = 650
WIDTH = 850
HEADER_HEIGHT = 70


def draw_white_header(img, height=70, color=(255, 234, 101)):
    title_w, title_h = 250, 55
    padding_y, padding_x = int( (height - title_h ) / 2 ), 10
    cv2.rectangle(img, (0, 0), (img.shape[1], height), color, -1)
    title = cv2.imread("./images/title_bg.png", cv2.IMREAD_COLOR)
    title_resized = cv2.resize(title, (title_w, title_h))
    img[padding_y: padding_y + title_h, padding_x: padding_x + title_w] = title_resized

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='./models/hand_landmarker.task'),
    running_mode=VisionRunningMode.IMAGE
)

cap = cv2.VideoCapture(0)

with HandLandmarker.create_from_options(options) as landmarker:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (850, 650))
        flipped = cv2.flip(frame, 1)
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        draw_white_header(frame)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.asarray(frame))
        result = landmarker.detect(mp_image)
        print(result)

        if result.hand_landmarks:
            for hand in result.hand_landmarks:
                for lm in hand:
                    cx, cy = int(lm.x * WIDTH), int(lm.y * HEIGHT)
                    cv2.circle(frame, (cx, cy), 4, (0, 255, 0), -1)

        cv2.imshow("WaveBoard Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
