# AP-SKILL-CCTV-WAREHOUSE🛡️ AI-WATCHTOWER: Multi-Agent Surveillance & Intelligence System

AI-WATCHTOWER is a modular, multi-agent surveillance project built for intelligent monitoring of warehouses using computer vision and LLM-based insights. It includes 4 autonomous agents:

- 📦 Gunny Bag Agent — Real-time gunny bag counting and volume analysis on conveyor belt
- 🚘 Number Plate Agent — License plate detection and OCR from video feeds
- 🧑‍🦱 Face Agent — Face recognition with live logging of known/unknown personnel
- 🔍 Anomaly Agent (Chatbot) — LLM-based natural language query interface over event database (bags, faces, vehicles)

---

## 📁 Project Structure

ai_watchtower/
├── agents/
│ ├── gunny_bag_agent_v3/
│ ├── number_plate_agent/
│ ├── face_agent/
│ └── anomaly_agent_friend/

yaml
Copy
Edit

Each folder is a self-contained agent with its own virtual environment (`venv`), models, and dashboard logic.

---

## 🧠 Agent 1: Gunny Bag Counting (YOLOv8 + Tracker + Streamlit)

### 🔧 Features:
- Detects only bags inside a defined **ROI** (conveyor region)
- Tracks unique bags using centroid tracking
- Calculates volume estimates
- Logs data to `count_data.csv`
- Real-time dashboard with count-over-time graph

### ▶️ How to Run:

```bash
cd agents/gunny_bag_agent_v3
source venv/bin/activate
python main.py                 # Runs the detector
streamlit run dashboard.py     # Opens real-time dashboard
🧠 Agent 2: Number Plate Detection & OCR
🔧 Features:
Detects plates using YOLO

Crops and OCRs text using EasyOCR

Logs detected plate numbers with bounding boxes

▶️ How to Run:
bash
Copy
Edit
cd agents/number_plate_agent
source venv/bin/activate
streamlit run app.py
Upload .mp4 video — see detected plates with timestamps and text recognition.

🧠 Agent 3: Face Detection and Logging
🔧 Features:
Detects and recognizes known faces from known_faces/

Logs every detection event to CSV

Can differentiate between "Verified" and "Intrusion"

▶️ How to Run:
bash
Copy
Edit
cd agents/face_agent
source venv/bin/activate
python face_logger.py    # Live webcam monitoring
python recognizer.py     # For identification
🧠 Agent 4: Anomaly Agent (LangChain + SQLite + Streamlit Chatbot)
🔧 Features:
Seeds a synthetic warehouse surveillance database

LLM (GPT-3.5) based chatbot answers SQL queries using natural language

Detects:

Intrusions (face logs)

Unauthorized vehicles

Bag activity history

Built using LangChain's SQL agent + OpenAI API

▶️ How to Run:
bash
Copy
Edit
cd agents/anomaly_agent_friend
source venv/bin/activate
python db.py                  # (First time only) Seeds database
python video_processor.py videos/sample.mp4    # Detect bags, faces, plates
streamlit run streamlit_app.py
Ask questions like:

"Show unauthorized vehicles yesterday"

"How many bags were moved on 2025-05-09?"

📦 Requirements
Each agent folder includes a requirements.txt. You can install them with:

bash
Copy
Edit
pip install -r requirements.txt
Make sure to use the correct Python version (recommended: 3.10 or 3.11)

💡 Tech Stack
Area	Tool/Framework
Object Detection	YOLOv8 (Ultralytics)
OCR	EasyOCR
Face Recognition	dlib, face_recognition
LLM Interface	LangChain + GPT-3.5 Turbo
Backend	SQLite, SQLAlchemy
Dashboard	Streamlit
Tracker	Centroid Tracker (custom)

🧪 Demo Use Cases
📦 Bag movement analysis

🧑‍💼 Detect unauthorized person entry

🚘 Vehicle access audit

🧠 Natural language CCTV log queries

🛠️ Maintenance Tips
Regularly clean large .mp4 video logs

Monitor count_data.csv for size growth

Use OpenAI key in .env for LLM-based agent
