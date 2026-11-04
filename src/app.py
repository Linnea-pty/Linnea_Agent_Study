import gradio as gr
from main import run_turn


def chat(message, history):
    if not message.strip():
        return history, ""
    reply, tier = run_turn(message, session_id="web")
    history.append({"role":"user","content":message})
    history.append({"role": "assistant", "content": reply})
    return history, f"本轮路由：**{tier}**"


with gr.Blocks(title="多模型Agent") as demo:
    gr.Markdown("# Linnea的多模型个人 Agent\nAgent 只构建一次，路由在中间件内部动态生效。")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="输入你的问题...", label="消息")
    tier_md = gr.Markdown()
    clear = gr.Button("清空会话")

    msg.submit(chat, [msg, chatbot], [chatbot, tier_md])
    msg.submit(lambda: "", None, msg)
    # 清空时返回空列表 []，而不是 None
    clear.click(lambda: ([], None, ""), None, [chatbot, msg, tier_md])

demo.launch()