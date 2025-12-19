import cv2
import mediapipe as mp

import numpy as np

import serial
import time


mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)


def palm_normal_z(lm):
    # 3D points
    p0 = np.array([lm[0].x, lm[0].y, lm[0].z])   # wrist
    p5 = np.array([lm[5].x, lm[5].y, lm[5].z])   # index MCP
    p17 = np.array([lm[17].x, lm[17].y, lm[17].z]) # pinky MCP

    v1 = p5 - p0
    v2 = p17 - p0
    n = np.cross(v1, v2)  # normal vector
    return n[2]   

# Put this near the top (outside loop)
palm_sign = None   # will be +1 or -1 after calibration

def is_palm_facing(lm, handedness_label):
    global palm_sign
    nz = palm_normal_z(lm)
    #revert for right hand because of mirroring in webcam
    if nz is not None and handedness_label == "Right":
        nz = -nz
    # Calibrate the first time you show your PALM to the camera
    if palm_sign is None:
        palm_sign = 1 if nz > 0 else -1
        print("Calibrated palm_sign =", palm_sign)

    # After calibration: palm facing if nz has same sign as palm_sign
    return (nz * palm_sign) > 0




def fingers_up(lm, handedness_label):
    # Returns list: [thumb, index, middle, ring, pinky]
    fingers = [0, 0, 0, 0, 0]

    # Thumb: compare tip (4) with MCP (2) for a more stable baseline
    # Right hand: extended thumb tends to have tip.x > mcp.x
    # Left  hand: extended thumb tends to have tip.x < mcp.x
    #check palm orientation
    palm_facing = is_palm_facing(lm, handedness_label)
    text = "Palm Facing" if palm_facing else "Palm Not Facing"
    cv2.putText(frame, text, (10, 60),  
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)    
    # if palm is not facing, we invert the logic for thumb detection
    while palm_facing:            
        if handedness_label == "Right":
            # Right hand lm is mirrored in webcam
            fingers[0] = 1 if lm[4].x > lm[2].x else 0
        else:  # "Left"
            fingers[0] = 1 if lm[4].x < lm[2].x else 0
        break
    else:
        if handedness_label == "Right":
            fingers[0] = 1 if lm[4].x < lm[2].x else 0
        else:  # "Left"
            fingers[0] = 1 if lm[4].x > lm[2].x else 0


    # Other fingers (y-based)
    fingers[1] = 1 if lm[8].y  < lm[6].y  else 0  # index
    fingers[2] = 1 if lm[12].y < lm[10].y else 0  # middle
    fingers[3] = 1 if lm[16].y < lm[14].y else 0  # ring
    fingers[4] = 1 if lm[20].y < lm[18].y else 0  # pinky

    return fingers

last_gesture = None

from typing import Optional, Sequence, Tuple

FingerState = Tuple[int, int, int, int, int]

# Finger patterns
OPEN      : FingerState = (1, 1, 1, 1, 1)
FIST      : FingerState = (0, 0, 0, 0, 0)
INDEX     : FingerState = (0, 1, 0, 0, 0)
THUMB     : FingerState = (1, 0, 0, 0, 0)
FOUR      : FingerState = (0, 1, 1, 1, 1)
SPIDERMAN : FingerState = (1, 1, 0, 0, 1)
TWO       : FingerState = (0, 1, 1, 0, 0)

GESTURES_ANY = {
    OPEN: "OPEN",
    FIST: "FIST",
    INDEX: "INDEX",
    THUMB: "THUMB",
    FOUR: "FOUR",
    SPIDERMAN: "SPIDERMAN",
}

GESTURES_ORIENTED = {
    TWO: ("PEACE", "V_SIGN"),  # (palm, back)
}

def classify_gesture(f: Sequence[int], palm_facing: bool = True) -> Optional[str]:
    state: FingerState = tuple(f)

    if state in GESTURES_ANY:
        return GESTURES_ANY[state]

    if state in GESTURES_ORIENTED:
        palm_gesture, back_gesture = GESTURES_ORIENTED[state]
        return palm_gesture if palm_facing else back_gesture

    return None



with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.resize(frame, (640, 480))
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            try:
                hand = results.multi_hand_landmarks[0]

                handedness_label = "Right"
                if results.multi_handedness and len(results.multi_handedness) > 0:
                    handedness_label = results.multi_handedness[0].classification[0].label  # "Left" or "Right"

                mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

                lm = hand.landmarks
                f = fingers_up(lm, handedness_label)

                text = f"Thumb:{f[0]} Index:{f[1]} Middle:{f[2]} Ring:{f[3]} Pinky:{f[4]}"
                cv2.putText(frame, text, (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

                print("Fingers:", f)

                # call gesture classification
                gesture = classify_gesture(f, palm_facing=is_palm_facing(lm, handedness_label))
                if gesture != last_gesture and gesture is not None:
                    text = f"Gesture: {gesture}"
                    cv2.putText(frame, text, (10, 90),  
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

            except Exception as e:
                print("ERROR inside hand block:", repr(e))


        cv2.imshow("Finger Detection", frame)
        if (cv2.waitKey(1) & 0xFF) == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
