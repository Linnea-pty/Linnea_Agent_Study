from langchain_tavily import TavilySearch
from tools.file_tool import read_local_file
from tools.math_tool import calculator
from tools.time_tool import current_time
from tools.web_tool import read_webpage

ALL_TOOLS = [
    calculator,
    current_time,
    read_local_file,
    read_webpage,
    TavilySearch(max_results=2),
]
__all__ = ["ALL_TOOLS"]