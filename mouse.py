from pynput import mouse, keyboard
import time

def rec_mouse():
    """
    Records mouse movements and clicks with timing.
    Stops recording when Escape key is pressed.
    Returns a list of (event_type, data, time_since_last_event) tuples.
    """
    events = []
    last_time = time.time()

    # Flag to stop listener
    stop_recording = False

    def on_move(x, y):
        nonlocal last_time, stop_recording
        if stop_recording:
            return False
        now = time.time()
        delay = now - last_time
        events.append(('move', (x, y), delay))
        last_time = now

    def on_click(x, y, button, pressed):
        nonlocal last_time, stop_recording
        if stop_recording:
            return False
        now = time.time()
        delay = now - last_time
        action = 'press' if pressed else 'release'
        events.append(('click', (x, y, button.name, action), delay))
        last_time = now

    def on_scroll(x, y, dx, dy):
        # Optional: record scrolls if desired
        pass

    def on_key_press(key):
        nonlocal stop_recording
        if key == keyboard.Key.esc:
            stop_recording = True
            return False  # Stop keyboard listener

    print("Recording mouse events... Press Escape key to stop.")

    # Start keyboard listener to catch escape key
    with keyboard.Listener(on_press=on_key_press) as keyboard_listener:
        # Start mouse listener (blocking)
        with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as mouse_listener:
            mouse_listener.join()

        keyboard_listener.join()

    return events


def play_mouse(events):
    from pynput.mouse import Controller, Button

    mouse_controller = Controller()

    for event_type, data, delay in events:
        time.sleep(delay)

        if event_type == 'move':
            x, y = data
            mouse_controller.position = (x, y)

        elif event_type == 'click':
            x, y, button_name, action = data
            mouse_controller.position = (x, y)
            btn = getattr(Button, button_name)
            if action == 'press':
                mouse_controller.press(btn)
            else:
                mouse_controller.release(btn)


if __name__ == "__main__":
    events = rec_mouse()

    import pickle
    with open("mouse_rec.pkl", "wb") as f:
        pickle.dump(events, f)

    # Playback after a delay
    time.sleep(2)
    with open("mouse_rec.pkl", "rb") as f:
        events = pickle.load(f)
    play_mouse(events)
