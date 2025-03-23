# utils/logger.py
import datetime
import json
import os

LOG_FILE = "error_log.json"

def log_error(error_message: str):
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "error": error_message
    }
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        except:
            logs = []
    logs.append(log_entry)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

def get_recent_errors(limit: int = 10):
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
            return logs[-limit:]
        except:
            return []
    else:
        return []
