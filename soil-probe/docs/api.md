# Soil Probe API

## Hub Endpoints (`http://192.168.4.1`)

All JSON unless stated, CORS open, errors as `{"error": "..."}` with proper HTTP codes.

### GET /api/status
```json
{
  "fw": "1.0.0",
  "uptime_s": 1234,
  "battery_v": 11.8,
  "battery_pct": 85,
  "cam_online": true,
  "wifi_clients": 1,
  "free_heap": 15360
}
```

### GET /api/sensors
```json
{
  "ts_ms": 1678886400000,
  "moisture_pct": 42.5,
  "moisture_raw": 2100,
  "ph": 6.2,
  "ph_voltage_mv": 1950,
  "n_mgkg": 32,
  "p_mgkg": 28,
  "k_mgkg": 45,
  "npk_ok": true,
  "errors": ["moisture_sensor_failed"]
}
```

### GET /api/capture?flash=1&q=85
Returns `image/jpeg` (hub fetches from camera node)

### GET /api/calibration
```json
{
  "ph_points": {
    "4.01": 1024,
    "6.86": 1638,
    "9.18": 2048
  },
  "moisture_cal": {
    "dry": 3000,
    "wet": 1300
  }
}
```

### POST /api/calibrate/ph
Body: `{"point":"4.01"|"6.86"|"9.18"}`

### POST /api/calibrate/moisture
Body: `{"point":"dry"|"wet"}`

### POST /api/calibrate/reset

### GET /api/debug/npk
```json
{
  "request": "0103001e0003742c",
  "response": "010306002000000000001a29"
}
```

## Camera Node Endpoints (`http://192.168.4.50`)

### GET /capture?flash=0|1&q=1..63
Returns `image/jpeg`, header `X-Capture-Ms`

### GET /status
```json
{
  "fw": "1.0.0",
  "rssi": -65,
  "free_heap": 12288,
  "psram": 4194304,
  "camera_ok": true,
  "camera_err": ""
}
```