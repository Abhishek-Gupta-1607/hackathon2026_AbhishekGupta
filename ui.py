import streamlit as st
import json
import os
import config # load .env
from agent.graph import support_graph

st.title("🤖 Autonomous AI Support Agent")
st.markdown("### Powered by LangGraph, Vector DB")

ticket = st.text_area("Customer Ticket Scenario:", placeholder="Enter your support query here (e.g. 'I want refund for order 123')")

if st.button("Submit Agent Workflow"):
    if ticket.strip():
        with st.spinner("Agent Reasoning (Executing Tool Loop)..."):
            try:
                # Initialize state
                state = {
                    "ticket_id": "T-UI-001",
                    "ticket_text": ticket,
                    "history": [],
                    "action": None,
                    "confidence": None,
                    "steps": [],
                    "logs": [],
                    "resolved": False,
                    "response": ""
                }
                
                # Directly invoke the graph instead of using the API
                result = support_graph.invoke(state)

                # Save to logs for dashboard
                os.makedirs("logs", exist_ok=True)
                audit_log_path = "logs/audit_log.json"
                audit_logs = []
                if os.path.exists(audit_log_path):
                    with open(audit_log_path, "r") as f:
                        try:
                            audit_logs = json.load(f)
                        except json.JSONDecodeError:
                            audit_logs = []
                
                audit_logs.append(result)
                with open(audit_log_path, "w") as f:
                    json.dump(audit_logs, f, indent=2)

                # Show Result
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
                    
            except Exception as e:
                st.error(f"System Error: {str(e)}")
    else:
        st.warning("Please enter a support query first.")
