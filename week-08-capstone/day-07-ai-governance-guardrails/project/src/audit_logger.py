"""Structured audit log (JSON Lines) for governance evidence."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


def _log_path() -> Path:
    base = Path(__file__).resolve().parent.parent
    return base / "data" / "audit.log"


def ensure_log_dir() -> None:
    Path(_log_path()).parent.mkdir(parents=True, exist_ok=True)


def append_event(
    event_type: str,
    tenant_id: str,
    payload: Dict[str, Any],
    *,
    audit_path: Optional[Path] = None,
) -> None:
    ensure_log_dir()
    path = audit_path or _log_path()
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "type": event_type,
        "tenant_id": tenant_id,
        **payload,
    }
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def read_recent_events(limit: int = 100, *, audit_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    path = audit_path or _log_path()
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").strip().splitlines()
    out: List[Dict[str, Any]] = []
    for line in lines[-limit:]:
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out
