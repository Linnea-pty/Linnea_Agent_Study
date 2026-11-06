import sys

def run_web():
    import gradio as gr
    from chat.controller import handle_chat

    with gr.Blocks(title="多模型Agent") as demo:
        gr.Markdown("# Linnea的多模型个人 Agent")
        chatbot = gr.Chatbot()
        msg = gr.Textbox(placeholder="输入你的问题...", label="消息")
        tier_md = gr.Markdown()
        clear = gr.Button("清空会话")

        msg.submit(handle_chat, [msg, chatbot], [chatbot, tier_md])
        msg.submit(lambda: "", None, msg)
        clear.click(lambda: ([], "", ""), None, [chatbot, msg, tier_md])

    demo.launch()

def run_cli():
    from chat.controller import handle_cli
    print("多模型个人 Agent（输入 exit/quit 退出）")
    while True:
        task = input("\n> ").strip()
        if task.lower() in ("exit", "quit"):
            break
        if not task:
            continue
        handle_cli(task)

if __name__ == "__main__":
    if "--cli" in sys.argv:
        run_cli()
    else:
        run_web()