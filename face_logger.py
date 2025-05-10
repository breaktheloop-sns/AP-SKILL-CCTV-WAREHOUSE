import json
import csv
import os
from datetime import datetime

CSV_PATH = "logs/face_logs.csv"
JSON_PATH = "logs/face_logs.json"

def init_face_logs():
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Name", "Status"])

    if not os.path.exists(JSON_PATH):
        with open(JSON_PATH, "w") as f:
            json.dump([], f)

def log_face(name, status):
    timestamp = datetime.now().isoformat()

    # Log to CSV
    with open(CSV_PATH, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, name, status])

    # Log to JSON
    try:
        with open(JSON_PATH, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append({
        "timestamp": timestamp,
        "name": name,
        "status": status
    })

    with open(JSON_PATH, "w") as f:
        json.dump(data, f, indent=4)
