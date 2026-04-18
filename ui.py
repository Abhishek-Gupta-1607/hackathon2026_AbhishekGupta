import streamlit as st
import requests

st.title("🤖 Autonomous AI Support Agent")
st.markdown("### Powered by LangGraph, Vector DB & FastAPI")

ticket = st.text_area("Customer Ticket Scenario:", placeholder="Enter your support query here (e.g. 'I want refund for order 123')")

if st.button("Submit Agent Workflow"):
    if ticket.strip():
        with st.spinner("Agent Reasoning (Executing Tool Loop)..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/process_ticket",
                    json={"id": "T-UI-001", "text": ticket}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if result.get("resolved", False):
                        st.success("✅ Ticket Resolved Autonomous Path")
                    else:
                        st.warning("⚠️ Escalated Path")

                    st.write("### 📬 Generated Response")
                    st.info(result.get("response", "No final response payload."))

                    st.write("### 🧠 Agent Reasoning Trace")
                    for step in result.get("steps", []):
                        st.write(f"- {step}")
                        
                    with st.expander("Show System Logs"):
                        st.json(result.get("logs", []))

                else:
                    st.error(f"Backend HTTP error: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to FastAPI backend. Ensure you run `uvicorn api:app --reload` first.")
    else:
        st.warning("Please enter a support query first.")
