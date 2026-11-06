import json
import os
from pathlib import Path
from chat.models import PERSIST_ROLES, ROLE_TO_CLS, role_of

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_DEFAULT_BASE = _PROJECT_ROOT / "histories"

class HistoryRepository:
    def __init__(self, base_dir: str | Path | None = None):
        self.base = Path(base_dir) if base_dir else _DEFAULT_BASE
        self.base.mkdir(parents=True, exist_ok=True)

    def _path(self, session_id: str) -> Path:
        return self.base / f"{session_id}.json"

    def load(self, session_id: str) -> list:
        f = self._path(session_id)
        if not f.exists():
            return []
        content = f.read_text(encoding="utf-8").strip()
        if not content:
            return []
        try:
            raw = json.loads(content)
        except json.JSONDecodeError:
            print(f"[警告] 历史文件 {f.name} 损坏，已重置为空历史")
            return []
        result = []
        for m in raw:
            cls = ROLE_TO_CLS.get(m.get("role"))
            if cls is None:
                continue
            result.append(cls(content=m.get("content", "")))
        return result

    def save(self, session_id: str, messages: list) -> None:
        serializable = []
        for m in messages:
            role = role_of(m)
            if role not in PERSIST_ROLES:
                if role is None:
                    print(f"[警告] 未知消息类型 {type(m).__name__}，已跳过")
                continue
            serializable.append({"role": role, "content": m.content})

        path = self._path(session_id)
        tmp = path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(serializable, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(tmp, path)