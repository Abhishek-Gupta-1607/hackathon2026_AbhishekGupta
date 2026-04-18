import json
import asyncio
import os
import config # loads dotenv
from agent.graph import support_graph
from agent.state import AgentState

async def process_batch():
    # Make sure logs directory exists
    os.makedirs("logs", exist_ok=True)
    
    with open("data/tickets.json", "r") as f:
        tickets = json.load(f)

    audit_logs = []
    failed_tickets = []

    print(f"Loaded {len(tickets)} tickets. Commencing logic...\n")

    for ticket in tickets:
        state: AgentState = {
            "ticket_id": ticket["id"],
            "ticket_text": ticket["text"],
            "history": [],
            "action": None,
            "confidence": None,
            "steps": [],
            "logs": []
        }
        
        try:
            print(f"[{ticket['id']}] Processing...")
            # We run asynchronously, but since tools in snippet are Sync, 
            # we can await graph.ainvoke to retain concurrency or just use invoke
            result = support_graph.invoke(state)
            audit_logs.append(result)
            print(f"[{ticket['id']}] Success! Action Taken: {result['action']}")
            
        except Exception as e:
            # DEAD LETTER QUEUE LOGIC
            print(f"[{ticket['id']}] SYSTEM FAILURE: {str(e)}. Moved to failed queue.")
            failed_tickets.append({
                "ticket_id": ticket["id"],
                "ticket_text": ticket["text"],
                "error": str(e)
            })

    # Save outputs
    with open("logs/audit_log.json", "w") as f:
        json.dump(audit_logs, f, indent=2)

    with open("logs/failed_tickets.json", "w") as f:
        json.dump(failed_tickets, f, indent=2)
        
    print("\nRun complete. Results written to logs/")
    print(f"Successful: {len(audit_logs)} | Failed (DLQ): {len(failed_tickets)}")

if __name__ == "__main__":
    # We use asyncio run if we decide to convert to fully async later,
    # but the snippet provided by user uses invoke directly. 
    # For compatibility, we'll wrap inside an asyncio.run since we set it up.
    asyncio.run(process_batch())
