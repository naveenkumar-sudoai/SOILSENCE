# Soil Probe

A portable soil analysis probe with ESP32-based sensor hub and camera node.

## Architecture Diagram

```
Phone app --WiFi--> ESP32 DevKit HUB (SoftAP "SoilProbe", 192.168.4.1)
                         |  reads moisture, pH, NPK, battery
                         |  HTTP proxy
                         +--WiFi STA--> ESP32-CAM node (static 192.168.4.50)
                                         /capture?flash=1  -> JPEG
Phone app --internet--> Open-Meteo (weather), DeepSeek (recommendations)
```

## Repository Structure

```
soil-probe/
  README.md
  .gitignore
  docs/            wiring.md  api.md  calibration.md  dataset-protocol.md  testing.md
  firmware/
    hub/           hub.ino  config.h  npk_modbus.h  calibration.h  battery.h
    cam_node/      cam_node.ino  config.h  camera_pins.h
  tools/
    dataset_collector/   soil_collector.py  requirements.txt   (USB-serial collector; keep existing protocol)
    mock_hub/            mock_hub.py  (FastAPI/Flask, implements section 4 with fake data and a sample JPEG)
  ml/
    dataset/<class>/     (images; gitignored except .gitkeep)
    train.py  export_tflite.py  evaluate.py  requirements.txt  README.md
  app/               (Flutter project)
```

## Hardware

- **Camera node:** ESP32-CAM (AI-Thinker pinout) with RHYX M21-45 camera (GC2145 sensor)
- **Sensor hub:** ESP32 DevKit (30-pin, ESP32-WROOM)
- **Sensors:** NPK (RS485), capacitive moisture, pH
- **Power:** 3S Li-ion 11.1 V with buck regulators

## Features

- Real-time soil sensor readings
- Camera capture with LED lighting
- Soil type classification via TFLite model
- DeepSeek API integration for crop/fertilizer recommendations
- Offline-first sample saving

## Getting Started

### USB Dataset Collection Mode

The camera node can be used in USB dataset collection mode:

1. Connect the ESP32-CAM to your computer via USB
2. Run the dataset collector tool:
   ```bash
   cd tools/dataset_collector
   python3 soil_collector.py
   ```
3. Follow the UI to select the COM port and capture images

### Building Firmware

For building firmware, use `arduino-cli` with the following command:
```bash
arduino-cli compile --fqbn esp32:esp32:esp32cam firmware/cam_node/
```