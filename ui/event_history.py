import pandas as pd
import streamlit as st

def render_event_history(database, db_status):
    st.subheader("Event history")
    if not database or not db_status:
        st.warning("Connect MySQL to browse persistent events. Detection itself can still run.")
        return
    events = database.fetch_events(limit=1000)
    if not events:
        st.info("No events have been logged yet.")
        return
    df = pd.DataFrame(events)
    labels = ["All"] + sorted(df["object_label"].dropna().unique().tolist())
    selected = st.selectbox("Filter by object class", labels)
    filtered = database.fetch_events(limit=1000, label=selected)
    out = pd.DataFrame(filtered)
    if not out.empty:
        out["confidence"] = (out["confidence"].astype(float) * 100).round(2)
        st.dataframe(out, use_container_width=True, hide_index=True)
        st.download_button("Export events as CSV", data=out.to_csv(index=False).encode("utf-8"),
                           file_name="detection_events.csv", mime="text/csv")
