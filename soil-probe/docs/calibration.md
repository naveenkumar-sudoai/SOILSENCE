# Calibration Guide

## pH Calibration

Two-point calibration using standard buffer solutions:
- Point 1: pH 4.01 (4.01 buffer solution)
- Point 2: pH 6.86 (6.86 buffer solution) 
- Point 3: pH 9.18 (9.18 buffer solution) - optional third point

Calibration is stored as linear fit coefficients from the three points.

## Moisture Calibration

Two-point calibration using:
- Dry: Sensor in air
- Wet: Sensor submerged in water up to the measurement line

Calibration stored as raw ADC values for dry and wet points.

## Storage

Calibration data stored in `Preferences` with the following keys:
- `ph_points`: JSON mapping pH buffer points to voltage readings
- `moisture_cal`: JSON mapping "dry" and "wet" to raw ADC values