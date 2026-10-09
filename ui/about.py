import streamlit as st

def render_about(db_status):
    st.subheader("About & setup")
    st.markdown("""
**VisionTrack** is a modular computer-vision demo built with Python, Streamlit, OpenCV, Ultralytics YOLO, and MySQL.

**Modules**
- `services/detector.py` — model loading and inference.
- `database/db.py` — schema creation, event inserts, and history queries.
- `ui/` — separate dashboard, detection, and history views.
- `config.py` — environment-based configuration.

**Database status:** """ + ("Connected" if db_status else "Not connected") + """

**Privacy note:** uploaded media is processed by this app. Use only images/videos you have permission to process. Avoid committing private media, database passwords, or personal information to GitHub.

**Troubleshooting**
- First run needs internet access to download the YOLO weights.
- If MySQL is unavailable, check that the MySQL service is running and `.env` credentials match your local setup.
- If the webcam is busy, close apps that may already be using it. The current UI supports image and video uploads; webcam streaming can be added as a separate module.
""")
