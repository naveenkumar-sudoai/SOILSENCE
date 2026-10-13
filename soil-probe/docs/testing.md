# Testing Checklist

## Hardware Tests

### Power Rail Voltages
- Verify 3S Li-ion input (9.5-12.6V)
- Check 12V rail for NPK sensor (should be stable)
- Check 5V rail for all components (ESP32, LEDs, sensors)

### Individual Sensors
- Test moisture sensor alone with known values
- Test pH sensor with buffer solutions
- Test NPK sensor communication (raw Modbus frames)
- Verify LED ring brightness & switching

### Camera Tests
- Verify camera capture at VGA resolution
- Test LED flash timing (150ms delay)
- Validate JPEG compression quality parameter

## System Tests

### WiFi Range Test
- Verify range with client connection stability
- Test softAP broadcast and client reconnection

### 10-Minute Soak Test
- Run continuous operation for 10 minutes
- Monitor: temperature, voltage, memory usage

### Sensor Integration Test
- Run full sensor reading sequence
- Verify correct data formatting in API responses

## Firmware Build Tests

- Compile with `arduino-cli` using: `esp32:esp32:esp32cam` with `PartitionScheme=huge_app`
- Verify all unit tests pass with mock data