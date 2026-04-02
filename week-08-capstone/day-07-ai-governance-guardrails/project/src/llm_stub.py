"""Stub LLM adapter — swap for real provider HTTP client in production."""

from __future__ import annotations

import hashlib
import time
from typing import Any, Dict, List


def generate(messages: List[Dict[str, Any]], tenant_id: str) -> Dict[str, Any]:
    """
    Deterministic fake response for demos and tests.
    Replace with: OpenAI / Anthropic / Bedrock / Azure OpenAI client.
    """
    last_user = ""
    for m in reversed(messages):
        if m.get("role") == "user":
            last_user = str(m.get("content", ""))
            break

    digest = hashlib.sha256(last_user.encode()).hexdigest()[:12]
    latency_ms = 5.0

    text = (
        f"[stub-llm] Processed request for tenant={tenant_id}. "
        f"Echo digest={digest}. "
        "Replace llm_stub.generate with your provider SDK."
    )
    return {
        "content": text,
        "model": "stub-v1",
        "latency_ms": latency_ms,
        "usage": {"prompt_tokens": len(last_user) // 4, "completion_tokens": len(text) // 4},
    }
