import os
from langchain_google_genai import ChatGoogleGenerativeAI

def decide_with_llm(ticket_text: str, history: list) -> str:
    """Prompt the LLM to classify the ticket and generate a JSON response."""
    
    prompt = f"""
    You are an AI agent.

    Conversation History:
    {history}

    Current Ticket:
    {ticket_text}

    Decide next action exactly from:
    - refund_flow
    - track_order
    - knowledge_search
    - escalate

    You must return raw JSON only without markdown wrapping, strictly matching this schema:
    {{ "action": "...", "confidence": 0.95 }}
    """
    
    from config import GEMINI_API_KEY
    import os
    os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest", 
        temperature=0.0,
        google_api_key=GEMINI_API_KEY
    )
    
    response = llm.invoke(prompt)
    return response.content
