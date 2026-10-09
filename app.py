import streamlit as st
from config import settings
from database.db import Database
from services.detector import ObjectDetector
from ui.dashboard import render_dashboard
from ui.detection import render_detection
from ui.live_camera import render_live_camera
from ui.event_history import render_event_history
from ui.about import render_about

st.set_page_config(page_title="VisionTrack | Object Detection", page_icon="👁️", layout="wide")

@st.cache_resource
def get_detector(model_name: str):
    return ObjectDetector(model_name)

@st.cache_resource
def get_database():
    db = Database(settings)
    db.initialize()
    return db

st.markdown("""
<style>
.block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
[data-testid="stSidebar"] {border-right: 1px solid rgba(128,128,128,.2);}
.hero {padding: 1.2rem 1.4rem; border-radius: 16px; background: linear-gradient(120deg,#14213d,#234e70); color: white; margin-bottom: 1rem;}
.hero h1 {margin:0; font-size:2rem;} .hero p {margin:.35rem 0 0 0; opacity:.88;}
</style>
<div class="hero"><h1>👁️ VisionTrack</h1><p>Real-time object detection, event logging, and visual analytics</p></div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Configuration")
    model_name = st.selectbox("YOLO model", ["yolo11n.pt", "yolo26n.pt"], index=0,
                              help="The model weights download on first use if not already cached.")
    confidence = st.slider("Confidence threshold", 0.10, 0.95, 0.35, 0.05)
    st.caption("Tip: a lower threshold detects more objects but may add false positives.")
    st.divider()
    page = st.radio("Workspace", ["Dashboard", "Live webcam", "Detect objects", "Event history", "About & setup"])

try:
    detector = get_detector(model_name)
except Exception as exc:
    st.error(f"Could not load YOLO model: {exc}")
    st.info("Check your internet connection for the first model download, then run: pip install -r requirements.txt")
    st.stop()

try:
    database = get_database()
    db_status = database.available
except Exception as exc:
    database = None
    db_status = False
    st.sidebar.warning(f"MySQL unavailable: {exc}")

if page == "Dashboard":
    render_dashboard(database, db_status)
elif page == "Live webcam":
    render_live_camera(detector, database, confidence)
elif page == "Detect objects":
    render_detection(detector, database, confidence)
elif page == "Event history":
    render_event_history(database, db_status)
else:
    render_about(db_status)
