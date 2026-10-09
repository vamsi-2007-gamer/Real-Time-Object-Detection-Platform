import time
import threading
import av
import cv2
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode

class LiveDetectionProcessor(VideoProcessorBase):
    def __init__(self, detector, database, confidence):
        self.detector = detector
        self.database = database
        self.confidence = confidence
        self.lock = threading.Lock()
        self.last_logged = {}
        self.last_error = None

    def recv(self, frame):
        image_bgr = frame.to_ndarray(format="bgr24")
        try:
            annotated_rgb, detections = self.detector.detect(image_bgr, self.confidence)
            # Throttle logging per class to avoid inserting a row for every frame.
            now = time.time()
            if self.database:
                selected = []
                for detection in detections:
                    label = detection["label"]
                    if now - self.last_logged.get(label, 0) >= 3.0:
                        selected.append(detection)
                        self.last_logged[label] = now
                if selected:
                    self.database.log_detections(selected, "webcam")
            annotated_bgr = cv2.cvtColor(annotated_rgb, cv2.COLOR_RGB2BGR)
            return av.VideoFrame.from_ndarray(annotated_bgr, format="bgr24")
        except Exception as exc:
            self.last_error = str(exc)
            return frame

def render_live_camera(detector, database, confidence):
    st.subheader("Live webcam detection")
    st.write("Allow camera access in your browser, then press **START** in the video panel. Press **STOP** to end the stream.")
    st.caption("For privacy, the app does not save webcam video. Detection events are logged to MySQL when the database is connected.")
    ctx = webrtc_streamer(
        key="visiontrack-live-webcam",
        mode=WebRtcMode.SENDRECV,
        video_processor_factory=lambda: LiveDetectionProcessor(detector, database, confidence),
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )
    if not ctx.state.playing:
        st.info("The camera is currently stopped. Browser camera permission may be required.")
    st.caption("Note: webcam access is browser/device dependent. On a remote deployment, HTTPS and appropriate network configuration are generally required.")
