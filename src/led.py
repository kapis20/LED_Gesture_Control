"""
LED Control Module
Handles GPIO control for LEDs on Raspberry Pi
"""

import logging
from config import GPIO_PINS, LED_BRIGHTNESS, IS_RASPBERRY_PI

logger = logging.getLogger(__name__)


class LEDController:
    """Control LEDs via GPIO on Raspberry Pi"""

    def __init__(self):
        self.is_available = IS_RASPBERRY_PI
        self.gpio = None
        self.pins = GPIO_PINS

        if self.is_available:
            try:
                import RPi.GPIO as GPIO
                self.gpio = GPIO
                self._initialize_gpio()
            except ImportError:
                logger.warning("RPi.GPIO not available. LED control disabled.")
                self.is_available = False

    def _initialize_gpio(self):
        """Initialize GPIO pins"""
        if not self.is_available or self.gpio is None:
            return

        try:
            self.gpio.setmode(self.gpio.BCM)
            for pin in self.pins:
                self.gpio.setup(pin, self.gpio.OUT)
                self.gpio.output(pin, self.gpio.LOW)
            logger.info(f"GPIO initialized for pins: {self.pins}")
        except Exception as e:
            logger.error(f"Failed to initialize GPIO: {e}")
            self.is_available = False

    def light_led(self, led_index):
        """Turn on a specific LED"""
        if not self.is_available or led_index >= len(self.pins):
            return

        try:
            pin = self.pins[led_index]
            if self.gpio:
                self.gpio.output(pin, self.gpio.HIGH)
                logger.debug(f"LED {led_index} on (GPIO {pin})")
        except Exception as e:
            logger.error(f"Failed to light LED {led_index}: {e}")

    def turn_off_all(self):
        """Turn off all LEDs"""
        if not self.is_available:
            return

        try:
            for pin in self.pins:
                if self.gpio:
                    self.gpio.output(pin, self.gpio.LOW)
            logger.debug("All LEDs turned off")
        except Exception as e:
            logger.error(f"Failed to turn off LEDs: {e}")

    def cleanup(self):
        """Clean up GPIO resources"""
        if self.is_available and self.gpio:
            try:
                self.gpio.cleanup()
                logger.info("GPIO cleaned up")
            except Exception as e:
                logger.error(f"Failed to cleanup GPIO: {e}")
