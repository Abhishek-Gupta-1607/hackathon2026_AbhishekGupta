🚀 Autonomous Support Resolution Agent

📌 Overview
This project implements an AI-powered autonomous support agent that resolves customer tickets using multi-step reasoning, tool usage, and intelligent escalation. It has been elevated to Production Grade using FastAPI, Streamlit, and an embedded Vector Database.

⚙️ Features
- **Frontend & Backend Decoupled**: Streamlit UI communicating to a FastAPI server.
- **Multi-step agentic reasoning**: Powered by LangGraph StateMachines.
- **Semantic Routing**: FAISS Vector DB (`sentence-transformers`) for Knowledge Base.
- **Tool chaining**: Sequence of modular Python closures executing state modifications.
- **Resiliency logic**: API timeout retries + Dead Letter Queues setup.

🧠 Architecture
The agent uses a decision loop:
Ticket → LLM JSON Decision → Semantic Router / API Action → Tool → Observe → Complete Request

▶️ How to Run
Ensure your `.env` contains `GEMINI_API_KEY=...`

1. Start Terminal 1 (Backend API):
```bash
uvicorn api:app --reload
```

2. Start Terminal 2 (Frontend UI):
```bash
streamlit run ui.py
```

📂 Output Logging System
- `logs/audit_log.json` → full reasoning trace batch dump
- `logs/failed_tickets.json` → failed dead-letter queues

⚠️ Failure Handling
- **API timeouts:** Handled via retry (`safe_tool_call` decorator pattern)
- **Low confidence:** Immediate threshold escalation to stop hallucination.
- **Invalid API Schema:** Graceful LangGraph fallback nodes.

🛠 Tech Stack
- Python (FastAPI, Streamlit)
- LangChain / LangGraph Engine 
- Gemini 1.5 Pro
- FAISS CPU Vector Search

🎯 Key Challenge Solved
Handling real-time tool failures and ensuring deterministic multi-step reasoning under production load uncertainty.

Webiste deployed link - https://autonomousaiagent.streamlit.app

website working Video - https://drive.google.com/file/d/1h6shIoh7oW3pb1rG5T6R62ln5LzCvW1G/view?usp=sharing
