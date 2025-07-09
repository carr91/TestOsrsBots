import pyautogui
from PIL import ImageGrab
import time
import random
import math
from collections import deque

def is_similar(c1, c2, tol):
    return all(abs(a - b) <= tol for a, b in zip(c1, c2))

def find_color_and_click(target_color_hex, tolerance=10):
    """
    Finds blobs of the target color and clicks the centroid of the largest blob.
    """
    target_color = tuple(int(target_color_hex[i:i+2], 16) for i in (0, 2, 4))

    screenshot = ImageGrab.grab()
    width, height = screenshot.size
    pixels = screenshot.load()
    visited = [[False] * width for _ in range(height)]

    def get_neighbors(x, y):
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                yield nx, ny

    blobs = []

    for y in range(height):
        for x in range(width):
            if visited[y][x]:
                continue

            current_color = pixels[x, y][:3]
            if is_similar(current_color, target_color, tolerance):
                # Start BFS for this blob
                blob = []
                queue = deque()
                queue.append((x, y))
                visited[y][x] = True

                while queue:
                    cx, cy = queue.popleft()
                    blob.append((cx, cy))

                    for nx, ny in get_neighbors(cx, cy):
                        if not visited[ny][nx] and is_similar(pixels[nx, ny][:3], target_color, tolerance):
                            visited[ny][nx] = True
                            queue.append((nx, ny))

                blobs.append(blob)

    if not blobs:
        return False

    # Pick largest blob
    largest_blob = max(blobs, key=len)

    # Compute centroid
    sum_x = sum(x for x, y in largest_blob)
    sum_y = sum(y for x, y in largest_blob)
    count = len(largest_blob)
    centroid_x = sum_x // count
    centroid_y = sum_y // count

    smooth_move_and_click(centroid_x, centroid_y)
    return True

def smooth_move_and_click(dest_x, dest_y, duration=random.uniform(.0001, .001)):
    """
    Moves mouse smoothly with slight randomness to (dest_x, dest_y) and left clicks.
    """
    start_x, start_y = pyautogui.position()

    steps = max(int(duration * 100), 10)  # number of small moves
    for i in range(steps):
        t = i / steps
        # Simple ease-in-out interpolation
        ease_t = t*t*(3 - 2*t)

        new_x = int(start_x + (dest_x - start_x) * ease_t + random.uniform(-1, 1))
        new_y = int(start_y + (dest_y - start_y) * ease_t + random.uniform(-1, 1))

        pyautogui.moveTo(new_x, new_y, duration=0)
        time.sleep(duration / steps)

    pyautogui.moveTo(dest_x, dest_y, duration=0)
    time.sleep(0.01)
    pyautogui.click(button='left')
    time.sleep(0.01)


def find_colors_and_click():
    # Find FF00D4 and click
    found1 = find_color_and_click("FF00D4")
    if not found1:
        return False
        print("Color FF00D4 not found.")

    # Small pause between actions
    time.sleep(0.01)

    # Find 00FAFF and click
    found2 = find_color_and_click("00FAFF")
    return True
    if not found2:
        print("Color 00FAFF not found.")
        return False