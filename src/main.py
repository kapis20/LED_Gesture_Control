"""
LED Gesture Control Main Application
Combines gesture detection with LED control
"""

import logging
import cv2
import sys
import time
from gesture import GestureDetector
from led import LEDController
from config import (
    CAMERA_INDEX,
    FRAME_WIDTH,
    FRAME_HEIGHT,
    FPS,
    GESTURE_LED_MAP,
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class GestureControlApp:
    """Main application for LED gesture control"""

    def __init__(self):
        self.gesture_detector = GestureDetector()
        self.led_controller = LEDController()
        self.cap = None
        self.running = False
        self.last_gesture_time = 0
        self.gesture_timeout = 2.0

    def initialize_camera(self):
        """Initialize camera capture"""
        try:
            self.cap = cv2.VideoCapture(CAMERA_INDEX)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
            self.cap.set(cv2.CAP_PROP_FPS, FPS)
            logger.info(f"Camera initialized (index: {CAMERA_INDEX})")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize camera: {e}")
            return False

    def run(self):
        """Main application loop"""
        if not self.initialize_camera():
            logger.error("Cannot start application without camera")
            return

        self.running = True
        logger.info("Starting LED Gesture Control application")

        try:
            while self.running:
                ret, frame = self.cap.read()
                if not ret:
                    logger.warning("Failed to read frame")
                    break

                # Detect gesture
                detection = self.gesture_detector.detect_gesture(frame)

                if detection:
                    gesture = detection["gesture"]
                    logger.info(f"Detected gesture: {gesture}")

                    # Control LED based on gesture
                    if gesture in GESTURE_LED_MAP:
                        led_index = GESTURE_LED_MAP[gesture]
                        self.led_controller.light_led(led_index)
                        self.last_gesture_time = time.time()

                # Draw landmarks on frame
                frame = self.gesture_detector.draw_landmarks(frame, detection)

                # Display frame
                cv2.imshow("LED Gesture Control", frame)

                # Check for timeout to turn off LEDs
                if (
                    time.time() - self.last_gesture_time > self.gesture_timeout
                    and self.last_gesture_time != 0
                ):
                    self.led_controller.turn_off_all()
                    self.last_gesture_time = 0

                # Exit on 'q' key
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    self.running = False

        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        except Exception as e:
            logger.error(f"Application error: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up resources"""
        logger.info("Cleaning up resources")
        self.running = False

        if self.cap:
            self.cap.release()

        cv2.destroyAllWindows()
        self.gesture_detector.cleanup()
        self.led_controller.turn_off_all()
        self.led_controller.cleanup()
        logger.info("Cleanup complete")


if __name__ == "__main__":
    app = GestureControlApp()
    app.run()
