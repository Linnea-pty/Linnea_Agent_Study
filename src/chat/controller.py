from chat.service import ChatService

_service = ChatService()

def handle_chat(message: str, history: list, session_id: str = "web"):
    if not message.strip():
        return history, ""
    reply, tier = _service.run_turn(message, session_id)
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": reply})
    return history, f"本轮路由：**{tier}**"

def handle_cli(task: str) -> None:
    reply, tier = _service.run_turn(task, session_id="cli")
    print(f"\n[路由档位: {tier}]\n{reply}")