import json
import re
from typing import Dict, Any

from agent.state import AgentState
from agent.llm import decide_with_llm
from tools.common import safe_tool_call
from tools.order import get_order
from tools.refund import issue_refund
from tools.vector_db import semantic_search
from tools.communication import send_reply, escalate_ticket

def decide_action(state: AgentState) -> dict:
    """Invokes LLM to select the route based on the ticket text."""
    try:
        history = state.get("history", [])
        result = decide_with_llm(state["ticket_text"], history)
        
        # Newer LangChain Gemini models can sometimes return a list of content blocks
        if isinstance(result, list):
            result = result[0].get("text", "") if isinstance(result[0], dict) else str(result[0])
        elif not isinstance(result, str):
            result = str(result)
            
        # Clean potential markdown output
        clean_json = re.sub(r"```json\s*", "", result)
        clean_json = re.sub(r"\s*```", "", clean_json)
        
        parsed = json.loads(clean_json)
        
        action = parsed.get("action", "escalate")
        confidence = parsed.get("confidence", 0.0)
        steps = [f"LLM decision: {parsed}"]
        
        # Low confidence immediately overrides to escalate
        if confidence < 0.5:
            action = "escalate"
            steps.append("Override: Confidence too low. Escalating.")
            
        return {
            "history": [state["ticket_text"]],
            "action": action,
            "confidence": confidence,
            "steps": steps
        }
    except Exception as e:
        # Invalid Tool Response fallback
        return {
            "action": "escalate",
            "confidence": 0.0,
            "steps": [f"LLM Parse Error: {str(e)} -> fallback to escalate"]
        }

def execute_route(state: AgentState) -> dict:
    """Executes the specific tool path based on the chosen action."""
    action = state["action"]
    ticket_text = state["ticket_text"]
    
    # Try to extract the first string of numbers as a mock ID
    ids = re.findall(r'\b\d{3}\b', ticket_text)
    primary_id = ids[0] if ids else "unknown"
    
    steps_out = []
    logs_out = []
    
    try:
        if action == "refund_flow":
            # Chained calls for refund reasoning
            steps_out.append(f"Calling get_order({primary_id})")
            o_resp = safe_tool_call(get_order, primary_id, retries=2)
            logs_out.append(f"Order: {o_resp}")
            
            steps_out.append(f"Calling issue_refund({primary_id})")
            r_resp = safe_tool_call(issue_refund, primary_id, retries=2)
            logs_out.append(f"Refund: {r_resp}")
            
            final_resp = safe_tool_call(send_reply, "Your refund is processed.", retries=2)
            return {"steps": steps_out, "logs": logs_out, "response": final_resp, "resolved": True}
            
        elif action == "track_order":
            steps_out.append(f"Calling get_order({primary_id})")
            o_resp = safe_tool_call(get_order, primary_id, retries=2)
            logs_out.append(f"Order: {o_resp}")
            final_resp = safe_tool_call(send_reply, f"Here is your tracking status: {o_resp}", retries=2)
            return {"steps": steps_out, "logs": logs_out, "response": final_resp, "resolved": True}
            
        elif action == "knowledge_search":
            steps_out.append(f"Calling semantic_search('{ticket_text}')")
            k_resp = safe_tool_call(semantic_search, ticket_text, retries=2)
            logs_out.append(f"Knowledge: {k_resp}")
            final_resp = safe_tool_call(send_reply, f"Based on our policy: {k_resp}", retries=2)
            return {"steps": steps_out, "logs": logs_out, "response": final_resp, "resolved": True}
            
        elif action == "escalate":
            steps_out.append("Calling escalate()")
            e_resp = safe_tool_call(escalate_ticket, "confidence low or explicitly escalated", retries=2)
            logs_out.append(f"Escalation: {e_resp}")
            return {"steps": steps_out, "logs": logs_out, "response": e_resp, "resolved": False}
        
        else:
            steps_out.append(f"Unknown action {action}, escalating.")
            e_resp = safe_tool_call(escalate_ticket, "unknown action", retries=2)
            return {"steps": steps_out, "response": e_resp, "resolved": False}

    except Exception as e:
        # If max retries failed, raise to Dead Letter Queue loop
        steps_out.append(f"System Error: {str(e)}")
        # By LangGraph rule, an exception during node execution should ideally be handled at execution time,
        # but since main.py wraps it in try-except, it acts as a DLQ there.
        raise e
