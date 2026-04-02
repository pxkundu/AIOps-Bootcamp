"""Load and resolve tenant policies from YAML."""

from __future__ import annotations

import os
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict

import yaml


def _config_path() -> Path:
    base = Path(__file__).resolve().parent.parent
    return base / "config" / "policies.yaml"


def load_policies(path: Path | None = None) -> Dict[str, Any]:
    path = path or _config_path()
    if not path.exists():
        raise FileNotFoundError(f"Policy file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def resolve_tenant_policy(
    policies: Dict[str, Any],
    tenant_id: str | None,
) -> Dict[str, Any]:
    """Merge defaults with tenant-specific overrides."""
    defaults = deepcopy(policies.get("defaults") or {})
    tenants = policies.get("tenants") or {}
    tid = tenant_id or "default"
    tenant_cfg = deepcopy(tenants.get(tid) or tenants.get("default") or {})
    merged = {**defaults, **tenant_cfg}
    merged["_tenant_id"] = tid
    merged["_risk_tier"] = tenant_cfg.get("risk_tier", "T1")
    return merged


def get_risk_tier_description(policies: Dict[str, Any], tier: str) -> str:
    tiers = policies.get("risk_tiers") or {}
    return str((tiers.get(tier) or {}).get("description", tier))
