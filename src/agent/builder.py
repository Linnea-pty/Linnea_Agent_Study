from langchain.agents import create_agent
from agent.middleware import inject_model_by_tier
from shared.llm import MODEL_POOL
from tools import ALL_TOOLS

SYSTEM_PROMPT = """你是Linnea的个人助理。根据任务类型选择合适的工具。
简单问答直接回答；需要计算、查时间、读文件、搜网页、读网页时调用工具。
不要编造工具返回结果之外的信息。
"""

def build_agent():
    return create_agent(
        model=MODEL_POOL["balanced"],
        tools=ALL_TOOLS,
        system_prompt=SYSTEM_PROMPT,
        middleware=[inject_model_by_tier],
    )