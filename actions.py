import random
import time

from adb import safe_device_tap, safe_device_scroll, device_capture_screen
from config import (
    ACCEPT_ALL_LIVES_RECEIVED_AND_SENT_BUTTON,
    ACCEPT_CONGRATULATIONS_BUTTON,
    ACCEPT_DAILY_CHECKIN_BOOST_SET_BUTTON,
    ACCEPT_DAILY_CHECKIN_BUTTON,
    ACCEPT_DAILY_TREASURE_BUTTON,
    ACCEPT_DAILY_NEW_BUTTON,
    ACCEPT_ENTER_LEAGUE_BUTTON,
    ACCEPT_LEAGUE_RESULTS_BUTTON,
    ACCEPT_LEVEL_UP_BUTTON,
    ACCEPT_MYSTERY_BOX_BUTTON,
    ACCEPT_OVERTAKE_BREAK_SCORE_BUTTON,
    ACCEPT_PREVIOUS_RANK_RESULTS_BUTTON,
    ACCEPT_TOO_MANY_TREASURES_BUTTON,
    ALL_LIVES_RECEIVED_AND_SENT_REGION,
    ALL_LIVES_RECEIVED_AND_SENT_TEMPLATE,
    CANCEL_SEND_LIFE_BUTTON,
    CLOSE_ANNOUNCEMENT_DIALOG_BUTTON,
    CLOSE_SEND_LIFE_DIALOG_BUTTON,
    COMPLETE_FINISH_BUTTON,
    CONFIRM_SEND_LIFE_BUTTON,
    CONFIRM_SEND_LIFE_REGION,
    CONFIRM_SEND_LIFE_TEMPLATE,
    COOKIE_RELAY_ITEM,
    COOKIE_RELAY_USE_BUTTON,
    DEVICE_IP,
    DEVICE_PORT,
    EXIT_GAME_SETTINGS_BUTTON,
    EXIT_PARTY_RUN_MODE_BUTTON,
    FAST_START_ITEM,
    FAST_START_USE_BUTTON,
    FRIEND_BOTTOM_LEADERBOARD_REGION,
    FRIEND_BOTTOM_LEADERBOARD_TEMPLATE,
    FRIEND_COOKIE_DIALOG_CLOSE_BUTTON,
    FRIEND_COOKIE_DIALOG_REGION,
    FRIEND_COOKIE_DIALOG_TEMPLATE,
    FRIEND_INFO_DIALOG_CLOSE_BUTTON,
    FRIEND_INFO_DIALOG_REGION,
    FRIEND_INFO_DIALOG_TEMPLATE,
    FRIEND_SEND_LIFE_REGION,
    FRIEND_SEND_LIFE_TEMPLATE,
    FRIEND_TOP_LEADERBOARD_REGION,
    FRIEND_TOP_LEADERBOARD_TEMPLATE,
    INACTIVE_RELOAD_BUTTON,
    LEADERBOARD_BOTTOM_POSITION,
    LEADERBOARD_TOP_POSITION,
    MAIL_BOX_BUTTON,
    MAIL_BOX_LIVES_TAB_BUTTON,
    MAIL_BOX_CLOSE_BUTTON,
    MULTI_BUY_BUTTON,
    MULTI_PURCHASE_BUTTON,
    NO_LIVES_TO_RECEIVE_REGION,
    NO_LIVES_TO_RECEIVE_TEMPLATE,
    NO_LIVES_TO_RECEIVE_TEMPLATE,
    PLAY_BUTTON,
    PURCHASE_BUTTON,
    QUICK_RECEIVE_AND_SEND_LIVES_BUTTON,
    RANDOM_BOOST_ITEM,
    RANDOM_BOOST_REGION,
    RELIC_CLAIM_BUTTON,
    RELIC_CLOSE_BUTTON,
    RELIC_COMPLETE_BUTTON,
    SEND_LIFE_CONFIRM_DIALOG_REGION,
    SEND_LIFE_CONFIRM_DIALOG_TEMPLATE,
    SEND_LIFE_CONFIRM_TIMEOUT,
    SEND_LIFE_MAX_TRANSITION_FAILURES,
    SEND_LIFE_NO_BUTTON_MAX_SCROLLS,
    SEND_LIFE_SENT_DIALOG_REGION,
    SEND_LIFE_SENT_DIALOG_TEMPLATE,
    SEND_LIFE_SENT_TIMEOUT,
    SEND_LIFE_TOP_MAX_SCROLLS,
    START_BUTTON,
    CONNECTION_LOST_RELOAD_BUTTON,
)
from detection import detect_templates, detect_anti_bot_odd_cards, detect_stage
from config import (
    ANTI_BOT_CARD_POS_1, ANTI_BOT_CARD_POS_2, ANTI_BOT_CARD_POS_3,
    ANTI_BOT_CARD_POS_4, ANTI_BOT_CARD_POS_5, ANTI_BOT_CARD_POS_6,
    ANTI_BOT_CARD_WIDTH, ANTI_BOT_CARD_HEIGHT,
)

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
        if detect_templates(screen, desired_template, RANDOM_BOOST_REGION):
            print(f"✅ Desired Boost detected: {desired_name}!")
            break
        time.sleep(0.5)


def using_fast_start():
    print("⚡ Using Fast Start...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, FAST_START_USE_BUTTON[0], FAST_START_USE_BUTTON[1])
    time.sleep(random.uniform(0.8, 1.2))


def using_cookie_relay():
    print("🍪 Using Cookie Relay...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, COOKIE_RELAY_USE_BUTTON[0], COOKIE_RELAY_USE_BUTTON[1])
    time.sleep(random.uniform(0.8, 1.2))


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


def accept_daily_checkin():
    print("📅 Accepting Daily Check-in...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, ACCEPT_DAILY_CHECKIN_BUTTON[0], ACCEPT_DAILY_CHECKIN_BUTTON[1])
    time.sleep(random.uniform(0.8, 1.4))


def accept_daily_checkin_boost_set():
    print("📅 Accepting Daily Check-in Boost Set...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, ACCEPT_DAILY_CHECKIN_BOOST_SET_BUTTON[0], ACCEPT_DAILY_CHECKIN_BOOST_SET_BUTTON[1])
    time.sleep(random.uniform(0.8, 1.4))


def accept_daily_treasure():
    print("💎 Accepting Daily Treasure...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, ACCEPT_DAILY_TREASURE_BUTTON[0], ACCEPT_DAILY_TREASURE_BUTTON[1])
    time.sleep(random.uniform(0.8, 1.4))


def accept_daily_new():
    print("📰 Accepting Daily New...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, ACCEPT_DAILY_NEW_BUTTON[0], ACCEPT_DAILY_NEW_BUTTON[1])
    time.sleep(random.uniform(0.8, 1.4))


def accept_enter_league():
    print("🏆 Accepting Enter League...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, ACCEPT_ENTER_LEAGUE_BUTTON[0], ACCEPT_ENTER_LEAGUE_BUTTON[1])
    time.sleep(random.uniform(0.8, 1.4))


def accept_league_results():
    print("🏆 Accepting League Results...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, ACCEPT_LEAGUE_RESULTS_BUTTON[0], ACCEPT_LEAGUE_RESULTS_BUTTON[1])
    time.sleep(random.uniform(0.8, 1.4))


def accept_previous_rank_results():
    print("🏆 Accepting Previous Rank Results...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, ACCEPT_PREVIOUS_RANK_RESULTS_BUTTON[0], ACCEPT_PREVIOUS_RANK_RESULTS_BUTTON[1])
    time.sleep(random.uniform(0.8, 1.4))

def accept_too_many_treasures():
    print("💎 Accepting Too Many Treasures...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, ACCEPT_TOO_MANY_TREASURES_BUTTON[0], ACCEPT_TOO_MANY_TREASURES_BUTTON[1])
    time.sleep(random.uniform(0.8, 1.4))

def accept_overtake_break_score():
    print("🏆 Accepting Overtake Break Score...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, ACCEPT_OVERTAKE_BREAK_SCORE_BUTTON[0], ACCEPT_OVERTAKE_BREAK_SCORE_BUTTON[1])
    time.sleep(random.uniform(0.8, 1.4))

def open_relic_complete():
    print("🏺 Opening Relic Complete...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, RELIC_COMPLETE_BUTTON[0], RELIC_COMPLETE_BUTTON[1])
    time.sleep(random.uniform(0.8, 1.4))


def accept_relic_claim():
    print("🏺 Accepting Relic Claim...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, RELIC_CLAIM_BUTTON[0], RELIC_CLAIM_BUTTON[1])
    time.sleep(random.uniform(0.8, 1.4))
    safe_device_tap(DEVICE_IP, DEVICE_PORT, RELIC_CLOSE_BUTTON[0], RELIC_CLOSE_BUTTON[1])
    time.sleep(random.uniform(10, 15))


def handle_anti_bot(screen):
    print("🤖 Solving Anti-Bot captcha...")
    card_coords = [
        ANTI_BOT_CARD_POS_1, ANTI_BOT_CARD_POS_2, ANTI_BOT_CARD_POS_3,
        ANTI_BOT_CARD_POS_4, ANTI_BOT_CARD_POS_5, ANTI_BOT_CARD_POS_6,
    ]

    odd_indices = detect_anti_bot_odd_cards(screen)
    card_nums = [i + 1 for i in odd_indices]
    print(f"🃏 Found odd cards: Card {card_nums[0]} and Card {card_nums[1]}")

    for idx in odd_indices:
        cx, cy = card_coords[idx]
        # random tap position inside the card, with a small margin
        margin = 20
        tx = random.randint(cx + margin, cx + ANTI_BOT_CARD_WIDTH - margin)
        ty = random.randint(cy + margin, cy + ANTI_BOT_CARD_HEIGHT - margin)
        print(f"  👆 Tapping Card {idx + 1} at ({tx}, {ty})")
        safe_device_tap(DEVICE_IP, DEVICE_PORT, tx, ty)
        time.sleep(random.uniform(10, 15))

    print("✅ Anti-Bot captcha solved!")
    time.sleep(random.uniform(0.8, 1.4))


def handle_connection_lost():
    print("🔌 Handling Connection Lost...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, CONNECTION_LOST_RELOAD_BUTTON[0], CONNECTION_LOST_RELOAD_BUTTON[1])
    time.sleep(random.uniform(10, 15))


def handle_inactive():
    print("💤 Handling Inactive state...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, INACTIVE_RELOAD_BUTTON[0], INACTIVE_RELOAD_BUTTON[1])
    time.sleep(random.uniform(10, 15))


def recover_friend_overlay(screen=None):
    """Close one known friend overlay and report whether recovery was attempted."""
    if screen is None:
        screen = device_capture_screen(DEVICE_IP, DEVICE_PORT)
    if detect_templates(screen, FRIEND_COOKIE_DIALOG_TEMPLATE, FRIEND_COOKIE_DIALOG_REGION):
        print("🧹 Closing unexpected Friend's Cookie dialog...")
        safe_device_tap(
            DEVICE_IP,
            DEVICE_PORT,
            FRIEND_COOKIE_DIALOG_CLOSE_BUTTON[0],
            FRIEND_COOKIE_DIALOG_CLOSE_BUTTON[1],
        )
        time.sleep(0.5)
        return True
    if detect_templates(screen, FRIEND_INFO_DIALOG_TEMPLATE, FRIEND_INFO_DIALOG_REGION):
        print("🧹 Closing unexpected Friend's Info dialog...")
        safe_device_tap(
            DEVICE_IP,
            DEVICE_PORT,
            FRIEND_INFO_DIALOG_CLOSE_BUTTON[0],
            FRIEND_INFO_DIALOG_CLOSE_BUTTON[1],
        )
        time.sleep(0.5)
        return True
    if detect_templates(screen, SEND_LIFE_SENT_DIALOG_TEMPLATE, SEND_LIFE_SENT_DIALOG_REGION):
        print("🧹 Closing leftover message-sent dialog...")
        safe_device_tap(
            DEVICE_IP,
            DEVICE_PORT,
            CLOSE_SEND_LIFE_DIALOG_BUTTON[0],
            CLOSE_SEND_LIFE_DIALOG_BUTTON[1],
        )
        time.sleep(0.5)
        return True
    if detect_templates(screen, SEND_LIFE_CONFIRM_DIALOG_TEMPLATE, SEND_LIFE_CONFIRM_DIALOG_REGION):
        print("🧹 Cancelling leftover send-life confirmation...")
        safe_device_tap(
            DEVICE_IP,
            DEVICE_PORT,
            CANCEL_SEND_LIFE_BUTTON[0],
            CANCEL_SEND_LIFE_BUTTON[1],
        )
        time.sleep(0.5)
        return True
    return False


def _wait_for_template(template_files, region, timeout):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        screen = device_capture_screen(DEVICE_IP, DEVICE_PORT)
        if detect_templates(screen, template_files, region):
            return screen
        time.sleep(0.2)
    return None


def _wait_for_template_to_clear(template_files, region, timeout):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        screen = device_capture_screen(DEVICE_IP, DEVICE_PORT)
        if not detect_templates(screen, template_files, region):
            return screen
        time.sleep(0.2)
    return None


def _send_one_friend_life(match):
    x, y, w, h = match
    print("💌 Sending life to friend...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, x + w // 2, y + h // 2)

    if _wait_for_template(
        SEND_LIFE_CONFIRM_DIALOG_TEMPLATE,
        SEND_LIFE_CONFIRM_DIALOG_REGION,
        SEND_LIFE_CONFIRM_TIMEOUT,
    ) is None:
        print("⚠️ Send-life confirmation did not appear. Skipping blind follow-up taps.")
        return False

    print("💌 Confirming send life...")
    safe_device_tap(
        DEVICE_IP,
        DEVICE_PORT,
        CONFIRM_SEND_LIFE_BUTTON[0],
        CONFIRM_SEND_LIFE_BUTTON[1],
    )

    if _wait_for_template(
        SEND_LIFE_SENT_DIALOG_TEMPLATE,
        SEND_LIFE_SENT_DIALOG_REGION,
        SEND_LIFE_SENT_TIMEOUT,
    ) is None:
        print("⚠️ Message-sent dialog did not appear. Skipping its fixed-coordinate tap.")
        return False

    print("💌 Closing message-sent dialog...")
    safe_device_tap(
        DEVICE_IP,
        DEVICE_PORT,
        CLOSE_SEND_LIFE_DIALOG_BUTTON[0],
        CLOSE_SEND_LIFE_DIALOG_BUTTON[1],
    )
    if _wait_for_template_to_clear(
        SEND_LIFE_SENT_DIALOG_TEMPLATE,
        SEND_LIFE_SENT_DIALOG_REGION,
        SEND_LIFE_CONFIRM_TIMEOUT,
    ) is None:
        print("⚠️ Message-sent dialog did not close.")
        return False
    return True


def handle_send_friend_life():
    print("💌 Handling Send Friend Life...")
    # Scroll leaderboard to top; stop if the expected screen never appears.
    for top_scroll_count in range(1, SEND_LIFE_TOP_MAX_SCROLLS + 1):
        screen = device_capture_screen(DEVICE_IP, DEVICE_PORT)
        if recover_friend_overlay(screen):
            continue
        if detect_templates(screen, FRIEND_TOP_LEADERBOARD_TEMPLATE, FRIEND_TOP_LEADERBOARD_REGION):
            print("✅ Top of Friend Leaderboard reached.")
            break
        print(f"🔄 Scrolling up to find Send Friend Life... ({top_scroll_count}/{SEND_LIFE_TOP_MAX_SCROLLS})")
        safe_device_scroll(DEVICE_IP, DEVICE_PORT, LEADERBOARD_BOTTOM_POSITION[0], LEADERBOARD_BOTTOM_POSITION[1], direction="down", distance=300, duration=150)
        time.sleep(random.uniform(0.8, 1.4))
    else:
        print("⚠️ Friend leaderboard top was not found. Aborting send-life flow.")
        return False

    # Scroll down, tap all send life buttons, stop when bottom leaderboard detected
    no_button_scroll_count = 0
    transition_failure_count = 0
    while True:
        screen = device_capture_screen(DEVICE_IP, DEVICE_PORT)
        if recover_friend_overlay(screen):
            transition_failure_count += 1
            if transition_failure_count >= SEND_LIFE_MAX_TRANSITION_FAILURES:
                print("⚠️ Too many unexpected friend overlays. Aborting send-life flow.")
                return False
            continue
        if detect_templates(screen, FRIEND_BOTTOM_LEADERBOARD_TEMPLATE, FRIEND_BOTTOM_LEADERBOARD_REGION):
            print("✅ Bottom of Friend Leaderboard reached. Done sending lives.")
            return True
        send_life_button_coords = detect_templates(screen, FRIEND_SEND_LIFE_TEMPLATE, FRIEND_SEND_LIFE_REGION)
        if send_life_button_coords:
            no_button_scroll_count = 0
            if _send_one_friend_life(send_life_button_coords[0]):
                transition_failure_count = 0
            else:
                transition_failure_count += 1
                if transition_failure_count >= SEND_LIFE_MAX_TRANSITION_FAILURES:
                    print("⚠️ Too many failed send-life transitions. Aborting send-life flow.")
                    return False
        else:
            no_button_scroll_count += 1
            if no_button_scroll_count >= SEND_LIFE_NO_BUTTON_MAX_SCROLLS:
                print(
                    f"⚠️ No send life buttons found for {SEND_LIFE_NO_BUTTON_MAX_SCROLLS} "
                    "consecutive scrolls. Aborting send-life flow."
                )
                return False
            print(
                "🔄 No send life buttons found, scrolling down... "
                f"({no_button_scroll_count}/{SEND_LIFE_NO_BUTTON_MAX_SCROLLS})"
            )
            safe_device_scroll(DEVICE_IP, DEVICE_PORT, LEADERBOARD_TOP_POSITION[0], LEADERBOARD_TOP_POSITION[1], direction="up", distance=70, duration=150)
            time.sleep(random.uniform(0.8, 1.4))


def handle_quick_receive_and_send_lives():
    print("✉️ Handling Quick Receive and Send Lives...")
    time.sleep(random.uniform(0.8, 1.4))
    # Tap the "Mail" button
    safe_device_tap(DEVICE_IP, DEVICE_PORT, MAIL_BOX_BUTTON[0], MAIL_BOX_BUTTON[1])
    time.sleep(random.uniform(0.8, 1.4))
    # Tap the "Lives" tab
    safe_device_tap(DEVICE_IP, DEVICE_PORT, MAIL_BOX_LIVES_TAB_BUTTON[0], MAIL_BOX_LIVES_TAB_BUTTON[1])
    time.sleep(random.uniform(0.8, 1.4))
    screen = device_capture_screen(DEVICE_IP, DEVICE_PORT)
    # No lives to receive
    if detect_templates(screen, NO_LIVES_TO_RECEIVE_TEMPLATE, NO_LIVES_TO_RECEIVE_REGION):
        print("✉️ No lives to receive. Proceeding to send lives...")
        # Close the mail dialog
        safe_device_tap(DEVICE_IP, DEVICE_PORT, MAIL_BOX_CLOSE_BUTTON[0], MAIL_BOX_CLOSE_BUTTON[1])
        return
    # Receive all lives
    print("✉️ Receiving all lives...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, QUICK_RECEIVE_AND_SEND_LIVES_BUTTON[0], QUICK_RECEIVE_AND_SEND_LIVES_BUTTON[1])
    time.sleep(random.uniform(0.8, 1.4))
    # Tap all send life buttons
    while True:
        # Check if all lifes received and sent!, so break the loop
        screen = device_capture_screen(DEVICE_IP, DEVICE_PORT)
        all_lives_received_and_sent = detect_templates(screen, ALL_LIVES_RECEIVED_AND_SENT_TEMPLATE, ALL_LIVES_RECEIVED_AND_SENT_REGION)
        if all_lives_received_and_sent:
            print("✉️ All lives received and sent. Done!")
            # Tap the "Confirm" button
            safe_device_tap(DEVICE_IP, DEVICE_PORT, ACCEPT_ALL_LIVES_RECEIVED_AND_SENT_BUTTON[0], ACCEPT_ALL_LIVES_RECEIVED_AND_SENT_BUTTON[1])
            time.sleep(random.uniform(0.8, 1.4))
            # Close the mail dialog
            safe_device_tap(DEVICE_IP, DEVICE_PORT, MAIL_BOX_CLOSE_BUTTON[0], MAIL_BOX_CLOSE_BUTTON[1])
            time.sleep(random.uniform(0.8, 1.4))
            break
        # Send lifes to friends
        confirm_send_life_button_coords = detect_templates(screen, CONFIRM_SEND_LIFE_TEMPLATE, CONFIRM_SEND_LIFE_REGION)
        if confirm_send_life_button_coords:
            print("✉️ Sending lives to friends...")
            safe_device_tap(DEVICE_IP, DEVICE_PORT, CONFIRM_SEND_LIFE_BUTTON[0], CONFIRM_SEND_LIFE_BUTTON[1])
            time.sleep(random.uniform(0.8, 1.4))
    print("✉️ Quick Receive and Send Lives completed.")


def close_announcement_dialog():
    print("🖱️ Closing announcement dialog...")
    for i in range(5):
        print(f"🖱️ Tapping close announcement dialog button {i+1}/5")
        safe_device_tap(DEVICE_IP, DEVICE_PORT, CLOSE_ANNOUNCEMENT_DIALOG_BUTTON[0], CLOSE_ANNOUNCEMENT_DIALOG_BUTTON[1])
        time.sleep(random.uniform(0.8, 1.4))
    time.sleep(random.uniform(0.8, 1.4))
    device_screen = device_capture_screen(DEVICE_IP, DEVICE_PORT)
    if detect_stage(device_screen, ["PARTY_RUN"]) == "PARTY_RUN":
        close_party_run_mode()
    elif detect_stage(device_screen, ["GAME_SETTINGS"]) == "GAME_SETTINGS":
        close_game_settings()


def close_party_run_mode():
    print("🖱️ Closing Party Run mode...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, EXIT_PARTY_RUN_MODE_BUTTON[0], EXIT_PARTY_RUN_MODE_BUTTON[1])
    time.sleep(random.uniform(0.8, 1.4))


def close_game_settings():
    print("🖱️ Closing Game Settings...")
    safe_device_tap(DEVICE_IP, DEVICE_PORT, EXIT_GAME_SETTINGS_BUTTON[0], EXIT_GAME_SETTINGS_BUTTON[1])
    time.sleep(random.uniform(0.8, 1.4))
