# 路由判断

CODING_KEYWORDS = ["代码","函数","写个","实现","bug","调试","python","sql"]
REASONING_KEYWORDS =  ["分析", "推理","比较","权衡","为什么","设计"]

def route_task(task: str):
    text = task.lower()
    if any(word in text for word in CODING_KEYWORDS):
        return "fast"
    if any(word in text for word in REASONING_KEYWORDS):
        return "balanced"
    return "fast"