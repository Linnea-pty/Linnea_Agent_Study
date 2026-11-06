from typing import Callable
from langchain.agents.middleware import ModelRequest, ModelResponse, wrap_model_call
from langgraph.config import get_config
from shared.llm import MODEL_POOL

@wrap_model_call
def inject_model_by_tier(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
    try:
        cfg = get_config() or {}
    except Exception:
        cfg = {}
    tier = cfg.get("configurable", {}).get("tier")
    if tier is None:
        return handler(request)
    model = MODEL_POOL.get(tier)
    if model is None:
        return handler(request)
    return handler(request.override(model=model))