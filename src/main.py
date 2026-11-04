import json
from pathlib import Path
from langchain_core.messages import HumanMessage, AIMessage

from agent import agent
from router import route_task

HISTORY_DIR = Path("../histories")
HISTORY_DIR.mkdir(exist_ok=True)

def load_history(session_id: str) -> list:
    f = HISTORY_DIR / f"{session_id}.json"
    if not f.exists():
        return []

    # 容错处理：读取并检查内容是否为空
    content = f.read_text(encoding="utf-8").strip()
    if not content:
        return []

    try:
        raw = json.loads(content)
    except json.JSONDecodeError:
        print(f"[警告] 历史文件 {f.name} 格式损坏，已自动重置为空历史。")
        return []

    result = []
    for m in raw:
        cls = HumanMessage if m["role"] == "user" else AIMessage
        result.append(cls(content=m["content"]))
    return result

def load_history(session_id: str) -> list:
    f = HISTORY_DIR / f"{session_id}.json"
    if not f.exists():
        return []
    raw = json.loads(f.read_text(encoding="utf-8"))
    result = []
    for m in raw:
        cls = HumanMessage if m["role"] == "user" else AIMessage
        result.append(cls(content=m["content"]))
    return result


def save_history(session_id: str, messages: list):
    serializable = [
        {"role": "user" if isinstance(m, HumanMessage) else "assistant",
         "content": m.content}
        for m in messages
    ]
    (HISTORY_DIR / f"{session_id}.json").write_text(
        json.dumps(serializable, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def run_turn(task: str, session_id: str = "default"):
    messages = load_history(session_id)
    messages.append(HumanMessage(content=task))

    # agent.invoke 每次传入完整历史，Agent 内部状态图保持连续
    result = agent.invoke({"messages": messages})
    reply = result["messages"][-1].content

    messages.append(AIMessage(content=reply))
    save_history(session_id, messages)

    tier = route_task(task)  # 仅用于显示，实际路由已在中间件内完成
    return reply, tier


if __name__ == "__main__":
    print("多模型个人 Agent（输入 exit//quit 退出）")
    while True:
        task = input("\n> ").strip()
        if task.lower() in ("exit", "quit"):
            break
        reply, tier = run_turn(task, session_id="cli")
        print(f"\n[路由档位: {tier}]\n{reply}")