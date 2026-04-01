"""Shared input validators — mobile, email, GST, PAN, Aadhaar."""
import re


MOBILE_RE = re.compile(r"^[6-9]\d{9}$")
EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}$")
GST_RE = re.compile(r"^\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}$")
PAN_RE = re.compile(r"^[A-Z]{5}\d{4}[A-Z]{1}$")
AADHAAR_RE = re.compile(r"^\d{12}$")


def is_valid_mobile(mobile: str) -> bool:
    return bool(MOBILE_RE.match(mobile))


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_RE.match(email))


def is_valid_gstin(gst: str) -> bool:
    return bool(GST_RE.match(gst))


def is_valid_pan(pan: str) -> bool:
    return bool(PAN_RE.match(pan.upper()))


def is_valid_aadhaar(aadhaar: str) -> bool:
    return bool(AADHAAR_RE.match(aadhaar))
