"""i18n — English and Hindi message lookup.

Usage:
    from shared.i18n import t
    msg = t("auth.otp_sent", lang="hi", mobile="9876543210")
"""
from __future__ import annotations
import json
from functools import lru_cache
from pathlib import Path

_BASE = Path(__file__).parent


@lru_cache
def _load(lang: str) -> dict:
    path = _BASE / lang / "messages.json"
    if not path.exists():
        path = _BASE / "en" / "messages.json"
    return json.loads(path.read_text(encoding="utf-8"))


def t(key: str, lang: str = "en", **kwargs) -> str:
    """Translate a dotted key with optional format vars.

    Example: t("auth.otp_sent", lang="hi", mobile="9876543210")
    """
    messages = _load(lang)
    parts = key.split(".")
    value = messages
    for part in parts:
        value = value.get(part, key) if isinstance(value, dict) else key
    if isinstance(value, str) and kwargs:
        try:
            return value.format(**kwargs)
        except KeyError:
            return value
    return value if isinstance(value, str) else key
