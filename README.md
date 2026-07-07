# CookieRun Classic Bot

An automated bot for CookieRun Classic that uses ADB (Android Debug Bridge) and OpenCV template matching to detect game stages and automate gameplay on an Android device or emulator.

## Features

- Automatically detects game stages via screen capture and template matching
- Handles the full game loop: Main Menu → Purchase Items → Game Start → Relay → Game Complete → Mystery Box → Congratulations → Level Up → Relic Complete → Relic Claim → Daily Check-in → Daily Treasure → Enter League → League Results → Previous Rank Results → Anti-Bot → Connection Lost → Inactive
- Optional **Fast Start** power-up (auto-purchase and use)
- Optional **Cookie Relay** power-up (auto-purchase and use)
- Optional **Desired Random Boost** (auto-purchase the selected boost from 11 available options)
- Human-like tap behavior with randomized coordinate jitter and delays
- Auto-waits 30–60 seconds between games to reduce detection risk
- Periodic session reset: automatically restarts the app every 1.5–3 hours to avoid long-session detection
- Anti-bot card challenge detection: identifies and taps the odd card out automatically
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

2. **Edit `config.py`** and set your device details at the top:

   ```python
   DEVICE_IP = "127.0.0.1"    # Your device's IP address
   DEVICE_PORT = 16384        # Your device's ADB port
   ```

3. **Ensure templates exist** — the `templates/` folder must contain the following detection images captured at 1280×720:

   **Stage templates:**
   `MAINMENU_1.png`, `PURCHASE_ITEM_1.png`, `GAME_START_1.png`, `GAME_RELAY_1.png`,
   `GAME_COMPLETE_1.png`, `MYSTERY_BOX_1.png`, `CONGRATULATIONS_1.png`, `CONGRATULATIONS_2.png`,
   `LEVEL_UP_1.png`, `RELIC_COMPLETE_1.png`, `RELIC_CLAIM_1.png`, `DAILY_CHECKIN_1.png`,
   `DAILY_TREASURE_1.png`, `ENTER_LEAGUE_1.png`, `LEAGUE_RESULTS_1.png`,
   `PREVIOUS_RANK_RESULTS_1.png`, `ANTI_BOT_1.png`, `CONNECTION_LOST_1.png`, `INACTIVE_1.png`

   **Boost templates** (only needed if using Desired Random Boost):
   `BOOST_DOUBLE_COINS_1.png`, `BOOST_15P_SCORE_BONUS_1.png`, `BOOST_M15P_HP_DRAIN_1.png`,
   `BOOST_REVIVE_ONCE_WITH_80HP_1.png`, `BOOST_70P_CRUSH_CHANCE_1.png`, `BOOST_17P_BASE_SPEED_1.png`,
   `BOOST_GOLD_COIN_MAGIC_1.png`, `BOOST_M30P_COLLISION_DAMAGE_1.png`, `BOOST_20P_HP_FROM_POTIONS_1.png`,
   `BOOST_MAGNETIC_AURA_1.png`, `BOOST_2PIT_LIFTS_1.png`

## Usage

```bash
python main.py
```

On startup, the bot will:

1. Connect to your ADB device
2. Prompt you to configure options:
   - **Fast Start**: auto-buy and use the Fast Start item each round
   - **Cookie Relay**: auto-buy and use the Cookie Relay item each round
   - **Desired Random Boost**: auto-buy a specific boost each round (choose from 11 options)
3. Begin the automation loop

## Project Structure

```
cookierun-classic-bot/
├── main.py              # Entry point
├── bot.py               # Main bot logic and game loop
├── actions.py           # Tap/action handlers for each stage
├── adb.py               # ADB connection and screen capture
├── config.py            # Device config, thresholds, and template paths
├── detection.py         # OpenCV template matching logic
├── debug.py             # Debug screen saving utility
├── requirements.txt     # Python dependencies
├── templates/           # Stage detection template images
└── debug_screens/       # Saved debug screenshots (auto-created)
```

## Configuration

All constants are defined in `config.py`.

| Constant                 | Default         | Description                                             |
| ------------------------ | --------------- | ------------------------------------------------------- |
| `DEVICE_IP`              | `127.0.0.1`     | ADB device IP address                                   |
| `DEVICE_PORT`            | `16384`         | ADB device port                                         |
| `MATCH_THRESHOLD`        | `0.8`           | Minimum confidence for template match (0.0–1.0)         |
| `TEMPLATE_DIR`           | `templates`     | Folder containing stage detection images                |
| `SESSION_RESET_INTERVAL` | `(5400, 10800)` | Random interval in seconds (1.5–3 h) before app restart |

You can also limit specific stage detection to a fixed screen region with `(x1, y1, x2, y2)` bounds. Each stage has a corresponding `STAGE_<NAME>_REGION` constant in `config.py` that restricts template matching to a sub-region of the screen, which speeds up detection.

## How It Works

1. The bot captures a screenshot via ADB approximately every 0.25 seconds.
2. It uses OpenCV's `matchTemplate` to compare the screen against known stage images within pre-defined screen regions.
3. Stage detection is split into `PRE_GAME`, `IN_GAME`, and `POST_GAME` groups so each loop checks only the stages relevant to the current flow. `CONNECTION_LOST` and `INACTIVE` are always checked regardless of group.
4. If grouped detection misses repeatedly (configurable timeout per group), the bot automatically falls back to a full stage scan to recover.
5. When a stage is detected, the corresponding action is performed (tapping buttons with randomized coordinate jitter and delays).
6. **Anti-bot challenge**: when the anti-bot card screen is detected, the bot identifies the odd card out from a set of six using template matching and taps it.
7. **Session reset**: after a random interval of 1.5–3 hours, the bot restarts the CookieRun app to reduce long-session detection risk.
8. The loop continues until the process is manually stopped (`Ctrl+C`).

## Debugging

To capture and save a screenshot for troubleshooting template matching, call `save_debug_screen()` from `debug.py`:

```python
from adb import device_capture_screen
from config import DEVICE_IP, DEVICE_PORT
from debug import save_debug_screen

device_screen = device_capture_screen(DEVICE_IP, DEVICE_PORT)
save_debug_screen(device_screen)
```

Saved screenshots will appear in the `debug_screens/` folder with a timestamp.

## Troubleshooting

- **Stage not detected**: Save a debug screenshot and compare it against the template images. You may need to recapture templates at the correct resolution.
- **ADB connection failed**: Verify ADB is in your PATH and the device is reachable (`adb devices`).
- **Wrong tap coordinates**: All coordinates are calibrated for **1280×720**. Ensure your emulator/device is set to this resolution.
