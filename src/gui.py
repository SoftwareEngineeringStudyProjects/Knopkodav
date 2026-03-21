import tkinter as tk
from src.recorder import start_recording, stop_recording
from src.screenshot import capture_screenshot
from src.config import INTERVAL
import threading
import time

class UIAutomationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("UI Automation Tool")

        # Start/Stop Recording Button
        self.record_button = tk.Button(root, text="Start Recording", command=self.toggle_recording)
        self.record_button.pack(pady=10)

        # Quit Button
        self.quit_button = tk.Button(root, text="Quit", command=root.quit)
        self.quit_button.pack(pady=10)

        self.is_recording = False
        self.record_thread = None  # Track the thread

    def toggle_recording(self):
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        if self.record_thread is not None and self.record_thread.is_alive():
            # If the thread is alive, do not start a new one
            print("Recording is already in progress.")
            return

        # Reset thread if it was previously finished
        if self.record_thread is not None and not self.record_thread.is_alive():
            self.record_thread = None  # This allows a new thread to be created

        self.is_recording = True
        self.record_button.config(text="Stop Recording")

        # Create a new thread for recording
        self.record_thread = threading.Thread(target=self.record_activity)
        self.record_thread.daemon = True  # Daemon thread will exit when the main program exits
        self.record_thread.start()

    def stop_recording(self):
        self.is_recording = False
        self.record_button.config(text="Start Recording")
        stop_recording()  # Ensure you implement stop_recording logic in recorder.py

    def record_activity(self):
        # Start recording mouse and keyboard events
        start_recording()

        # Periodically capture screenshots
        while self.is_recording:
            capture_screenshot()
            time.sleep(INTERVAL)  # Adjust the interval as needed

def run_gui():
    root = tk.Tk()
    app = UIAutomationApp(root)
    root.mainloop()