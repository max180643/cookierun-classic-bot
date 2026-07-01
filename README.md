# CookieRun Classic Bot

An automated bot for CookieRun Classic that uses ADB (Android Debug Bridge) and OpenCV template matching to detect game stages and automate gameplay on an Android device or emulator.

## Features

- Automatically detects game stages via screen capture and template matching
- Handles the full game loop: Main Menu → Purchase Items → Game Start → Relay → Game Complete → Mystery Box → Congratulations
- Optional **Fast Start** power-up (auto-purchase and use)
- Optional **Cookie Relay** power-up (auto-purchase and use)
- Human-like tap behavior with randomized coordinate jitter and delays
- Auto-waits 30–60 seconds between games to reduce detection risk
- Debug screen saving for troubleshooting

## Requirements

- Python 3.x
- [ADB (Android Debug Bridge)](https://developer.android.com/tools/adb) installed and in your system PATH
- An Android device or emulator running CookieRun Classic
- **Device screen resolution must be set to 1280×720**

### Python Dependencies

```
numpy
opencv-python
```

Install via:

```bash
pip install -r requirements.txt
```

## Setup

1. **Enable ADB on your device/emulator** and note its IP address and port.

2. **Edit `main.py`** and set your device details at the top:
   ```python
   DEVICE_IP = "127.0.0.1"   # Your device's IP address
   DEVICE_PORT = 16384        # Your device's ADB port
   ```

3. **Ensure templates exist** — the `templates/` folder must contain the following detection images captured at 1280×720:
   - `MAINMENU_1.png`
   - `PURCHASE_ITEM_1.png`
   - `GAME_START_1.png`
   - `GAME_RELAY_1.png`
   - `GAME_COMPLETE_1.png`
   - `MYSTERY_BOX_1.png`
   - `CONGRATULATIONS_1.png`

## Usage

```bash
python main.py
```

On startup, the bot will:
1. Connect to your ADB device
2. Prompt you to configure options:
   - **Fast Start**: auto-buy and use the Fast Start item each round
   - **Cookie Relay**: auto-buy and use the Cookie Relay item each round
3. Begin the automation loop

## Project Structure

```
cookierun-classic-bot/
├── main.py              # Main bot logic
├── requirements.txt     # Python dependencies
└── templates/           # Stage detection template
```

## Configuration

| Constant          | Default     | Description                                     |
|-------------------|-------------|-------------------------------------------------|
| `DEVICE_IP`       | `127.0.0.1` | ADB device IP address                           |
| `DEVICE_PORT`     | `16384`     | ADB device port                                 |
| `MATCH_THRESHOLD` | `0.8`       | Minimum confidence for template match (0.0–1.0) |
| `TEMPLATE_DIR`    | `templates` | Folder containing stage detection images        |

## How It Works

1. The bot captures a screenshot via ADB every 0.5 seconds.
2. It uses OpenCV's `matchTemplate` to compare the screen against known stage images.
3. When a stage is detected, the corresponding action is performed (tapping buttons with randomized coordinate jitter).
4. The loop continues until the process is manually stopped (`Ctrl+C`).

## Debugging

Uncomment the following lines in `main()` to capture and save a screenshot on startup for troubleshooting template matching:

```python
device_screen = device_capture_screen(DEVICE_IP, DEVICE_PORT)
save_debug_screen(device_screen)
```

Saved screenshots will appear in the `debug_screens/` folder with a timestamp.

## Troubleshooting

- **Stage not detected**: Save a debug screenshot and compare it against the template images. You may need to recapture templates at the correct resolution.
- **ADB connection failed**: Verify ADB is in your PATH and the device is reachable (`adb devices`).
- **Wrong tap coordinates**: All coordinates are calibrated for **1280×720**. Ensure your emulator/device is set to this resolution.
