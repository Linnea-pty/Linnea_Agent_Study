import os
from pathlib import Path

# src/shared/sandbox.py -> parent x3 到达根目录
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_DEFAULT_ROOT = _PROJECT_ROOT / "sandbox"

ALLOWED_ROOT = Path(os.getenv("AGENT_FILE_ROOT", str(_DEFAULT_ROOT))).resolve()
ALLOWED_ROOT.mkdir(parents=True, exist_ok=True)

ALLOWED_SUFFIX = frozenset({".txt", ".md", ".json", ".csv", ".log", ".py"})
MAX_BYTES = 8000

class SandboxViolation(ValueError):
    pass

def safe_read_text(path: str) -> str:
    p = Path(path).expanduser()
    if not p.is_absolute():
        p = ALLOWED_ROOT / p
    real = p.resolve(strict=True)

    if not real.is_relative_to(ALLOWED_ROOT):
        raise SandboxViolation(f"路径不在允许目录内：{path}")
    if real.suffix.lower() not in ALLOWED_SUFFIX:
        raise SandboxViolation(f"不支持的文件类型：{real.suffix}")

    return real.read_text(encoding="utf-8", errors="ignore")[:MAX_BYTES]