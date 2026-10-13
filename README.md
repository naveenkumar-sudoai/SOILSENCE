# Soil Probe Project

This is the main repository for the Soil Probe project - a portable soil analysis system with ESP32-based sensor hub and camera node.

## Overview

A portable soil analysis probe that:
- Uses ESP32-CAM for imaging with LED ring lighting 
- Integrates multiple sensors (NPK, moisture, pH)
- Connects to phone app via WiFi for real-time readings
- Uses AI/ML for soil type classification
- Provides crop/fertilizer recommendations via DeepSeek API

## Project Structure

```
SOILSENCE/
├── soil-probe/              # Main project directory
│   ├── README.md            # This file  
│   ├── .gitignore
│   ├── docs/                # Documentation
│   ├── firmware/            # ESP32 firmware
│   │   ├── hub/             # Sensor hub firmware
│   │   └── cam_node/        # Camera node firmware  
│   ├── tools/               # Development tools
│   │   ├── dataset_collector/  # Image collection tool
│   │   └── mock_hub/        # Mock server for app development
│   ├── ml/                  # Machine learning models
│   └── app/                 # Mobile application (Flutter)
└── README.md                # This file
```

## Getting Started

1. Navigate to `soil-probe` directory
2. Follow the main README there for detailed instructions

For immediate development, see:
- `soil-probe/README.md` for full documentation
- `soil-probe/firmware/cam_node/` for camera firmware 
- `soil-probe/tools/dataset_collector/` for image collection

## Milestone 1 Complete

Completed: Repository scaffold, documentation, USB dataset mode implementation
- ESP32-CAM USB dataset mode support
- Python dataset collector tool  
- All required firmware and tool files