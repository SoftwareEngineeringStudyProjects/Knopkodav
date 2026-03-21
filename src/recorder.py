from pynput import mouse, keyboard
import time
from src.event_logger import log_event

# Global variables to store the listeners
mouse_listener = None
keyboard_listener = None

# List to store events
events = []

# Callback for mouse events
def on_move(x, y):
    events.append({"event": "move", "x": x, "y": y, "time": time.time()})
    log_event(events[-1])

def on_click(x, y, button, pressed):
    events.append({"event": "click", "x": x, "y": y, "button": str(button), "pressed": pressed, "time": time.time()})
    log_event(events[-1])

def on_scroll(x, y, dx, dy):
    events.append({"event": "scroll", "x": x, "y": y, "dx": dx, "dy": dy, "time": time.time()})
    log_event(events[-1])

# Callback for keyboard events
def on_press(key):
    try:
        events.append({"event": "key_press", "key": str(key.char), "time": time.time()})
        log_event(events[-1])
    except AttributeError:
        events.append({"event": "key_press", "key": str(key), "time": time.time()})
        log_event(events[-1])

def on_release(key):
    if key == keyboard.Key.esc:
        return False  # Stop listener

# Start recording: starts the listeners
def start_recording():
    global mouse_listener, keyboard_listener

    # Start a new listener only if the listeners are not already running
    if mouse_listener is None or not mouse_listener.running:
        mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
        mouse_listener.start()

    if keyboard_listener is None or not keyboard_listener.running:
        keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        keyboard_listener.start()

# Stop recording: stops the listeners
def stop_recording():
    global mouse_listener, keyboard_listener

    if mouse_listener is not None and mouse_listener.running:
        mouse_listener.stop()

    if keyboard_listener is not None and keyboard_listener.running:
        keyboard_listener.stop()

    # Reset the listeners for the next start
    mouse_listener = None
    keyboard_listener = None