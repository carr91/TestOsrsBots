import cv2
import numpy as np
import pyautogui
import time
import random
from pynput.mouse import Controller, Button
from math import sqrt

def click_yellow(min_area=300, move_duration=0.6):
    """Detects yellow polygons on screen and clicks the center of the closest one to screen center."""
    
    centers = []
    while not centers:
        # Screenshot and convert to OpenCV BGR
        screenshot = pyautogui.screenshot()
        screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Convert to HSV and mask yellow
        hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)
        lower_yellow = np.array([20, 250, 250])
        upper_yellow = np.array([40, 255, 255])
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # Morph cleanup
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((5, 5), np.uint8))

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Get screen center
        screen_w, screen_h = pyautogui.size()
        screen_center = (screen_w // 2, screen_h // 2)

        def distance(p1, p2):
            return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

        # Filter valid polygon contours and compute centers
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < min_area:
                continue
            M = cv2.moments(cnt)
            if M["m00"] == 0:
                continue
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            centers.append((cx, cy))
            
    # Choose closest to screen center
    closest = min(centers, key=lambda p: distance(p, screen_center))

    # Humanlike mouse movement
    def move_mouse_smoothly(to_x, to_y, duration=0.6):
        mouse = Controller()
        from_x, from_y = pyautogui.position()
        steps = int(duration * 100)
        for i in range(steps):
            t = i / steps
            t = t * t * (3 - 2 * t)
            x = int(from_x + (to_x - from_x) * t + random.uniform(-1, 1))
            y = int(from_y + (to_y - from_y) * t + random.uniform(-1, 1))
            mouse.position = (x, y)
            time.sleep(duration / steps)

    # Move and click
    move_mouse_smoothly(*closest, duration=move_duration)
    time.sleep(random.uniform(0.1, 0.25))
    mouse = Controller()
    mouse.click(Button.left, 1)
    return True

import cv2
import numpy as np
import pyautogui
import time
import random
from pynput.mouse import Controller, Button
from math import sqrt

def click_blue(min_area=300, move_duration=0.6):
    """Detects blue polygons on screen and clicks the center of the closest one to screen center."""
    
    # Screenshot and convert to OpenCV BGR
    screenshot = pyautogui.screenshot()
    screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Convert to HSV and mask blue
    hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([100, 150, 100])
    upper_blue = np.array([130, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Morph cleanup
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((5, 5), np.uint8))

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Get screen center
    screen_w, screen_h = pyautogui.size()
    screen_center = (screen_w // 2, screen_h // 2)

    def distance(p1, p2):
        return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

    # Filter valid contours and compute centers
    centers = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < min_area:
            continue
        M = cv2.moments(cnt)
        if M["m00"] == 0:
            continue
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        centers.append((cx, cy))

    if not centers:
        print("No blue polygons found.")
        return False

    # Choose closest to screen center
    closest = min(centers, key=lambda p: distance(p, screen_center))

    # Humanlike mouse movement
    def move_mouse_smoothly(to_x, to_y, duration=0.6):
        mouse = Controller()
        from_x, from_y = pyautogui.position()
        steps = int(duration * 100)
        for i in range(steps):
            t = i / steps
            t = t * t * (3 - 2 * t)
            x = int(from_x + (to_x - from_x) * t + random.uniform(-1, 1))
            y = int(from_y + (to_y - from_y) * t + random.uniform(-1, 1))
            mouse.position = (x, y)
            time.sleep(duration / steps)

    # Move and click
    move_mouse_smoothly(*closest, duration=move_duration)
    time.sleep(random.uniform(0.1, 0.25))
    mouse = Controller()
    mouse.click(Button.left, 1)
    return True

def detect_white_circle_top_center():
    """Detects a white circular blob in the top-middle third of the screen (approx color FFFFFFFF)."""
    
    # Screenshot and convert to OpenCV format (RGB to BGR)
    screenshot = pyautogui.screenshot()
    screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    h, w = screen.shape[:2]

    # Define region: top 1/3 height, center 1/3 width
    x_start = w // 3
    x_end = 2 * w // 3
    y_start = 0
    y_end = h // 3
    cropped = screen[y_start:y_end, x_start:x_end]

    # Convert to grayscale for brightness-based detection
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

    # Threshold to isolate near-white areas (255 or close to it)
    _, binary = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)

    # Find contours in the white areas
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 50 or area > 3000:
            continue  # ignore tiny specks and giant blocks

        perimeter = cv2.arcLength(cnt, True)
        if perimeter == 0:
            continue

        # Circularity = 4πA / P², closer to 1 = more circle-like
        circularity = 4 * np.pi * area / (perimeter ** 2)
        if circularity > 0.7:
            return True

    return False

import time
import cv2
import numpy as np
import pyautogui
import time

INVENTORY_REGION = (1446, 739, 200, 200)
EMPTY_SLOT_PATH = "emptyinv.png"

def is_inventory_full(threshold=0.4):
    # Take screenshot of inventory region
    screenshot = pyautogui.screenshot(region=INVENTORY_REGION)
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Load template
    template = cv2.imread(EMPTY_SLOT_PATH, cv2.IMREAD_COLOR)
    if template is None:
        raise FileNotFoundError(f"{EMPTY_SLOT_PATH} not found or unreadable")

    # Match template
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Debug: print match confidence
    print(f"Best match confidence: {max_val:.3f}")

    # If match above threshold, inventory is NOT full
    return max_val < threshold


import time

def wait_for_xp_drop(check_interval=0.1, timeout=10, verbose=True):
    """
    Waits for a white circle to appear and then disappear in the top-middle of the screen.
    Times out after `timeout` seconds.

    Args:
        check_interval (float): seconds between checks.
        timeout (float): max time to wait in seconds.
        verbose (bool): whether to print status messages.
    
    Returns:
        bool: True if XP drop was detected and completed, False if timeout occurred.
    """
    start_time = time.time()

    if verbose:
        print("Waiting for XP drop to appear...")

    # Wait for XP drop to start
    while not detect_white_circle_top_center():
        if time.time() - start_time > timeout:
            if verbose:
                print("Timeout waiting for XP drop to appear.")
            return False
        time.sleep(check_interval)

    if verbose:
        print("XP drop detected. Waiting for it to disappear...")

    # Wait for XP drop to end
    while detect_white_circle_top_center():
        if time.time() - start_time > timeout:
            if verbose:
                print("Timeout waiting for XP drop to end.")
            return False
        time.sleep(check_interval)

    if verbose:
        print("XP drop ended.")
    return True

