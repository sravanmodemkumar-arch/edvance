"""Visitor management schemas — walk-in, appointment, gate pass."""
from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field
from api.modules.institution.models.visitor import VisitorPurpose, GatePassStatus


class VisitorCreate(BaseModel):
    """Walk-in visitor or pre-booked appointment."""
    visitor_name: str = Field(..., min_length=2, max_length=120)
    visitor_phone: str = Field(..., pattern=r"^[6-9]\d{9}$")
    visitor_id_type: str = Field("AADHAR", max_length=20)
    visitor_id_number: str | None = None
    purpose: VisitorPurpose
    host_name: str | None = None
    host_user_id: int | None = None
    student_id: int | None = None
    expected_at: datetime | None = None
    vehicle_number: str | None = Field(None, max_length=15)
    notes: str | None = None


class VisitorOut(BaseModel):
    id: int
    institution_id: int
    visitor_name: str
    visitor_phone: str
    purpose: VisitorPurpose
    host_name: str | None
    gate_pass_status: GatePassStatus
    qr_token: str | None
    expected_at: datetime | None
    checked_in_at: datetime | None
    checked_out_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class GatePassScan(BaseModel):
    """Gate staff scans QR token to check visitor in or out."""
    qr_token: str
    action: str = Field(..., pattern=r"^(CHECK_IN|CHECK_OUT)$")


class VisitorApprove(BaseModel):
    """Security/admin approves a pending walk-in or appointment."""
    visitor_id: int
    approved: bool
    notes: str | None = None


class SettingUpsert(BaseModel):
    """Create or update an institution setting."""
    category: str
    key: str = Field(..., min_length=2, max_length=80)
    value: str = Field(..., min_length=1)
    description: str | None = None


class SettingOut(BaseModel):
    id: int
    institution_id: int
    category: str
    key: str
    value: str
    requires_approval: bool
    is_pending_approval: bool

    model_config = {"from_attributes": True}
