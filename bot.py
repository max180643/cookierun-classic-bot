import random
import time

from adb import device_capture_screen, device_connect, device_reset_app
from actions import (
    accept_congratulations,
    accept_daily_checkin,
    accept_daily_treasure,
    accept_enter_league,
    accept_league_results,
    accept_level_up,
    accept_mystery_box,
    accept_relic_claim,
    complete_finish,
    handle_anti_bot,
    handle_connection_lost,
    open_relic_complete,
    play_game,
    purchase_cookie_relay,
    purchase_desired_random_boost,
    purchase_fast_start,
    start_game,
    using_cookie_relay,
    using_fast_start,
)
from config import (
    BOOST_17P_BASE_SPEED_TEMPLATE,
    BOOST_15P_SCORE_BONUS_TEMPLATE,
    BOOST_20P_HP_FROM_POTIONS_TEMPLATE,
    BOOST_2PIT_LIFTS_TEMPLATE,
    BOOST_70P_CRUSH_CHANCE_TEMPLATE,
    BOOST_DOUBLE_COINS_TEMPLATE,
    BOOST_GOLD_COIN_MAGIC_TEMPLATE,
    BOOST_M15P_HP_DRAIN_TEMPLATE,
    BOOST_M30P_COLLISION_DAMAGE_TEMPLATE,
    BOOST_MAGNETIC_AURA_TEMPLATE,
    BOOST_REVIVE_ONCE_WITH_80HP_TEMPLATE,
    DEVICE_IP,
    DEVICE_PORT,
    SESSION_RESET_INTERVAL,
)
from detection import detect_stage

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
        session_start_time = time.time()
        session_reset_interval = random.uniform(*SESSION_RESET_INTERVAL)

        while True:
            device_screen = device_capture_screen(DEVICE_IP, DEVICE_PORT)
            stage = detect_stage(device_screen)

            if stage == last_stage:
                time.sleep(0.5)
                continue

            last_stage = stage

            if stage == "MAINMENU":
                print("🎮 Detected Stage: MAINMENU")
                elapsed = time.time() - session_start_time
                if elapsed >= session_reset_interval:
                    print(f"🔄 Session reset triggered after {elapsed / 3600:.2f}h — restarting app...")
                    device_reset_app(DEVICE_IP, DEVICE_PORT)
                    time.sleep(30)
                    session_start_time = time.time()
                    session_reset_interval = random.uniform(*SESSION_RESET_INTERVAL)
                    last_stage = None
                    is_first_game = True
                    continue
                if not is_first_game:
                    delay = random.uniform(30, 60)
                    print(f"⏳ Waiting for {delay:.2f} seconds before starting the next game...")
                    time.sleep(delay)
                is_first_game = False
                start_game()
            elif stage == "PURCHASE_ITEM":
                print("🛒 Detected Stage: PURCHASE_ITEM")
                if options["use_fast_start"]:
                    purchase_fast_start()
                if options["use_cookie_relay"]:
                    purchase_cookie_relay()
                if options["use_desired_random_boost"]:
                    purchase_desired_random_boost(options["desired_boost_template"], options["desired_boost_name"])
                play_game()
            elif stage == "GAME_START":
                print("🏁 Detected Stage: GAME_START")
                if options["use_fast_start"]:
                    using_fast_start()
            elif stage == "GAME_RELAY":
                print("🔄 Detected Stage: GAME_RELAY")
                if options["use_cookie_relay"]:
                    using_cookie_relay()
            elif stage == "GAME_COMPLETE":
                print("✅ Detected Stage: GAME_COMPLETE")
                complete_finish()
            elif stage == "MYSTERY_BOX":
                print("🎁 Detected Stage: MYSTERY_BOX")
                accept_mystery_box()
                time.sleep(3)
                last_stage = None
            elif stage == "CONGRATULATIONS":
                print("🎉 Detected Stage: CONGRATULATIONS")
                accept_congratulations()
                last_stage = None
            elif stage == "LEVEL_UP":
                print("⬆️ Detected Stage: LEVEL_UP")
                accept_level_up()
            elif stage == "DAILY_CHECKIN":
                print("📅 Detected Stage: DAILY_CHECKIN")
                accept_daily_checkin()
            elif stage == "DAILY_TREASURE":
                print("💎 Detected Stage: DAILY_TREASURE")
                accept_daily_treasure()
            elif stage == "ENTER_LEAGUE":
                print("🏆 Detected Stage: ENTER_LEAGUE")
                accept_enter_league()
            elif stage == "LEAGUE_RESULTS":
                print("🏆 Detected Stage: LEAGUE_RESULTS")
                accept_league_results()
            elif stage == "RELIC_COMPLETE":
                print("🏺 Detected Stage: RELIC_COMPLETE")
                open_relic_complete()
            elif stage == "RELIC_CLAIM":
                print("🏺 Detected Stage: RELIC_CLAIM")
                accept_relic_claim()
            elif stage == "ANTI_BOT":
                print("⚠️ Detected Stage: ANTI_BOT")
                handle_anti_bot(device_screen)
                last_stage = None
            elif stage == "CONNECTION_LOST":
                print("🔌 Detected Stage: CONNECTION_LOST")
                handle_connection_lost()
                last_stage = None

            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n\n🛑 Bot stopped by user.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
