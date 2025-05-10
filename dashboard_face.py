import streamlit as st
import pandas as pd
import os
import json

LOG_PATH = "logs/face_logs.json"

st.set_page_config(page_title="🧠 Face Log Dashboard", layout="wide")
st.title("👤 Face Recognition Access Log")

# Load logs
if not os.path.exists(LOG_PATH):
    st.warning("Face log file not found.")
    st.stop()

with open(LOG_PATH) as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Search UI
st.subheader("🔍 Search Logs by Name")
query = st.text_input("Enter name (e.g., Santosh, Kaushik):").strip().lower()

if query:
    filtered = df[df["name"].str.lower().str.contains(query)]
    if filtered.empty:
        st.error("No matching records found.")
    else:
        st.success(f"Found {len(filtered)} entries.")
        st.dataframe(filtered)
else:
    st.subheader("📋 Recent Logs")
    st.dataframe(df.tail(15).sort_values("timestamp", ascending=False))
