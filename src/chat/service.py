from langchain_core.messages import AIMessage, HumanMessage
from agent.builder import build_agent
from chat.repository import HistoryRepository
from chat.router import decide_tier

_agent = None

def _get_agent():
    global _agent
    if _agent is None:
        _agent = build_agent()
    return _agent

class ChatService:
    def __init__(self, repo: HistoryRepository | None = None):
        self.repo = repo or HistoryRepository()

    def run_turn(self, task: str, session_id: str) -> tuple[str, str]:
        messages = self.repo.load(session_id)
        messages.append(HumanMessage(content=task))
        tier = decide_tier(task)

        result = _get_agent().invoke(
            {"messages": messages},
            config={"configurable": {"tier": tier.value}},
        )
        reply = result["messages"][-1].content

        messages.append(AIMessage(content=reply))
        self.repo.save(session_id, messages)
        return reply, tier.value