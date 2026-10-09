import streamlit as st
import pandas as pd

def render_dashboard(database, db_status):
    st.subheader("Overview")
    if not database or not db_status:
        st.warning("MySQL is not connected. Detection still works, but persistent event history is unavailable. See About & setup.")
        summary = {"events": 0, "labels": 0, "sources": 0}
    else:
        summary = database.summary()
    a, b, c = st.columns(3)
    a.metric("Logged detections", f'{summary.get("events", 0):,}')
    b.metric("Unique object classes", summary.get("labels", 0))
    c.metric("Input source types", summary.get("sources", 0))
    st.divider()
    st.markdown("#### Recent events")
    events = database.fetch_events(limit=12) if database and db_status else []
    if events:
        df = pd.DataFrame(events)
        df["confidence"] = (df["confidence"].astype(float) * 100).round(1).astype(str) + "%"
        st.dataframe(df[["id", "event_time", "source_type", "object_label", "confidence"]],
                     use_container_width=True, hide_index=True)
    else:
        st.info("No events to display yet. Open **Detect objects** and upload an image or video.")
    st.markdown("#### Workflow")
    st.write("1. Choose a YOLO model and confidence threshold in the sidebar.")
    st.write("2. Upload an image or video in Detect objects.")
    st.write("3. Review saved detection events in Event history.")
