from typing import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import ModelRequest, ModelResponse, wrap_model_call

from config import MODEL_POOL
from router import route_task
from tools import tools

SYSTEM_PROMPT = """你是Linnea的个人助理。根据任务类型选择合适的工具。
简单问答直接回答；需要计算、查时间、读文件、搜网页、读网页时调用工具。
不要编造工具返回结果之外的信息。
"""

@wrap_model_call
def  route_by_task(
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    )->ModelResponse:
    """每次模型调用前，根据最后一条用户消息动态选择模型档位。"""

    messages = request.state["messages"]
    last_user = next(
        (m.content
        for m in reversed(messages) if m.type == "human"),""
    )
    tier = route_task(last_user)
    model = MODEL_POOL[tier]
    return handler(request.override(model=model))

# Agent 只构建一次，全程复用同一个状态图
agent = create_agent(
    model = MODEL_POOL["fast"],
    tools = tools,
    system_prompt = SYSTEM_PROMPT,
    middleware = [route_by_task],
)