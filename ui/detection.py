import time
import cv2
import pandas as pd
import streamlit as st
from PIL import Image
import numpy as np

def render_detection(detector, database, confidence):
    st.subheader("Detect objects")
    tab_image, tab_video = st.tabs(["Image detection", "Video detection"])
    with tab_image:
        uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "bmp", "webp"], key="image_upload")
        if uploaded:
            image = Image.open(uploaded).convert("RGB")
            rgb = np.array(image)
            bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
            if st.button("Run detection", type="primary", key="run_image"):
                with st.spinner("Running YOLO inference..."):
                    annotated, detections = detector.detect(bgr, confidence)
                left, right = st.columns(2)
                left.image(rgb, caption="Original image", use_container_width=True)
                right.image(annotated, caption="Detected objects", use_container_width=True)
                st.success(f"Found {len(detections)} object(s).")
                if detections:
                    df = pd.DataFrame(detections)
                    df["confidence"] = (df["confidence"] * 100).round(1).astype(str) + "%"
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    if database:
                        saved = database.log_detections(detections, "image")
                        st.caption(f"Saved {saved} event row(s) to MySQL." if saved else "MySQL logging unavailable; results are shown but not persisted.")
                else:
                    st.info("No objects passed the selected confidence threshold.")
                st.download_button("Download annotated image", data=Image.fromarray(annotated).convert("RGB").tobytes(),
                                   file_name="annotated_image.rgb", mime="application/octet-stream",
                                   help="Raw RGB pixel bytes. For a standard PNG, use the Save annotated PNG button below.")
                import io
                buf = io.BytesIO()
                Image.fromarray(annotated).save(buf, format="PNG")
                st.download_button("Save annotated PNG", data=buf.getvalue(), file_name="annotated_image.png", mime="image/png")
    with tab_video:
        video = st.file_uploader("Upload a short video", type=["mp4", "avi", "mov", "mkv"], key="video_upload")
        if video:
            st.caption("The app processes every frame and logs detected objects. Long videos may take time.")
            if st.button("Process video", type="primary"):
                temp_path = "uploaded_video_temp.mp4"
                with open(temp_path, "wb") as f:
                    f.write(video.getbuffer())
                cap = cv2.VideoCapture(temp_path)
                if not cap.isOpened():
                    st.error("Could not open this video. Try an MP4 file.")
                else:
                    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
                    fps = cap.get(cv2.CAP_PROP_FPS) or 25
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    output_path = "annotated_video.mp4"
                    writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
                    progress = st.progress(0)
                    status = st.empty()
                    event_buffer = []
                    frame_idx = 0
                    preview = st.empty()
                    while True:
                        ok, frame = cap.read()
                        if not ok:
                            break
                        annotated, detections = detector.detect(frame, confidence)
                        writer.write(cv2.cvtColor(annotated, cv2.COLOR_RGB2BGR))
                        event_buffer.extend(detections)
                        frame_idx += 1
                        if frame_idx % 10 == 0 or frame_idx == total:
                            progress.progress(min(frame_idx / total, 1.0))
                            status.write(f"Processed {frame_idx} / {total} frames")
                            preview.image(annotated, caption="Latest processed frame", use_container_width=True)
                        # Insert in batches to avoid a database round-trip for every frame.
                        if len(event_buffer) >= 100 and database:
                            database.log_detections(event_buffer, "video")
                            event_buffer = []
                    cap.release()
                    writer.release()
                    if event_buffer and database:
                        database.log_detections(event_buffer, "video")
                    status.success(f"Finished processing {frame_idx} frames.")
                    with open(output_path, "rb") as f:
                        st.download_button("Download annotated video", data=f.read(), file_name="annotated_video.mp4", mime="video/mp4")
