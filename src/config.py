# Configuration for LED Gesture Control

# GPIO Pin Configuration (Raspberry Pi)
# Adjust these based on your wiring
GPIO_PINS = [17, 27, 22, 24]  # Example GPIO pin numbers for LEDs

# LED Configuration
LED_COUNT = len(GPIO_PINS)
LED_BRIGHTNESS = 255  # 0-255, if using PWM

# Camera Configuration
CAMERA_INDEX = 0  # Default camera index (0 for primary camera)
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FPS = 30

# Gesture Detection Configuration
CONFIDENCE_THRESHOLD = 0.7
DETECTION_TIMEOUT = 2.0  # seconds

# Gesture to LED Mapping
GESTURE_LED_MAP = {
    "THUMBS_UP": 0,
    "PEACE": 1,
    "OPEN_PALM": 2,
    "POINTING": 3,
}

# Platform Detection
IS_RASPBERRY_PI = False  # Set to True when running on Pi

try:
    import RPi.GPIO as GPIO
    IS_RASPBERRY_PI = True
except (ImportError, RuntimeError):
    IS_RASPBERRY_PI = False
