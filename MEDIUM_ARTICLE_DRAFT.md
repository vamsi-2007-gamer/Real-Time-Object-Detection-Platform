# Building a Real-Time Object Detection Platform with Python, YOLO, OpenCV, and MySQL

*Replace bracketed sections with your real results and screenshots before publishing.*

## Introduction
For this project, I built VisionTrack, a modular object-detection dashboard designed to connect computer vision with event logging and a usable interface. The goal was to detect objects in images and videos, display the results, and save structured detection events for later review.

## Technology stack
- **Python** for application logic
- **Ultralytics YOLO** for object detection
- **OpenCV** for image/video processing
- **Streamlit** for the modular web interface
- **MySQL** for persistent event records

## How it works
The user uploads an image or video. The detector runs YOLO inference and returns object labels, confidence scores, and bounding-box coordinates. The interface displays an annotated result, while the database module stores each detection with a timestamp and source type. The dashboard and event-history page read these records back from MySQL.

## Architecture
The code is separated into UI pages, a detector service, a database layer, and environment-based configuration. This separation makes it easier to change the model or database without rewriting the interface.

## Challenges and lessons learned
1. **Model setup:** pretrained weights may need to download on the first run.
2. **Database configuration:** credentials belong in an environment file, not in source control.
3. **Video processing:** long videos take time, so progress feedback and batched database writes improve usability.
4. **Modular design:** separating detection, persistence, and UI logic makes debugging easier.

## Results
[Insert your actual test results here: sample images/videos tested, object classes detected, number of events saved, and any performance observations. Do not claim results you did not measure.]

## Demo
[Insert your GitHub repository URL and a link to your demonstration video.]

## What I would improve next
- Add a continuous webcam stream with a start/stop control
- Add per-class charts and time-range filters
- Add object tracking and alert rules
- Add automated tests and deployment configuration

## Conclusion
This project helped me connect a pretrained computer-vision model to a practical user interface and a relational database. The most important lesson was that a working AI application needs more than inference: configuration, error handling, data persistence, and clear documentation are also part of the engineering work.

---
**Before publishing:** add your own screenshots, link your actual repository/demo, and revise the learning section to reflect what you personally encountered.
