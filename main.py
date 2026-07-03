import os
import random
import subprocess
import time
import cv2
import numpy as np

# -------------------
# CONFIG
# -------------------
DEVICE_IP = "127.0.0.1"  # Change to your adb device's IP address
DEVICE_PORT = 16384      # Change to your adb device's port number
TEMPLATE_DIR = "templates"
MATCH_THRESHOLD = 0.8

# -------------------
# DETECTION TEMPLATES 
# -------------------
STAGE_MAINMENU_TEMPLATE = ["MAINMENU_1.png"]
STAGE_PURCHASE_ITEM_TEMPLATE = ["PURCHASE_ITEM_1.png"]
STAGE_GAME_START_TEMPLATE = ["GAME_START_1.png"]
STAGE_GAME_RELAY_TEMPLATE = ["GAME_RELAY_1.png"]
STAGE_GAME_COMPLETE_TEMPLATE = ["GAME_COMPLETE_1.png"]
STAGE_MYSTERY_BOX_TEMPLATE = ["MYSTERY_BOX_1.png"]
STAGE_CONGRATULATIONS_TEMPLATE = ["CONGRATULATIONS_1.png"]
STAGE_LEVEL_UP_TEMPLATE = ["LEVEL_UP_1.png"]
STAGE_RELIC_COMPLETE_TEMPLATE = ["RELIC_COMPLETE_1.png"]
STAGE_RELIC_CLAIM_TEMPLATE = ["RELIC_CLAIM_1.png"]

# -------------------
# BOOST TEMPLATES
# -------------------
BOOST_DOUBLE_COINS_TEMPLATE = ["BOOST_DOUBLE_COINS_1.png"]
BOOST_15P_SCORE_BONUS_TEMPLATE = ["BOOST_15P_SCORE_BONUS_1.png"]
BOOST_M15P_HP_DRAIN_TEMPLATE = ["BOOST_M15P_HP_DRAIN_1.png"]
BOOST_REVIVE_ONCE_WITH_80HP_TEMPLATE = ["BOOST_REVIVE_ONCE_WITH_80HP_1.png"]
BOOST_70P_CRUSH_CHANCE_TEMPLATE = ["BOOST_70P_CRUSH_CHANCE_1.png"]
BOOST_17P_BASE_SPEED_TEMPLATE = ["BOOST_17P_BASE_SPEED_1.png"]
BOOST_GOLD_COIN_MAGIC_TEMPLATE = ["BOOST_GOLD_COIN_MAGIC_1.png"]
BOOST_M30P_COLLISION_DAMAGE_TEMPLATE = ["BOOST_M30P_COLLISION_DAMAGE_1.png"]
BOOST_20P_HP_FROM_POTIONS_TEMPLATE = ["BOOST_20P_HP_FROM_POTIONS_1.png"]
BOOST_MAGNETIC_AURA_TEMPLATE = ["BOOST_MAGNETIC_AURA_1.png"]
BOOST_2PIT_LIFTS_TEMPLATE = ["BOOST_2PIT_LIFTS_1.png"]

# -------------------
# STAGE MAP
# -------------------
STAGE_TEMPLATES = {
    # higher priority stages first
    "LEVEL_UP":        STAGE_LEVEL_UP_TEMPLATE,
    "CONGRATULATIONS": STAGE_CONGRATULATIONS_TEMPLATE,
    "RELIC_COMPLETE":  STAGE_RELIC_COMPLETE_TEMPLATE,
    "RELIC_CLAIM":     STAGE_RELIC_CLAIM_TEMPLATE,
    "MAINMENU":        STAGE_MAINMENU_TEMPLATE,
    "PURCHASE_ITEM":   STAGE_PURCHASE_ITEM_TEMPLATE,
    "GAME_START":      STAGE_GAME_START_TEMPLATE,
    "GAME_RELAY":      STAGE_GAME_RELAY_TEMPLATE,
    "GAME_COMPLETE":   STAGE_GAME_COMPLETE_TEMPLATE,
    "MYSTERY_BOX":     STAGE_MYSTERY_BOX_TEMPLATE,
}

# -------------------
# ITEM COORDINATES
# -------------------
START_BUTTON = (955, 650)
PLAY_BUTTON = (895, 620)
FAST_START_ITEM = (235, 600)
COOKIE_RELAY_ITEM = (385, 600)
RANDOM_BOOST_ITEM = (535, 600)
PURCHASE_BUTTON = (925, 295)
MULTI_PURCHASE_BUTTON = (1100, 195)
MULTI_BUY_BUTTON = (640, 587)
FAST_START_USE_BUTTON = (655, 340)
COOKIE_RELAY_USE_BUTTON = (655, 340)
COMPLETE_FINISH_BUTTON = (460, 625)
ACCEPT_MYSTERY_BOX_BUTTON = (650, 645)
ACCEPT_CONGRATULATIONS_BUTTON = (640, 565)
ACCEPT_LEVEL_UP_BUTTON = (640, 640)
RELIC_COMPLETE_BUTTON = (530, 110)
RELIC_CLAIM_BUTTON = (640, 580)

# -------------------
# ADB FUNCTIONS
# -------------------
def device_connect(ip: str, port: int):
    result = subprocess.run(
        ["adb", "connect", f"{ip}:{port}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    print(f"🔌 {result.stdout.strip().capitalize()}")
    if "connected" not in result.stdout and "already connected" not in result.stdout:
        raise Exception(f"❌ Failed to connect to {ip}:{port}\n{result.stderr.strip()}")

def device_capture_screen(ip: str, port: int):
    result = subprocess.run(
        ["adb", "-s", f"{ip}:{port}", "exec-out", "screencap", "-p"],
        stdout=subprocess.PIPE,
        check=True
    )
    img = np.frombuffer(result.stdout, dtype=np.uint8)
    return cv2.imdecode(img, cv2.IMREAD_COLOR)

def device_tap(ip: str, port: int, x: int, y: int):
    subprocess.run(
        ["adb", "-s", f"{ip}:{port}", "shell", "input", "tap", str(x), str(y)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

def safe_device_tap(ip: str, port: int, x: int, y: int):
    jitter_x = x + random.randint(-15, 15)
    jitter_y = y + random.randint(-15, 15)
    subprocess.run(
        ["adb", "-s", f"{ip}:{port}", "shell", "input", "tap", str(jitter_x), str(jitter_y)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

# -------------------
# DEBUGGING FUNCTIONS
# -------------------
def save_debug_screen(screen):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"debug_screen_{timestamp}.png"
    folder = "debug_screens"
    if not os.path.exists(folder):
        os.makedirs(folder)
    filepath = os.path.join(folder, filename)
    cv2.imwrite(filepath, screen)
    print(f"💾 Saved screen to {filepath}")

# -------------------
# BOT LOGIC
# -------------------
def detect_templates(screen, template_files):
    for filename in template_files:
        template_path = os.path.join(TEMPLATE_DIR, filename)
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        if template is None:
            continue
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        if max_val >= MATCH_THRESHOLD:
            return True
    return False

def detect_stage(screen):
    for stage_name, template_files in STAGE_TEMPLATES.items():
        for filename in template_files:
            template_path = os.path.join(TEMPLATE_DIR, filename)
            template = cv2.imread(template_path, cv2.IMREAD_COLOR)
            if template is None:
                continue
            result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)
            if max_val >= MATCH_THRESHOLD:
                return stage_name
    return None

def start_game():
    print("🏁 Starting the game...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, START_BUTTON[0], START_BUTTON[1])
    time.sleep(random.uniform(0.8, 1.4))

def play_game():
    print("🎮 Playing the game...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, PLAY_BUTTON[0], PLAY_BUTTON[1])
    time.sleep(random.uniform(0.8, 1.4))

def purchase_fast_start():
    print("🛒 Purchasing Fast Start...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, FAST_START_ITEM[0], FAST_START_ITEM[1])
    time.sleep(random.uniform(0.8, 1.4))
    safe_device_tap(DEVICE_IP, DEVICE_PORT, PURCHASE_BUTTON[0], PURCHASE_BUTTON[1])
    time.sleep(random.uniform(1, 2))

def purchase_cookie_relay():
    print("🛒 Purchasing Cookie Relay...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, COOKIE_RELAY_ITEM[0], COOKIE_RELAY_ITEM[1])
    time.sleep(random.uniform(0.8, 1.4))
    safe_device_tap(DEVICE_IP, DEVICE_PORT, PURCHASE_BUTTON[0], PURCHASE_BUTTON[1])
    time.sleep(random.uniform(1, 2))

def purchase_random_boost():
    print("🛒 Purchasing Random Boost...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, RANDOM_BOOST_ITEM[0], RANDOM_BOOST_ITEM[1])
    time.sleep(random.uniform(0.8, 1.4))
    safe_device_tap(DEVICE_IP, DEVICE_PORT, PURCHASE_BUTTON[0], PURCHASE_BUTTON[1])
    time.sleep(random.uniform(1, 2))

def purchase_desired_random_boost(desired_template, desired_name):
    print("🛒 Purchasing Desired Random Boost...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, RANDOM_BOOST_ITEM[0], RANDOM_BOOST_ITEM[1])
    time.sleep(random.uniform(0.8, 1.4))
    safe_device_tap(DEVICE_IP, DEVICE_PORT, MULTI_PURCHASE_BUTTON[0], MULTI_PURCHASE_BUTTON[1])
    time.sleep(random.uniform(1, 2))
    safe_device_tap(DEVICE_IP, DEVICE_PORT, MULTI_BUY_BUTTON[0], MULTI_BUY_BUTTON[1])
    time.sleep(random.uniform(0.8, 1.4))
    print(f"🔍 Waiting for desired boost to be detected: {desired_name}...")
    timeout = 30
    start_time = time.time()
    while True:
        if time.time() - start_time > timeout:
            print(f"⏰ Timeout: Could not detect desired boost '{desired_name}' within {timeout} seconds.")
            print("⚠️ Skipping Desired Random Boost. Please verify your in-game boost config is correct.")
            return
        screen = device_capture_screen(DEVICE_IP, DEVICE_PORT)
        if detect_templates(screen, desired_template):
            print(f"✅ Desired Boost detected: {desired_name}!")
            break
        time.sleep(0.5)

def using_fast_start():
    print("⚡ Using Fast Start...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, FAST_START_USE_BUTTON[0], FAST_START_USE_BUTTON[1])
    time.sleep(random.uniform(0.8, 1.4))

def using_cookie_relay():
    print("🍪 Using Cookie Relay...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, COOKIE_RELAY_USE_BUTTON[0], COOKIE_RELAY_USE_BUTTON[1])
    time.sleep(random.uniform(0.8, 1.4))

def complete_finish():
    print("🏆 Completing the game...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, COMPLETE_FINISH_BUTTON[0], COMPLETE_FINISH_BUTTON[1])
    time.sleep(random.uniform(0.8, 1.4))

def accept_mystery_box():
    print("🎁 Accepting Mystery Box...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, ACCEPT_MYSTERY_BOX_BUTTON[0], ACCEPT_MYSTERY_BOX_BUTTON[1])
    time.sleep(random.uniform(0.8, 1.4))

def accept_congratulations():
    print("🎉 Accepting Congratulations...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, ACCEPT_CONGRATULATIONS_BUTTON[0], ACCEPT_CONGRATULATIONS_BUTTON[1])
    time.sleep(random.uniform(0.8, 1.4))

def accept_level_up():
    print("⬆️ Accepting Level Up...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, ACCEPT_LEVEL_UP_BUTTON[0], ACCEPT_LEVEL_UP_BUTTON[1])
    time.sleep(random.uniform(0.8, 1.4))

def open_relic_complete():
    print("🏺 Opening Relic Complete...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, RELIC_COMPLETE_BUTTON[0], RELIC_COMPLETE_BUTTON[1])
    time.sleep(random.uniform(0.8, 1.4))

def accept_relic_claim():
    print("🏺 Accepting Relic Claim...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, RELIC_CLAIM_BUTTON[0], RELIC_CLAIM_BUTTON[1])
    time.sleep(random.uniform(10, 15))

# -------------------
# BOT OPTIONS
# -------------------
BOOST_CHOICES = [
    ("Double Coins",            BOOST_DOUBLE_COINS_TEMPLATE),
    ("+15% Score Bonus",        BOOST_15P_SCORE_BONUS_TEMPLATE),
    ("-15% HP Drain",           BOOST_M15P_HP_DRAIN_TEMPLATE),
    ("Revive Once with 80 HP",  BOOST_REVIVE_ONCE_WITH_80HP_TEMPLATE),
    ("70% Crush Chance",        BOOST_70P_CRUSH_CHANCE_TEMPLATE),
    ("+17% Base Speed",         BOOST_17P_BASE_SPEED_TEMPLATE),
    ("Gold Coin Magic",         BOOST_GOLD_COIN_MAGIC_TEMPLATE),
    ("-30% Collision Damage",   BOOST_M30P_COLLISION_DAMAGE_TEMPLATE),
    ("+20% HP from Potions",    BOOST_20P_HP_FROM_POTIONS_TEMPLATE),
    ("Magnetic Aura",           BOOST_MAGNETIC_AURA_TEMPLATE),
    ("2 Pit Lifts",             BOOST_2PIT_LIFTS_TEMPLATE),
]

def prompt_user_options():
    desired_boost_template = None

    print("\n⚙️ --- Bot Options ---")
    use_fast_start = input("⚡ Use Fast Start (buy + use)? [y/n]: ").strip().lower() == "y"
    use_cookie_relay = input("🍪 Use Cookie Relay (buy + use)? [y/n]: ").strip().lower() == "y"
    use_desired_random_boost = input("🎲 Use Desired Random Boost (buy + use)? [y/n]: ").strip().lower() == "y"
    if use_desired_random_boost:
        print("  Select desired boost (must match the boost option configured in-game):")
        for i, (name, _) in enumerate(BOOST_CHOICES, 1):
            print(f"  {i:2}. {name}")
        while True:
            choice = input("  Enter number: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(BOOST_CHOICES):
                desired_boost_template = BOOST_CHOICES[int(choice) - 1][1]
                desired_boost_name = BOOST_CHOICES[int(choice) - 1][0]
                print(f"  ✅ Selected: {desired_boost_name}")
                break
            print(f"  ⚠️ Please enter a number between 1 and {len(BOOST_CHOICES)}.")
    print("---------------------\n")

    return {
        "use_fast_start": use_fast_start,
        "use_cookie_relay": use_cookie_relay,
        "use_desired_random_boost": use_desired_random_boost,
        "desired_boost_template": desired_boost_template,
        "desired_boost_name": desired_boost_name if use_desired_random_boost else None,
    }

# -------------------
# MAIN LOOP
# -------------------
def main():
    try:
        print("🚀 CookieRun Classic Bot Started")
        print("⚠️ Screen must be 1280x720 resolution for the bot to work properly.")
        print(f"📱 Connecting to device at {DEVICE_IP}:{DEVICE_PORT}...")

        device_connect(DEVICE_IP, DEVICE_PORT)

        # * for debugging *
        # device_screen = device_capture_screen(DEVICE_IP, DEVICE_PORT)
        # save_debug_screen(device_screen)

        options = prompt_user_options()

        last_stage = None
        is_first_game = True

        while True:
                device_screen = device_capture_screen(DEVICE_IP, DEVICE_PORT)
                stage = detect_stage(device_screen)

                if stage == last_stage:
                    time.sleep(0.5)
                    continue

                last_stage = stage

                if stage == "MAINMENU":
                    print("🎮 Detected Stage: MAINMENU")
                    # Add logic for MAINMENU stage
                    if not is_first_game:
                        delay = random.uniform(30, 60)
                        print(f"⏳ Waiting for {delay:.2f} seconds before starting the next game...")
                        time.sleep(delay)
                    is_first_game = False
                    start_game()
                elif stage == "PURCHASE_ITEM":
                    print("🛒 Detected Stage: PURCHASE_ITEM")
                    # Add logic for PURCHASE_ITEM stage
                    if options["use_fast_start"]:
                        purchase_fast_start()
                    if options["use_cookie_relay"]:
                        purchase_cookie_relay()
                    if options["use_desired_random_boost"]:
                        purchase_desired_random_boost(options["desired_boost_template"], options["desired_boost_name"])
                    play_game()
                elif stage == "GAME_START":
                    print("🏁 Detected Stage: GAME_START")
                    # Add logic for GAME_START stage
                    if options["use_fast_start"]:
                        using_fast_start()
                elif stage == "GAME_RELAY":
                    print("🔄 Detected Stage: GAME_RELAY")
                    # Add logic for GAME_RELAY stage
                    if options["use_cookie_relay"]:
                        using_cookie_relay()
                elif stage == "GAME_COMPLETE":
                    print("✅ Detected Stage: GAME_COMPLETE")
                    # Add logic for GAME_COMPLETE stage
                    complete_finish()
                elif stage == "MYSTERY_BOX":
                    print("🎁 Detected Stage: MYSTERY_BOX")
                    # Add logic for MYSTERY_BOX stage
                    accept_mystery_box()
                    # Reset last_stage to None to allow re-detection of stages
                    time.sleep(3)
                    last_stage = None
                elif stage == "CONGRATULATIONS":
                    print("🎉 Detected Stage: CONGRATULATIONS")
                    # Add logic for CONGRATULATIONS stage
                    accept_congratulations()
                    # Reset last_stage to None to allow re-detection of stages
                    last_stage = None
                elif stage == "LEVEL_UP":
                    print("⬆️ Detected Stage: LEVEL_UP")
                    # Add logic for LEVEL_UP stage
                    accept_level_up()
                elif stage == "RELIC_COMPLETE":
                    print("🏺 Detected Stage: RELIC_COMPLETE")
                    # Add logic for RELIC_COMPLETE stage
                    open_relic_complete()
                elif stage == "RELIC_CLAIM":
                    print("🏺 Detected Stage: RELIC_CLAIM")
                    # Add logic for RELIC_CLAIM stage
                    accept_relic_claim()

                time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n\n🛑 Bot stopped by user.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
