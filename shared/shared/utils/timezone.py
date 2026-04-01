"""IST timezone helpers.

Rule: Store all datetimes in UTC in the DB. Display in IST.
Never store naive datetimes.
"""
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")
UTC = timezone.utc


def now_ist() -> datetime:
    """Current datetime in IST (tz-aware)."""
    return datetime.now(IST)


def now_utc() -> datetime:
    """Current datetime in UTC — use this for DB writes."""
    return datetime.now(UTC)


def to_ist(dt: datetime) -> datetime:
    """Convert any tz-aware datetime to IST."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt.astimezone(IST)


def to_utc(dt: datetime) -> datetime:
    """Convert any tz-aware datetime to UTC."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=IST)
    return dt.astimezone(UTC)


def format_ist(dt: datetime, fmt: str = "%d %b %Y %I:%M %p") -> str:
    """Format for user-facing display (e.g. '15 Aug 2025 10:30 AM')."""
    return to_ist(dt).strftime(fmt)


def ist_day_bounds(date=None) -> tuple[datetime, datetime]:
    """Return (start_utc, end_utc) for a date in IST. Defaults to today."""
    d = date or now_ist().date()
    start = datetime(d.year, d.month, d.day, tzinfo=IST)
    end = datetime(d.year, d.month, d.day, 23, 59, 59, 999999, tzinfo=IST)
    return to_utc(start), to_utc(end)
