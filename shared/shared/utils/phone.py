"""Indian phone number normalization utilities."""
import re

_MOBILE_RE = re.compile(r"^(?:\+91|91|0)?([6-9]\d{9})$")


def normalize_mobile(raw: str) -> str | None:
    """Return 10-digit mobile without prefix, or None if invalid.

    Accepts: +919876543210, 919876543210, 09876543210, 9876543210
    """
    cleaned = raw.strip().replace(" ", "").replace("-", "")
    match = _MOBILE_RE.match(cleaned)
    return match.group(1) if match else None


def to_e164(raw: str) -> str | None:
    """Return +91XXXXXXXXXX format or None if invalid."""
    normalized = normalize_mobile(raw)
    return f"+91{normalized}" if normalized else None


def mask_mobile(mobile: str) -> str:
    """Return XXXXXX1234 — safe for logs and display."""
    digits = normalize_mobile(mobile) or mobile
    if len(digits) >= 4:
        return f"XXXXXX{digits[-4:]}"
    return "XXXXXXXXXX"


def is_valid_mobile(raw: str) -> bool:
    return normalize_mobile(raw) is not None
