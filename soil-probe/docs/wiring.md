# Wiring Diagram

## Camera Node (ESP32-CAM)

### Camera Connections (AI-Thinker pinout)
- PWDN 32
- RESET -1 (not connected)
- XCLK 0
- SIOD 26
- SIOC 27
- Y2..Y9 = 5,18,19,21,36,39,34,35
- VSYNC 25
- HREF 23
- PCLK 22

### LED Ring
- 15 white LEDs (5V, ~3.1V, 20mA each with 100Ω resistor)
- Low-side switching via N-MOSFET
- Gate driven from ESP32-CAM GPIO4 through 100Ω with 10k pull-down

## Sensor Hub (ESP32 DevKit)

### Analog Sensors
- Moisture AOUT: GPIO34 (ADC1 only)
- pH analog out: GPIO35 (ADC1 only) via 10k/20k divider
- Battery voltage: GPIO32 (ADC1 only) via 33k/10k divider

### Digital Sensors
- NPK RS485 module RO/DI: GPIO16 (RX2), GPIO17 (TX2)
- NPK DE+RE tied together: GPIO4
- Reserved for GPS: GPIO25 (RX), GPIO26 (TX)

### Power
- 3S Li-ion input (9.5-12.6V)
- Dedicated 12V rail for NPK sensor + buck regulator
- 5V rail for ESP32 DevKit VIN, ESP32-CAM 5V, LEDs, pH board