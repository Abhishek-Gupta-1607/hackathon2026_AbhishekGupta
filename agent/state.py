from typing import TypedDict, List, Optional, Annotated
import operator

class AgentState(TypedDict):
    ticket_id: str
    ticket_text: str
    history: Annotated[list, operator.add]
    action: Optional[str]
    confidence: Optional[float]
    steps: Annotated[List[str], operator.add]
    logs: Annotated[List[str], operator.add]
    resolved: bool
    response: str
