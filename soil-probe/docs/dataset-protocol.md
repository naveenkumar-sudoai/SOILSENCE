# Dataset Collection Protocol

## USB Serial Mode (USB_DATASET_MODE)

When enabled, the camera node enters dataset collection mode:

### Commands
- `'C'`: Capture image with flash and send over serial
- `'P'`: Preview current frame and send over serial  

### Data Format
- `IMG!` + 4-byte little-endian length + JPEG data
- `PNG!` + 4-byte little-endian length + PNG data  
- `ERR!` + 4-byte little-endian length + error text

## Web Mode

When running in WiFi mode, the camera node responds to:
- `/capture?flash=1&q=85`: Capture with flash (JPEG)
- `/status`: Status report