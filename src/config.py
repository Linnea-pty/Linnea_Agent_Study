# 模型池（ChatOpenAI 实例）
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

def _deepseek( ):
    return  ChatOpenAI(
        model="deepseek-flash",
        base_url="https://api.deepseek.com",
        api_key=os.getenv("DEEP_SEEKER_API_KEY"),
        temperature=0,
    )

def _qwen( ):
    return ChatOpenAI(
        model="qwen3.8-flash",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        api_key=os.getenv("QWEN_API_KEY"),
        temperature=0,
    )

MODEL_POOL = {
    "balanced": _deepseek(),
    "fast": _qwen(),
}
