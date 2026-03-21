import json
from src.config import LOG_FILE_PATH

def log_event(event):
    try:
        with open(LOG_FILE_PATH, 'a') as file:
            json.dump(event, file)
            file.write("\n")  # Write each event on a new line
    except Exception as e:
        print(f"Error logging event: {e}")