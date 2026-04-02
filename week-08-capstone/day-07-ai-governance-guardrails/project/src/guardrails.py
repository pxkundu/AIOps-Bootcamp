"""Input/output guardrails: injection patterns, deny topics, optional PII."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class Violation:
    code: str
    message: str
    detail: Optional[str] = None


def _concat_messages(messages: List[Dict[str, Any]]) -> str:
    parts = []
    for m in messages:
        role = m.get("role", "unknown")
        content = m.get("content", "")
        parts.append(f"[{role}] {content}")
    return "\n".join(parts)


def check_injection_patterns(text: str, patterns: List[str]) -> Optional[Violation]:
    for p in patterns:
        try:
            if re.search(p, text):
                return Violation(
                    code="PROMPT_INJECTION_SUSPECTED",
                    message="Input matched a blocked injection pattern.",
                    detail=p,
                )
        except re.error:
            continue
    return None


def check_deny_topics(text: str, topics: List[str]) -> Optional[Violation]:
    lower = text.lower()
    for topic in topics:
        if topic.lower() in lower:
            return Violation(
                code="TOPIC_DENIED",
                message="Input references a policy-denied topic.",
                detail=topic,
            )
    return None


def check_length(text: str, max_chars: int) -> Optional[Violation]:
    if len(text) > max_chars:
        return Violation(
            code="PROMPT_TOO_LONG",
            message=f"Prompt exceeds max length ({max_chars} chars).",
            detail=str(len(text)),
        )
    return None


def redact_pii(text: str) -> str:
    """Naive demo redaction — replace with enterprise DLP in production."""
    out = text
    out = re.sub(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "[EMAIL_REDACTED]",
        out,
    )
    out = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[SSN_REDACTED]", out)
    return out


def evaluate_input(
    messages: List[Dict[str, Any]],
    policy: Dict[str, Any],
) -> Tuple[bool, List[Violation]]:
    """Run all input guards. Returns (ok, violations)."""
    violations: List[Violation] = []
    full_text = _concat_messages(messages)

    mlen = policy.get("max_prompt_chars", 12000)
    v = check_length(full_text, int(mlen))
    if v:
        violations.append(v)
        return False, violations

    topics = policy.get("deny_topics") or []
    v = check_deny_topics(full_text, topics)
    if v:
        violations.append(v)
        return False, violations

    patterns = policy.get("injection_patterns") or []
    v = check_injection_patterns(full_text, patterns)
    if v:
        violations.append(v)
        return False, violations

    return True, []


def evaluate_output(
    text: str,
    policy: Dict[str, Any],
) -> Tuple[str, List[Violation]]:
    """Apply output policy (e.g. PII). Returns (possibly_redacted_text, violations)."""
    violations: List[Violation] = []
    out = text
    if policy.get("block_pii_in_output"):
        redacted = redact_pii(out)
        if redacted != out:
            violations.append(
                Violation(
                    code="PII_REDACTED",
                    message="Potential PII removed from model output.",
                )
            )
        out = redacted
    return out, violations
