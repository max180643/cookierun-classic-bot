import os
import time

import cv2

def save_debug_screen(screen):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"debug_screen_{timestamp}.png"
    folder = "debug_screens"
    if not os.path.exists(folder):
        os.makedirs(folder)
    filepath = os.path.join(folder, filename)
    cv2.imwrite(filepath, screen)
    print(f"💾 Saved screen to {filepath}")
