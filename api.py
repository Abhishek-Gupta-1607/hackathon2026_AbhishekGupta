from fastapi import FastAPI
from pydantic import BaseModel
import json
import os
import config # Loads the .env file!
from agent.graph import support_graph

app = FastAPI(title="Autonomous Support API")

class TicketRequest(BaseModel):
    id: str
    text: str

@app.get("/")
def read_root():
    return {"message": "Autonomous Support API is running! Please run 'streamlit run ui.py' in a separate terminal to view the User Interface."}

@app.post("/process_ticket")
def process_ticket(ticket: TicketRequest):
    # Initialize the required state format
    state = {
        "ticket_id": ticket.id,
        "ticket_text": ticket.text,
        "history": [],
        "action": None,
        "confidence": None,
        "steps": [],
        "logs": [],
        "resolved": False,
        "response": ""
    }

    try:
        # Run agent
        result = support_graph.invoke(state)
        
        # Save to logs for the dashboard
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
            
        return result
    except Exception as e:
        error_result = {
            "ticket_id": ticket.id,
            "resolved": False,
            "response": f"System Error: {str(e)}",
            "steps": ["System Failure occurred", str(e)]
        }
        return error_result
