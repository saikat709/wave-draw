import cv2
import mediapipe as mp
import math

class HandDetector:
    def __init__(self, mode =False, max_hands=10, model_complexity=1, detection_con=0.5, track_con=0.5):
        self.lm_list = None
        self.results = None
        self.mode = mode
        self.maxHands = max_hands
        self.model_complexity = model_complexity
        self.detection_con = detection_con
        self.track_con = track_con
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.model_complexity,
                                        self.detection_con, self.track_con)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

        self.land_marks = None
        self.finger_status = [0, 0, 0, 0] # [thumb, index, middle, ring, pinky] 0 if closed, 1 if open
        self.has_hand = False
        self.width = 0
        self.height = 0

    def close(self):
        self.hands.close()


    def load_hands(self, img, draw = True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        self.height, self.width, _ = img_rgb.shape

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
                self.has_hand = True
                self.land_marks = handLms
                self._count_fingers()
                # break
        else:
            self.has_hand = False


    def _count_fingers(self):
        if not self.land_marks:
            print("None inside counting")
            return 

        self.finger_status.clear()

        thumb_tip = self.land_marks.landmark[4]
        thumb_mcp = self.land_marks.landmark[2]
        if thumb_tip.x < thumb_mcp.x:
            self.finger_status.append(1)
        else:
            self.finger_status.append(0)

        tips = [8, 12, 16, 20]
        pips = [6, 10, 14, 18]
        for tip_id, pip_id in zip(tips, pips):
            tip = self.land_marks.landmark[tip_id]
            pip = self.land_marks.landmark[pip_id]
            if tip.y < pip.y:  # higher up = open
                self.finger_status.append(1)
            else:
                self.finger_status.append(0)

    def is_thumbs_up(self):
        if not self.land_marks:
            print("None inside thumbs up")
            return False
        
        thumb_tip = self.land_marks.landmark[4]
        thumb_ip  = self.land_marks.landmark[3]
        thumb_mcp = self.land_marks.landmark[2]

        tips = [8, 12, 16, 20]
        pips = [6, 10, 14, 18]

        is_thumb_up = thumb_tip.y < thumb_mcp.y

        fingers_down = True
        for tip_id, pip_id in zip(tips, pips):
            if self.land_marks.landmark[tip_id].y < self.land_marks.landmark[pip_id].y:
                fingers_down = False
                break

        return is_thumb_up and fingers_down and sum(self.finger_status) == 1

    def is_thumbs_down(self):
        if not self.land_marks:
            print("None inside thumbs down")
            return False

        thumb_tip = self.land_marks.landmark[4]
        thumb_mcp = self.land_marks.landmark[2]

        tips = [8, 12, 16, 20]
        pips = [6, 10, 14, 18]

        # Thumb pointing down → tip below mcp
        is_thumb_down = thumb_tip.y > thumb_mcp.y

        # All other fingers should be folded (tip below pip)
        fingers_down = True
        for tip_id, pip_id in zip(tips, pips):
            if self.land_marks.landmark[tip_id].y < self.land_marks.landmark[pip_id].y:
                fingers_down = False
                break

        return is_thumb_down and fingers_down and sum(self.finger_status) == 1


    def drawing_mood(self):
        return ( self.finger_status[1] == 1 and sum(self.finger_status) == 1 )  or ( self.finger_status[1] == 1 and self.finger_status[0] == 1 and sum(self.finger_status) == 2 )

    def tool_selection_mood(self):
        return ( self.finger_status[1] == self.finger_status[2] == 1 and sum(self.finger_status) == 2 ) or (
            self.finger_status[0] == self.finger_status[1] == self.finger_status[2] == 1 and sum(self.finger_status) == 3
        )

    def hand_spread(self):
        return sum(self.finger_status) == 5

    def hand_closed(self):
        return ( sum(self.finger_status) == 0 ) or ( self.finger_status[0] == 1 and sum(self.finger_status) == 1 )

    def find_index_tip_position(self, draw = True):
        index_top = self.land_marks.landmark[8]
        after_index_top = self.land_marks.landmark[12]
        res = None
        if not self.tool_selection_mood():
            res = int(index_top.x * self.width), int(index_top.y * self.height)
        else:
            res = int(after_index_top.x * self.width), int(after_index_top.y * self.height)
        
        return res

    def get_finger_count(self):
        count = 0
        for i in self.finger_status:
            count += i
        return count

    def get_fingers(self):
        return self.finger_status

    def fingers_up(self):
        fingers = []
        if self.lm_list[self.tipIds[0]][1] > self.lm_list[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1, 5):
            if self.lm_list[self.tipIds[id]][2] < self.lm_list[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def find_distance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.lm_list[p1][1:]
        x2, y2 = self.lm_list[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]