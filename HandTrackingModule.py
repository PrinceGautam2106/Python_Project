import cv2
import mediapipe as mp
import numpy as np
from pynput.mouse import Controller, Button

mouse = Controller()

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Smoothing factor
smoothening = 7
prev_x, prev_y = 0, 0

# Set your screen resolution
screen_w = 1440
screen_h = 900

cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
) as hands:

    while True:
        ret, img = cap.read()
        img = cv2.flip(img, 1)

        h, w, _ = img.shape

        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            lm_list = []

            for id, lm in enumerate(hand.landmark):
                lm_x, lm_y = int(lm.x * w), int(lm.y * h)
                lm_list.append((lm_x, lm_y))

            # Landmarks
            index_x, index_y = lm_list[8]   # Index tip
            middle_x, middle_y = lm_list[12] # Middle tip
            thumb_x, thumb_y = lm_list[4]   # Thumb tip

            # ------------------------------
            # 1) Move mouse with index finger
            # ------------------------------
            target_x = np.interp(index_x, (0, w), (0, screen_w))
            target_y = np.interp(index_y, (0, h), (0, screen_h))

            curr_x = prev_x + (target_x - prev_x) / smoothening
            curr_y = prev_y + (target_y - prev_y) / smoothening

            mouse.position = (curr_x, curr_y)
            prev_x, prev_y = curr_x, curr_y

            cv2.circle(img, (index_x, index_y), 10, (255, 0, 255), -1)

            # ------------------------------
            # 2) Left click (index + middle touching)
            # ------------------------------
            distance_click = np.hypot(index_x - middle_x, index_y - middle_y)

            if distance_click < 30:# changable 
                cv2.putText(img, "CLICK", (index_x, index_y - 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                mouse.click(Button.left, 1)

            # ------------------------------
            # 3) Scroll with thumb + index
            # ------------------------------
            distance_scroll = np.hypot(index_x - thumb_x, index_y - thumb_y)

            cv2.putText(img, f"Scroll Dist: {int(distance_scroll)}",
                        (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

            if distance_scroll < 30:     # Close → Scroll down
                mouse.scroll(0, -1)
                cv2.putText(img, "SCROLL DOWN",
                            (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            elif distance_scroll > 80:   # Far → Scroll up
                mouse.scroll(0, 1)
                cv2.putText(img, "SCROLL UP",
                            (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

            mp_drawing.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)

        cv2.imshow("Hand Control", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
