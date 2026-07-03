import os

import cv2
import numpy as np

from config import (
    ANTI_BOT_CARD_HEIGHT,
    ANTI_BOT_CARD_POS_6,
    ANTI_BOT_CARD_WIDTH,
    ANTI_BOT_CARD_POS_1,
    ANTI_BOT_CARD_POS_2,
    ANTI_BOT_CARD_POS_3,
    ANTI_BOT_CARD_POS_4,
    ANTI_BOT_CARD_POS_5,
    ANTI_BOT_CARD_POS_6,
    MATCH_THRESHOLD,
    STAGE_TEMPLATES,
    TEMPLATE_DIR,
)


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


def detect_anti_bot_odd_cards(screen):
    """
    Return 0-based indices of the 2 cards that differ from the majority 4.

    Strategy:
      1. Crop each card region.
      2. Build a pairwise HSV-histogram similarity matrix (6x6).
      3. For each card, compute its average similarity to all others.
      4. The 2 cards with the lowest average similarity are the odd ones.
    """

    # Define card coordinates based on config constants
    card_coords = [
        ANTI_BOT_CARD_POS_1,
        ANTI_BOT_CARD_POS_2,
        ANTI_BOT_CARD_POS_3,
        ANTI_BOT_CARD_POS_4,
        ANTI_BOT_CARD_POS_5,
        ANTI_BOT_CARD_POS_6,
    ]

    # Crop card regions as grayscale for structural comparison
    crops = []
    for cx, cy in card_coords:
        crop = screen[cy:cy + ANTI_BOT_CARD_HEIGHT, cx:cx + ANTI_BOT_CARD_WIDTH]
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        crops.append(gray)

    # Pairwise structural similarity via normalized cross-correlation
    n = len(crops)
    sim = np.zeros((n, n), dtype=np.float32)
    for i in range(n):
        for j in range(n):
            if i != j:
                result = cv2.matchTemplate(crops[i], crops[j], cv2.TM_CCOEFF_NORMED)
                sim[i][j] = result[0][0]

    # Average similarity of each card against all others (excluding self)
    avg_sim = sim.sum(axis=1) / (n - 1)
    print("🔍 Analyzing card similarity...")
    for idx, s in enumerate(avg_sim):
        print(f"  Card {idx + 1}: similarity score {s:.2f}")

    # The 2 cards with the lowest average similarity are the odd ones
    odd_indices = list(np.argsort(avg_sim)[:2])
    return odd_indices
