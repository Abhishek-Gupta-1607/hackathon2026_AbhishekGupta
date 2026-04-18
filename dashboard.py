import streamlit as st
import json
import time

st.title("📊 AI Agent Dashboard")

while True:
    try:
        with open("logs/audit_log.json") as f:
            data = json.load(f)

        total = len(data)
        resolved = sum(1 for d in data if d["resolved"])
        failed = total - resolved

        st.metric("Total Tickets", total)
        st.metric("Resolved", resolved)
        st.metric("Failed", failed)

        st.write("### Recent Activity")
        for item in data[-5:]:
            st.write(item["steps"])

    except:
        st.write("Waiting for data...")

    time.sleep(3)
    st.rerun()
