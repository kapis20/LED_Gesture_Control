import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

def fingers_up(lm):
    # Returns list: [thumb, index, middle, ring, pinky]
    fingers = [0, 0, 0, 0, 0]

    # THUMB (simple x-based rule; works well for many angles)
    fingers[0] = 1 if lm[4].x > lm[3].x else 0

    # Other fingers (y-based)
    fingers[1] = 1 if lm[8].y  < lm[6].y  else 0  # index
    fingers[2] = 1 if lm[12].y < lm[10].y else 0  # middle
    fingers[3] = 1 if lm[16].y < lm[14].y else 0  # ring
    fingers[4] = 1 if lm[20].y < lm[18].y else 0  # pinky

    return fingers

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.resize(frame, (640, 480))
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            lm = hand.landmark
            f = fingers_up(lm)

            text = f"Thumb:{f[0]} Index:{f[1]} Middle:{f[2]} Ring:{f[3]} Pinky:{f[4]}"
            cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

            print("Fingers:", f)

        cv2.imshow("Finger Detection", frame)
        if (cv2.waitKey(1) & 0xFF) == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
