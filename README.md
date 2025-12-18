# LED Gesture Control

Control LEDs with hand gestures using MediaPipe and Raspberry Pi GPIO.

## Project Structure

```
LED_Gesture_Control/
├── src/
│   ├── main.py         # Application entry point
│   ├── gesture.py      # MediaPipe gesture detection
│   ├── led.py          # GPIO LED control (Pi-only)
│   └── config.py       # Configuration & constants
├── scripts/
│   ├── run_dev.sh      # Development run script
│   └── run_pi.sh       # Raspberry Pi run script
├── requirements.txt    # Python dependencies
├── environment.yml     # Conda environment file
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Features

- **Hand Gesture Detection** - Uses MediaPipe to detect hand gestures via webcam
- **LED Control** - Controls LEDs on Raspberry Pi via GPIO
- **Gesture Mapping** - Customizable mapping of gestures to LED states
- **PC Development** - Can run on PC (without GPIO) for testing
- **Easy Configuration** - All settings in `src/config.py`

## Supported Gestures

- **THUMBS_UP** - Thumbs up gesture
- **PEACE** - Peace sign (two fingers)
- **OPEN_PALM** - All fingers spread
- **POINTING** - Index finger pointing

## Installation

### Requirements

- Python 3.8+
- Webcam or camera module
- Raspberry Pi (optional, for GPIO control)

### Development (PC)

```bash
chmod +x scripts/run_dev.sh
./scripts/run_dev.sh
```

### Raspberry Pi

1. Install dependencies:
```bash
sudo apt-get install python3-pip python3-venv
```

2. Make script executable:
```bash
chmod +x scripts/run_pi.sh
```

3. Run:
```bash
./scripts/run_pi.sh
```

## Manual Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run
cd src
python3 main.py
```

## Configuration

Edit `src/config.py` to customize:

- **GPIO_PINS** - GPIO pin numbers for LEDs
- **CAMERA_INDEX** - Camera device index
- **CONFIDENCE_THRESHOLD** - Detection confidence level
- **GESTURE_LED_MAP** - Gesture to LED mapping

## Dependencies

- **mediapipe** - Hand gesture detection
- **opencv-python** - Camera & image processing
- **RPi.GPIO** - Raspberry Pi GPIO control (Pi only)

## Usage

```bash
# Press 'q' to quit
# LEDs turn off automatically after 2 seconds of no gesture
```

## Hardware Setup (Raspberry Pi)

Connect LEDs with resistors to GPIO pins defined in `config.py`.

Example with pins 17, 27, 22, 24:
```
GPIO17 → LED1 → GND
GPIO27 → LED2 → GND
GPIO22 → LED3 → GND
GPIO24 → LED4 → GND
```

## Troubleshooting

- **Camera not found**: Check `CAMERA_INDEX` in config.py
- **GPIO permission denied**: Run with sudo or add user to gpio group
- **MediaPipe import error**: Reinstall dependencies

## License

Your License Here

## Contributing

Contributions welcome! Please submit pull requests.
