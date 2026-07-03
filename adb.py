import random
import subprocess

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
