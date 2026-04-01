"""Academic year utilities — Indian EdTech specific.

Most Indian schools start June; coaching institutes vary.
Academic year "2025-26" = June 2025 → May 2026.
"""
from __future__ import annotations
from datetime import date


def current_academic_year(start_month: int = 6, ref: date | None = None) -> str:
    """Return academic year string e.g. '2025-26'.

    Args:
        start_month: Month when academic year begins (1-12). Default 6 = June.
        ref: Reference date (defaults to today).
    """
    d = ref or date.today()
    if d.month >= start_month:
        start_year = d.year
    else:
        start_year = d.year - 1
    end_year = start_year + 1
    return f"{start_year}-{str(end_year)[2:]}"


def academic_year_bounds(start_month: int = 6, ref: date | None = None) -> tuple[date, date]:
    """Return (start_date, end_date) of the current academic year."""
    d = ref or date.today()
    if d.month >= start_month:
        start_year = d.year
    else:
        start_year = d.year - 1
    end_year = start_year + 1
    start = date(start_year, start_month, 1)
    end_month = start_month - 1 if start_month > 1 else 12
    end = date(end_year if start_month > 1 else start_year, end_month, 1)
    # Last day of end_month
    import calendar
    last_day = calendar.monthrange(end.year, end.month)[1]
    end = date(end.year, end.month, last_day)
    return start, end
