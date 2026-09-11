import json
import socket
import urllib.error
import urllib.request

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def send_telegram_alert(message: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("🔔 Telegram alert skipped (TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID not set).")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = json.dumps({"chat_id": TELEGRAM_CHAT_ID, "text": message}).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        urllib.request.urlopen(request, timeout=10)
        print("🔔 Telegram alert sent.")
    except (socket.gaierror, urllib.error.URLError) as e:
        print(f"🔔 Couldn't send Telegram alert — looks like your internet connection dropped: {e}")
    except Exception as e:
        print(f"🔔 Failed to send Telegram alert: {e}")
