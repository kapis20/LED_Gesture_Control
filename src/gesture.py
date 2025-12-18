"""
Gesture Detection Module
Uses MediaPipe and OpenCV for hand gesture recognition
"""

import logging
import cv2
import mediapipe as mp
from config import CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT, FPS, CONFIDENCE_THRESHOLD

logger = logging.getLogger(__name__)


class GestureDetector:
    """Detect hand gestures using MediaPipe"""

    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=CONFIDENCE_THRESHOLD,
            min_tracking_confidence=0.5,
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.gesture_history = []

    def detect_gesture(self, frame):
        """
        Detect hand gestures in a frame

        Args:
            frame: OpenCV frame

        Returns:
            dict: Detected gesture info or None
        """
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                gesture = self._classify_gesture(hand_landmarks)
                return {"gesture": gesture, "landmarks": hand_landmarks}

        return None

    def _classify_gesture(self, landmarks):
        """
        Classify gesture based on hand landmarks

        Args:
            landmarks: MediaPipe hand landmarks

        Returns:
            str: Gesture name
        """
        # Extract key landmark positions
        thumb_tip = landmarks.landmark[4]
        index_tip = landmarks.landmark[8]
        middle_tip = landmarks.landmark[12]
        ring_tip = landmarks.landmark[16]
        pinky_tip = landmarks.landmark[20]
        palm = landmarks.landmark[0]

        # Simple gesture classification logic
        if self._is_thumbs_up(landmarks):
            return "THUMBS_UP"
        elif self._is_peace(landmarks):
            return "PEACE"
        elif self._is_open_palm(landmarks):
            return "OPEN_PALM"
        elif self._is_pointing(landmarks):
            return "POINTING"

        return "UNKNOWN"

    def _is_thumbs_up(self, landmarks):
        """Check if gesture is thumbs up"""
        thumb_tip = landmarks.landmark[4]
        thumb_ip = landmarks.landmark[3]
        return thumb_tip.y < thumb_ip.y

    def _is_peace(self, landmarks):
        """Check if gesture is peace sign"""
        index_tip = landmarks.landmark[8]
        middle_tip = landmarks.landmark[12]
        ring_tip = landmarks.landmark[16]
        pinky_tip = landmarks.landmark[20]

        # Peace is when index and middle are up, others are down
        return (
            index_tip.y < 0.5
            and middle_tip.y < 0.5
            and ring_tip.y > 0.7
            and pinky_tip.y > 0.7
        )

    def _is_open_palm(self, landmarks):
        """Check if gesture is open palm"""
        thumb_tip = landmarks.landmark[4]
        index_tip = landmarks.landmark[8]
        middle_tip = landmarks.landmark[12]
        ring_tip = landmarks.landmark[16]
        pinky_tip = landmarks.landmark[20]

        # All fingers spread out
        return (
            thumb_tip.y < 0.5
            and index_tip.y < 0.5
            and middle_tip.y < 0.5
            and ring_tip.y < 0.5
            and pinky_tip.y < 0.5
        )

    def _is_pointing(self, landmarks):
        """Check if gesture is pointing"""
        index_tip = landmarks.landmark[8]
        middle_tip = landmarks.landmark[12]
        ring_tip = landmarks.landmark[16]
        pinky_tip = landmarks.landmark[20]

        # Index up, others down
        return (
            index_tip.y < 0.5
            and middle_tip.y > 0.7
            and ring_tip.y > 0.7
            and pinky_tip.y > 0.7
        )

    def draw_landmarks(self, frame, detection):
        """Draw hand landmarks on frame"""
        if detection and "landmarks" in detection:
            self.mp_drawing.draw_landmarks(frame, detection["landmarks"], None)
        return frame

    def cleanup(self):
        """Clean up resources"""
        self.hands.close()
