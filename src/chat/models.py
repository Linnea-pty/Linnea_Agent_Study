from enum import Enum
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

CODING_KEYWORDS = ("代码", "函数", "写个", "实现", "bug", "调试", "python", "sql")
REASONING_KEYWORDS = ("分析", "推理", "比较", "权衡", "为什么", "设计")

ROLE_MAP: list[tuple[type, str]] = [
    (HumanMessage,  "user"),
    (SystemMessage, "system"),
    (ToolMessage,   "tool"),
    (AIMessage,     "assistant"),
]
PERSIST_ROLES = frozenset({"user", "assistant"})
ROLE_TO_CLS: dict[str, type] = {"user": HumanMessage, "assistant": AIMessage}

def role_of(msg) -> str | None:
    for cls, role in ROLE_MAP:
        if isinstance(msg, cls):
            return role
    return None

class Tier(str, Enum):
    FAST = "fast"
    BALANCED = "balanced"
