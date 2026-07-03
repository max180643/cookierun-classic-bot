import os

import cv2

from config import MATCH_THRESHOLD, STAGE_TEMPLATES, TEMPLATE_DIR


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
