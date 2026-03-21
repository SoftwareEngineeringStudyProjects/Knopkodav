import pyautogui
import time
from src.config import SCREENSHOT_DIR

def capture_screenshot():
    screenshot = pyautogui.screenshot()
    timestamp = time.time()
    screenshot.save(f"{SCREENSHOT_DIR}/screenshot_{timestamp}.png")