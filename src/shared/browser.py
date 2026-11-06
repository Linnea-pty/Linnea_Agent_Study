import atexit
import threading
from playwright.sync_api import sync_playwright

_local = threading.local()
_registry: list[tuple] = []
_lock = threading.Lock()

def get_browser():
    b = getattr(_local, "browser", None)
    if b is not None and b.is_connected():
        return b
    pw = sync_playwright().start()
    b = pw.chromium.launch(headless=True)
    _local.pw, _local.browser = pw, b
    with _lock:
        _registry.append((pw, b))
    return b

@atexit.register
def shutdown_browsers() -> None:
    with _lock:
        for pw, b in _registry:
            try:
                b.close()
            finally:
                pw.stop()
        _registry.clear()