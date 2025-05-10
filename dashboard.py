import streamlit as st
import pandas as pd
import os
import cv2
import tempfile
from datetime import datetime
import time

# === Config ===
st.set_page_config(page_title="Gunny Bag Dashboard", layout="wide")
st.title("🧺 Real-Time Gunny Bag Detection Dashboard")

# === Constants ===
CSV_PATH = "data/count_data.csv"
VIDEO_PATH = "data/video1.mp4"  # same as main.py
FRAME_INTERVAL = 1  # seconds between frame updates

# === Function to get video frame ===
def get_video_frame(video_path, pos_frame):
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, pos_frame)
    ret, frame = cap.read()
    cap.release()
    return frame if ret else None

# === Load CSV ===
if not os.path.exists(CSV_PATH):
    st.error("❌ count_data.csv not found. Run main.py first.")
    st.stop()

# === Layout ===
col1, col2 = st.columns([2, 1])
chart_placeholder = st.empty()
video_placeholder = col1.empty()
metrics_placeholder = col2.empty()
log_placeholder = st.expander("📄 Full Count Log", expanded=False)

# === Get total frames ===
video_cap = cv2.VideoCapture(VIDEO_PATH)
fps = video_cap.get(cv2.CAP_PROP_FPS)
total_frames = int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT))
video_cap.release()

# === Live Refresh Loop ===
pos_frame = 0
while True:
    # 1. Load latest data
    try:
        df = pd.read_csv(CSV_PATH, names=["Timestamp", "Count"], skiprows=1)
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        latest = df.iloc[-1]
        total_count = int(latest["Count"])
    except:
        time.sleep(1)
        continue

    # 2. Show live video snapshot
    frame = get_video_frame(VIDEO_PATH, pos_frame)
    if frame is not None:
        frame_bgr = cv2.resize(frame, (720, 400))
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        video_placeholder.image(frame_rgb, caption="Live Video Feed", channels="RGB")

    # 3. Show metrics
    with metrics_placeholder:
        st.metric("📦 Total Bags Counted", total_count)
        st.caption(f"🕒 Last update: {latest['Timestamp']}")

    # 4. Line chart
    chart_placeholder.line_chart(df.set_index("Timestamp")[["Count"]])
    df = df.drop_duplicates(subset="Count", keep="last")

    # 5. Log table
    with log_placeholder:
        st.dataframe(df[::-1], use_container_width=True)

    # 6. Update frame
    pos_frame += int(fps * FRAME_INTERVAL)
    if pos_frame >= total_frames:
        pos_frame = 0  # loop

    time.sleep(FRAME_INTERVAL)
