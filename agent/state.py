from typing import TypedDict, List, Dict

class AgentState(TypedDict):
    question: str
    context: str
    messages: List[Dict]
    answer: str