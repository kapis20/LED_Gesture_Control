#include <FastLED.h>

// -------------------- LED CONFIG --------------------
#define LED_PIN     9
#define NUM_LEDS    250
#define LED_TYPE    WS2812B
#define COLOR_ORDER GRB

CRGB leds[NUM_LEDS];
uint8_t gBrightness = 80;

// -------------------- MODES --------------------
enum Mode : uint8_t {
  MODE_OFF = 0,
  MODE_WHITE,
  MODE_SOLID_BLUE,
  MODE_BREATH_WARM,
  MODE_RAINBOW_SOLID,
  MODE_RAINBOW_CHASE,
  MODE_KNIGHT_RIDER,
  MODE_SPARKLE,
  MODE_COUNT
};

Mode mode = MODE_OFF;

// Animation state
uint8_t gHue = 0;
uint16_t scannerPos = 0;
int8_t scannerDir = 1;

// -------------------- HELPERS --------------------
void printMenu() {
  Serial.println();
  Serial.println("=== LED MODE MENU ===");
  Serial.println("Type a number then press Enter:");
  Serial.println("0 = OFF");
  Serial.println("1 = WHITE (solid)");
  Serial.println("2 = SOLID BLUE");
  Serial.println("3 = BREATH (warm)");
  Serial.println("4 = RAINBOW (solid hue)");
  Serial.println("5 = RAINBOW CHASE");
  Serial.println("6 = KNIGHT RIDER (red scanner)");
  Serial.println("7 = SPARKLE (glitter)");
  Serial.println("m = show this menu again");
  Serial.println("=====================");
  Serial.println();
}

void setAll(const CRGB &c) {
  fill_solid(leds, NUM_LEDS, c);
  FastLED.show();
}

void clearAll() {
  fill_solid(leds, NUM_LEDS, CRGB::Black);
  FastLED.show();
}

void resetModeState(Mode m) {
  // reset animation state so switching looks clean
  if (m == MODE_KNIGHT_RIDER) {
    scannerPos = 0;
    scannerDir = 1;
    clearAll();
  }
}

// -------------------- EFFECTS --------------------
void modeBreathWarm() {
  uint8_t b = beatsin8(10, 10, 255);  // speed, min, max
  CRGB warm = CRGB(b, (uint8_t)(b * 0.8), (uint8_t)(b * 0.5));
  fill_solid(leds, NUM_LEDS, warm);
  FastLED.show();
}

void modeRainbowSolid() {
  fill_solid(leds, NUM_LEDS, CHSV(gHue, 255, 255));
  FastLED.show();
  gHue++;
}

void modeRainbowChase() {
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CHSV(gHue + i * 3, 255, 255);
  }
  FastLED.show();
  gHue++;
}

void modeKnightRider() {
  fadeToBlackBy(leds, NUM_LEDS, 40);
  leds[scannerPos] = CRGB::Red;
  FastLED.show();

  scannerPos += scannerDir;
  if (scannerPos == 0 || scannerPos == NUM_LEDS - 1) {
    scannerDir = -scannerDir;
  }
}

void modeSparkle() {
  fadeToBlackBy(leds, NUM_LEDS, 30);
  if (random8() < 80) {
    uint16_t pos = random16(NUM_LEDS);
    leds[pos] += CHSV(random8(), 200, 255);
  }
  FastLED.show();
}

// -------------------- SERIAL INPUT --------------------
void handleSerial() {
  if (!Serial.available()) return;

  // Read a whole line (e.g. "3" or "m")
  String line = Serial.readStringUntil('\n');
  line.trim();
  if (line.length() == 0) return;

  if (line.equalsIgnoreCase("m")) {
    printMenu();
    return;
  }

  // Try parse number
  int v = line.toInt();  // returns 0 if not a number; that's OK because 0 is a valid mode
  if (line.length() == 1 && (line[0] < '0' || line[0] > '7')) {
    Serial.println("Invalid input. Type 0..7 or 'm'.");
    return;
  }

  if (v < 0 || v >= (int)MODE_COUNT) {
    Serial.println("Invalid mode. Type 0..7.");
    return;
  }

  mode = (Mode)v;
  resetModeState(mode);

  Serial.print("Switched to mode ");
  Serial.println(v);
}

// -------------------- SETUP/LOOP --------------------
void setup() {
  delay(200);

  Serial.begin(115200);
  while (!Serial) { ; }  // OK on boards that support it

  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS);
  FastLED.setBrightness(gBrightness);
  FastLED.clear(true);

  random16_add_entropy(analogRead(A0)); // helps sparkle randomness (safe even if floating)

  printMenu();
  Serial.println("Ready. Choose a mode!");
}

void loop() {
  handleSerial();

  switch (mode) {
    case MODE_OFF:
      clearAll();
      delay(50);
      break;

    case MODE_WHITE:
      setAll(CRGB::White);
      delay(50);
      break;

    case MODE_SOLID_BLUE:
      setAll(CRGB::Blue);
      delay(50);
      break;

    case MODE_BREATH_WARM:
      modeBreathWarm();
      delay(20);
      break;

    case MODE_RAINBOW_SOLID:
      modeRainbowSolid();
      delay(20);
      break;

    case MODE_RAINBOW_CHASE:
      modeRainbowChase();
      delay(20);
      break;

    case MODE_KNIGHT_RIDER:
      modeKnightRider();
      delay(15);
      break;

    case MODE_SPARKLE:
      modeSparkle();
      delay(20);
      break;

    default:
      clearAll();
      delay(50);
      break;
  }
}
