# main.py
import cv2
import pandas as pd
from ultralytics import YOLO
import cvzone
import os
import datetime
import csv
from src.tracker import Tracker

# ---------- Paths ----------
video_path = "data/video1.mp4"
weights_file = "weights/coco1.txt"
model_path = "weights/best.pt"
csv_file_path = "data/count_data.csv"

# ---------- Pre-checks ----------
if not os.path.exists(video_path):
    raise FileNotFoundError(f"Video file '{video_path}' not found.")
if not os.path.exists(weights_file):
    raise FileNotFoundError(f"Class list file '{weights_file}' not found.")
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file '{model_path}' not found.")

# ---------- Create data folder if missing ----------
os.makedirs("data", exist_ok=True)

# ---------- Create CSV if not exists ----------
if not os.path.exists(csv_file_path):
    with open(csv_file_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Count"])

# ---------- Load YOLO model ----------
model = YOLO(model_path)

# ---------- Load Video ----------
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    raise FileNotFoundError(f"Cannot open video file '{video_path}'.")

original_fps = cap.get(cv2.CAP_PROP_FPS)
frame_interval = int(original_fps / 10) if original_fps else 3

with open(weights_file, "r") as f:
    class_list = f.read().split("\n")

# ---------- Initial Variables ----------
frame_count = 0
tracker = Tracker()
cy1, cy2 = 200, 300  # Conveyor ROI Y-axis limits
offset = 10
count = 0
prev_count = 0
ids = []

# ---------- Start Loop ----------
while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video.")
        break

    if frame_count % frame_interval != 0:
        frame_count += 1
        continue

    frame_count += 1
    frame = cv2.resize(frame, (1020, 500))
    output_image = frame.copy()
    results = model.predict(frame)

    if not results or not results[0].boxes.data.size:
        cv2.imshow("RGB", output_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    a = results[0].boxes.data.detach().cpu().numpy()
    px = pd.DataFrame(a).astype("float")
    detections = [[int(row[0]), int(row[1]), int(row[2]), int(row[3])] for _, row in px.iterrows()]

    bbox_id = tracker.update(detections)

    for bbox in bbox_id:
        x3, y3, x4, y4, obj_id = bbox
        cx, cy = (x3 + x4) // 2, (y3 + y4) // 2
        cv2.circle(output_image, (cx, cy), 4, (0, 0, 255), -1)
        cv2.putText(output_image, str(obj_id), (cx, cy), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)

        if cy1 <= cy <= cy2:
            cv2.rectangle(output_image, (x3, y3), (x4, y4), (0, 255, 0), 2)

        if (cy1 - offset < cy < cy1 + offset) or (cy2 - offset < cy < cy2 + offset):
            if obj_id not in ids:
                count += 1
                ids.append(obj_id)
                current_time = datetime.datetime.now().replace(microsecond=0)

                # ✅ Only log if count increased
                if count > prev_count:
                    print(f"[LOG] Count: {count} at {current_time}")
                    with open(csv_file_path, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([current_time, count])
                    prev_count = count

    # ---------- Draw overlay ----------
    cv2.line(output_image, (100, cy1), (900, cy1), (0, 0, 255), 2)
    cv2.putText(output_image, 'Counter Line 1', (90, cy1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
    cv2.line(output_image, (100, cy2), (900, cy2), (0, 0, 255), 2)
    cv2.putText(output_image, 'Counter Line 2', (90, cy2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
    cv2.putText(output_image, f'Count: {count}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

    cv2.imshow("RGB", output_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
