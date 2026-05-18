import cv2
import mediapipe as mp
from mac_keys import (
    up_pressed, down_pressed,
    left_pressed, right_pressed,
    PressKey, ReleaseKey
)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

video = cv2.VideoCapture(0)
current_key = None

# Finger tip IDs
tips = [4, 8, 12, 16, 20]

def count_fingers(landmarks):
    fingers = []

    # Thumb (check x difference)
    if landmarks[tips[0]].x > landmarks[tips[0] - 1].x:
        fingers.append(1)   # Thumb open
    else:
        fingers.append(0)

    # Other 4 fingers (compare y)
    for i in range(1,5):
        if landmarks[tips[i]].y < landmarks[tips[i] - 2].y:
            fingers.append(1)   # Finger open
        else:
            fingers.append(0)

    return fingers  # List of 0/1


def execute_action(fingers):
    global current_key

    total = sum(fingers)

    desired = None

    # ✊ Only index finger → JUMP
    if fingers == [0,1,0,0,0]:
        desired = up_pressed

    # 👍 Only thumb → SLIDE
    elif fingers == [1,0,0,0,0]:
        desired = down_pressed

    # 🖐 Five fingers → LEFT
    elif total == 5:
        desired = left_pressed

    # 🖐 Four fingers → RIGHT
    elif total == 4:
        desired = right_pressed

    # ---- KEY PRESS HANDLING ----
    if desired != current_key:
        if current_key:
            ReleaseKey(current_key)
        if desired:
            PressKey(desired)
        current_key = desired


with mp_hands.Hands(min_detection_confidence=0.5,
                    min_tracking_confidence=0.5) as hands:

    while True:
        ret, image = video.read()
        if not ret:
            continue

        imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]

            mp_draw.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)

            fingers = count_fingers(hand.landmark)
            execute_action(fingers)

        else:
            if current_key:
                ReleaseKey(current_key)
                current_key = None

        cv2.imshow("Gesture Control", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if current_key:
    ReleaseKey(current_key)

video.release()
cv2.destroyAllWindows()
