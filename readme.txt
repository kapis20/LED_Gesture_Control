# Hand Gesture Controlled LED Strip (MediaPipe + Arduino + FastLED)

Control a WS2812B (NeoPixel-style) LED strip using hand gestures captured by a webcam.  
A Python script detects gestures with **MediaPipe Hands**, then sends a **serial command** to an **Arduino** which runs **FastLED** animations.

This repo contains:
- `gesture_control.py` → main gesture → serial command controller
- `LED_Colours_control.ino` → Arduino/FastLED modes + serial menu
- `gesture.py` → simple MediaPipe demo (useful for debugging landmarks)

---


## Demo Video

[![Watch the demo video](https://raw.githubusercontent.com/<YOUR-USERNAME>/<YOUR-REPO>/main/assets/demo_thumbnail.png)](https://drive.google.com/file/d/1xDw4fCx2-SH803H9Xw2Jfc1-25vwOXAM/view?usp=sharing)


**Pipeline**
1. Webcam → Python (`opencv-python`)
2. Hand landmarks → MediaPipe → finger states/gesture classification
3. Gesture → mapped to a number (`0..7`) sent over Serial
4. Arduino receives the number → switches LED mode/effect

---

## Hardware

- Arduino (Uno/Nano/Mega, etc.)
- WS2812B LED strip (configured for **250 LEDs**)
- 5V power supply capable of handling your strip (see power note below)
- Wires
- Recommended:
  - 330–470Ω resistor in series with LED data line
  - 1000µF capacitor across +5V and GND near the strip
  - Logic level shifter (if your Arduino is 5V you may be OK; if 3.3V, strongly recommended)

### Wiring (default in code)
- **Arduino D9** → LED strip **DIN**
- **Arduino GND** → LED strip **GND**
- LED strip **+5V** → external **5V PSU +**
- External PSU **GND** → LED strip **GND**
- **IMPORTANT:** All grounds must be common (Arduino GND tied to PSU GND).

> ⚠️ Power note: 250 WS2812B LEDs at full white can draw a lot of current (worst-case ~60mA per LED).  
> That’s up to ~15A worst-case. In practice you’ll likely run far less, but choose a PSU accordingly and consider injecting power.

---

## Software Requirements

### Arduino
- Arduino IDE
- Library: **FastLED**

### Python (Laptop / Raspberry Pi)
- Python 3.8+ recommended
- Packages:
  - `opencv-python`
  - `mediapipe`
  - `numpy`
  - `pyserial`

Install:
```bash
pip install opencv-python mediapipe numpy pyserial
