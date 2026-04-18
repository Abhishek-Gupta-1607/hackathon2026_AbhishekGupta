# Architecture Diagram

```mermaid
sequenceDiagram
    participant BatchSystem as async main()
    participant AgentNode as LangGraph Agent Node
    participant LLM as Gemini Model
    participant Tools as Mock Internal APIs (tools.py)

    Note over BatchSystem: Load Tickets & Process
    BatchSystem->>AgentNode: Invoke Graph (Ticket: "I want refund...")
    
    AgentNode->>LLM: Pass State + System Prompt
    LLM-->>AgentNode: Decide to call tool (e.g., {"action": "refund_flow", "confidence": 0.9})
        
    alt Tool Decision execution
      AgentNode->>Tools: Execute: safe_tool_call(get_order("123"))
      
      alt Tool Failure (Simulated)
          Tools--xAgentNode: ConnectionError!
          AgentNode--xBatchSystem: Graph fails execution.
          BatchSystem->>BatchSystem: Logs to Dead Letter Queue (failed_tickets.json)
      else Tool Success
          Tools-->>AgentNode: Return ToolMessage (Order Status)
          AgentNode->>Tools: Execute: safe_tool_call(issue_refund("123", 50.0))
      end
    end
    
    AgentNode-->>BatchSystem: Final State (Messages)
    BatchSystem->>BatchSystem: Write to audit_log.json
```

## Abstract View
                ┌──────────────┐
                │   Tickets    │
                └──────┬───────┘
                       ↓
              ┌─────────────────┐
              │  LLM Decision   │
              └──────┬──────────┘
                     ↓
        ┌────────────┼────────────┐
        ↓            ↓            ↓
   Refund Flow   Order Tracking   KB Search
        ↓            ↓            ↓
              ┌─────────────────┐
              │   Observation   │
              └──────┬──────────┘
                     ↓
        ┌────────────┼────────────┐
        ↓                         ↓
     Resolve                 Escalate
        ↓                         ↓
              ┌─────────────────┐
              │   Send Reply    │
              └─────────────────┘
