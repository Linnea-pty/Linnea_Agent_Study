import datetime
import json

from pathlib import Path
from langchain.tools import tool
from playwright.sync_api import sync_playwright
from langchain_tavily import TavilySearch

@tool
def calculator(expression: str) -> str:
    """计算数学表达式，如：'3*(4+2)'"""

    try:
        return str(eval(expression,{"__builtins__":{}}))
    except Exception as e:
        return f"计算失败：{e}"

@tool
def current_time() -> str:
    """获取当前日期和时间。"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool
def read_local_file(path: str) -> str:
    """读取本地文本文件，path 必须是绝对路径。"""
    try:
        return Path(path).read_text(encoding="utf-8")[0:8000]
    except Exception as e:
        return f"读取失败：{e}"

@tool
def read_webpage(url: str) -> str:
    """读取网页内容，返回无障碍树快照。适合 SPA 和动态渲染页面。"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, wait_until="networkidle", timeout=20000)
            snapshot = page.accessibility.snapshot()
            return json.dumps(snapshot, ensure_ascii=False)[:8000]
        except Exception as e:
            return f"网页读取失败：{e}"
        finally:
            browser.close()

tavily = TavilySearch(max_results=2)
tools = [calculator, current_time, read_local_file, read_webpage, tavily]