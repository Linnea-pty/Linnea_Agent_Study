from langchain.tools import tool
from shared.sandbox import SandboxViolation, safe_read_text

@tool
def read_local_file(path: str) -> str:
    """读取沙箱目录内的文本文件。path 可以是相对沙箱根的路径，也可以是沙箱内的绝对路径。"""
    try:
        return safe_read_text(path)
    except SandboxViolation as e:
        return f"读取失败：{e}"
    except FileNotFoundError:
        return "读取失败：文件不存在"
    except Exception as e:
        return f"读取失败：{e}"