# Failure Modes & Retries

1. **Tool Timeout**
   → Simulated via 20% random failure parameter.
   → Recovered via `safe_tool_call` wrapper (Retry 2 times).
   → If exhaust, escalates through system crash to DLQ.

2. **Invalid Tool Response or LLM JSON Failure**
   → `try..except` in `nodes.py` catching invalid JSON schemas.
   → Falls back to `escalate` flow.

3. **Low Confidence Decision**
   → Any ticket evaluated by the semantic LLM with confidence < 0.5.
   → Immediate pipeline override to human escalation queue.

4. **Concurrent/System Failure**
   → Handled centrally in `main.py`
   → Failed tickets isolated and logged to `logs/failed_tickets.json`
