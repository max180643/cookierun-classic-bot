import random
import subprocess
import time

import cv2
import numpy as np


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


def safe_device_scroll(ip: str, port: int, x: int, y: int, direction: str = "up", distance: int = 500, duration: int = 300):
    jx = x + random.randint(-15, 15)
    jy = y + random.randint(-15, 15)
    direction_map = {
        "up":    (jx, jy + distance, jx, jy - distance),
        "down":  (jx, jy - distance, jx, jy + distance),
        "left":  (jx + distance, jy, jx - distance, jy),
        "right": (jx - distance, jy, jx + distance, jy),
    }
    if direction not in direction_map:
        raise ValueError(f"Invalid direction '{direction}'. Use: up, down, left, right.")
    x1, y1, x2, y2 = direction_map[direction]
    subprocess.run(
        ["adb", "-s", f"{ip}:{port}", "shell", "input", "swipe",
         str(x1), str(y1), str(x2), str(y2), str(duration)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )


def device_is_app_running(ip: str, port: int, package: str) -> bool:
    result = subprocess.run(
        ["adb", "-s", f"{ip}:{port}", "shell", "pidof", package],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return bool(result.stdout.strip())


def device_reset_app(ip: str, port: int, package: str = "com.devsisters.crg", max_retries: int = 5):
    print(f"🔄 Resetting app {package} on device at {ip}:{port}...")
    subprocess.run(
        ["adb", "-s", f"{ip}:{port}", "shell", "cmd", "activity", "force-stop", package],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    print(f"⏳ Waiting 15 seconds for app {package} to stop...")
    time.sleep(15)

    for attempt in range(1, max_retries + 1):
        print(f"📱 Restarting app {package} on device at {ip}:{port} (attempt {attempt}/{max_retries})...")
        subprocess.run(
            ["adb", "-s", f"{ip}:{port}", "shell", "monkey", "-p", package, "1"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"⏳ Waiting 15 seconds to check if app started...")
        time.sleep(15)

        if device_is_app_running(ip, port, package):
            print(f"📊 App {package} is running, verifying stability...")
            stable = True
            for check in range(1, 4):
                time.sleep(20)
                if not device_is_app_running(ip, port, package):
                    print(f"💥 App {package} crashed during stability check ({check}/3).")
                    stable = False
                    break
                print(f"✅ Stability check {check}/3 passed.")
            if stable:
                print(f"✅ App {package} is stable.")
                return

        print(f"💥 App {package} appears to have crashed after launch.")
        if attempt < max_retries:
            print(f"🔁 Retrying in 5 seconds...")
            time.sleep(5)

    raise Exception(f"❌ Failed to start {package} after {max_retries} attempts.")
