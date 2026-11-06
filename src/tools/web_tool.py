import json
from langchain.tools import tool
from shared.browser import get_browser

@tool
def read_webpage(url: str) -> str:
    """读取网页内容，返回 ARIA 快照。适合 SPA 和动态渲染页面。"""
    browser = get_browser()
    context = browser.new_context()
    page = context.new_page()
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=20000)
        try:
            page.wait_for_load_state("networkidle", timeout=10000)
        except Exception:
            pass
        snapshot = page.locator("body").aria_snapshot()
        return json.dumps(snapshot, ensure_ascii=False)[:8000]
    except Exception as e:
        return f"网页读取失败：{e}"
    finally:
        context.close()