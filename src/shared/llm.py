import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

def _deepseek() -> ChatOpenAI:
    return ChatOpenAI(
        model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
        base_url="https://api.deepseek.com",
        api_key=os.getenv("DEEP_SEEKER_API_KEY"),
        temperature=0,
    )

def _qwen() -> ChatOpenAI:
    return ChatOpenAI(
        model=os.getenv("QWEN_MODEL", "qwen-flash"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        api_key=os.getenv("QWEN_API_KEY"),
        temperature=0,
    )

MODEL_POOL: dict[str, ChatOpenAI] = {
    "balanced": _deepseek(),
    "fast":     _qwen(),
}