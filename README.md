<<<<<<< HEAD
# VisionTrack — Real-Time Object Detection Platform

A modular object-detection dashboard built with Python, OpenCV, Ultralytics YOLO, Streamlit, and MySQL.

## Features
- YOLO-powered object detection on uploaded images and videos
- Annotated output with bounding boxes, class labels, and confidence
- MySQL event logging with timestamp, source, class, confidence, and bounding-box coordinates
- Dashboard summary, event history, class filtering, and CSV export
- Configurable confidence threshold and model selection

- Continuous browser webcam detection using `streamlit-webrtc` (camera permission required)

## Requirements
- Python 3.10–3.12 recommended
- MySQL Server running locally or reachable over the network
- Internet access on first launch to download YOLO weights

## Windows setup (PowerShell)
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and set your MySQL password. Do not upload `.env` to GitHub.

Create the database/table using MySQL Workbench and `schema.sql`, or let the app create them when the configured MySQL account has database-creation permission.

Run:
```powershell
streamlit run app.py
```
The terminal prints a local URL, usually `http://localhost:8501`.

## MySQL
The app uses parameterized SQL for event inserts and filters. The configured account needs permission to create the database/table on first run, or you can create them manually with `schema.sql` and use a restricted account.

## Troubleshooting
- **MySQL disconnected:** verify the MySQL service is running, port is usually `3306`, and `.env` credentials are correct.
- **YOLO download error:** check internet access and retry.
- **Slow inference:** choose the nano model, use shorter videos, or reduce input resolution.
- **PowerShell blocks activation:** run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate the environment again.

## Repository checklist
- Keep `.env`, private media, and downloaded model weights out of Git.
- Add screenshots and a short demo video only if they contain no private information.
- Verify the README commands on a clean environment before describing the app as fully tested.

## License
Choose a license appropriate for your intended use. Review Ultralytics licensing terms before distributing a product built on its software.
=======
# Real-Time-Object-Detection-Platform
>>>>>>> cb41ef79f67e8a9dbc49dc4bc52c709de35a87b5
