"""Institution schemas."""
from api.modules.institution.schemas.institution_schema import OnboardingRequest, InstitutionProfileOut
from api.modules.institution.schemas.id_card_schema import (
    IDCardTemplateCreate, IDCardTemplateOut, IDCardIssueRequest, IDCardOut, IDCardRevokeRequest,
)
from api.modules.institution.schemas.visitor_schema import (
    VisitorCreate, VisitorOut, GatePassScan, VisitorApprove, SettingUpsert, SettingOut,
)
