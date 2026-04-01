# Module 01 — Auth

## Stack

| Layer | Technology |
|---|---|
| API | FastAPI 0.111 · Python 3.12 |
| Auth Standard | OAuth2 (FastAPI native) · JWT HS256 |
| Password Hashing | passlib · bcrypt (cost 12) |
| JWT Library | python-jose |
| Database | PostgreSQL 16 · SQLAlchemy 2.0 · Alembic |
| Queue | AWS SQS (critical ops only) |
| Storage | Cloudflare R2 (logos, avatars, tenant branding JSON) |
| CDN | Cloudflare (tenant branding cached 1hr at edge) |
| Mobile | Flutter · Riverpod |
| Runtime | AWS Lambda · Mangum |
| Port | 8001 |

---

## What This Module Owns

| Concern | Owner |
|---|---|
| User identity (phone, email, password hash) | ✅ Auth |
| OAuth2 token issuance (access + refresh) | ✅ Auth |
| OTP generation + validation (critical ops only) | ✅ Auth |
| Session management (device, IP, last seen) | ✅ Auth |
| Tenant branding resolution (login + home page) | ✅ Auth |
| Password policy + account lockout | ✅ Auth |
| Google OAuth2 social login | ✅ Auth |
| Self-registration (B2C exam domain only) | ✅ Auth |
| Role assignment | ❌ Module 03-iam |
| Permission checks | ❌ Module 03-iam |
| OTP delivery (SMS / WhatsApp) | ❌ Module 04-notifications |
| Institution / DB provisioning | ❌ Module 02-tenancy |

---

## Critical Rule — OTP Usage

> **Login does NOT use OTP. Login = phone/email + password.**
> OTP is sent ONLY before irreversible or high-risk operations.

| Operation | OTP Required | Delivery |
|---|---|---|
| Login | ❌ Never | — |
| Register | ❌ Never | — |
| Forgot password | ✅ Yes | WhatsApp (MSG91) |
| Change password (logged in) | ✅ Yes | WhatsApp |
| Delete account | ✅ Yes | WhatsApp + Email both |
| Change registered phone | ✅ Yes | Old + new number |
| Change registered email | ✅ Yes | Old + new email |
| Payment above ₹10,000 | ✅ Yes | WhatsApp |
| Export all user data (DSAR) | ✅ Yes | Email |
| Deactivate institution (platform admin) | ✅ Yes | Email |

---

## OAuth2 Flows

FastAPI provides OAuth2 natively. Three flows are used across EduForge.

### Flow 1 — Password Grant (Web Portal + Mobile, First-Party)

Used by: Django HTMX portal, Flutter mobile app.

```python
# identity/app/api/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.auth_service import AuthService
from app.utils.jwt import create_access_token, create_refresh_token
from app.database import get_db

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

@router.post("/api/v1/auth/token")
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
    tenant_id: str = Header(...),        # injected by subdomain middleware
):
    user = await AuthService(db).authenticate(
        identifier=form.username,        # phone or email
        password=form.password,
        tenant_id=tenant_id,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token  = create_access_token(user, tenant_id)
    refresh_token = await create_refresh_token(user, tenant_id, db)

    return {
        "access_token": access_token,
        "token_type":   "bearer",
        "expires_in":   900,             # 15 minutes
        "user": {
            "id":         str(user.id),
            "name":       user.full_name,
            "role":       user.primary_role,
            "avatar_url": user.avatar_url,
        },
        "redirect_to": get_dashboard_url(user.primary_role),
    }
```

### Flow 2 — Authorization Code + PKCE (B2B Partners, Third-Party Apps)

Used by: B2B API partners, government integrations, external LMS systems.
PKCE is mandatory — no client secret exposure.

```python
from fastapi.security import OAuth2AuthorizationCodeBearer

oauth2_code = OAuth2AuthorizationCodeBearer(
    authorizationUrl="/api/v1/auth/authorize",
    tokenUrl="/api/v1/auth/token",
)

# Step 1 — Partner redirects user to EduForge:
# GET /api/v1/auth/authorize
#   ?response_type=code
#   &client_id=partner_xyz
#   &redirect_uri=https://partner.com/callback
#   &scope=read:students read:results
#   &code_challenge=BASE64URL(SHA256(code_verifier))   ← PKCE
#   &code_challenge_method=S256
#   &state=random_csrf_state

# Step 2 — User logs in + consents → redirect back:
# GET https://partner.com/callback?code=AUTH_CODE&state=...

# Step 3 — Partner exchanges code for token:
# POST /api/v1/auth/token
# { grant_type: authorization_code, code: AUTH_CODE,
#   code_verifier: PKCE_ORIGINAL, client_id: ..., redirect_uri: ... }
```

### Flow 3 — Client Credentials (Service-to-Service)

Used by: B2B API partners for server-to-server calls, no user involved.

```python
# POST /api/v1/auth/token
# {
#   "grant_type":    "client_credentials",
#   "client_id":     "partner_client_id",
#   "client_secret": "partner_client_secret",
#   "scope":         "read:results write:attendance"
# }
# Returns: service access token (1 hour expiry, no refresh token)
```

### Flutter Mobile — Secure Token Storage

```dart
// lib/features/auth/providers/auth_provider.dart

final authProvider = StateNotifierProvider<AuthNotifier, AuthState>(
  (ref) => AuthNotifier(ref.read(authRepositoryProvider)),
);

class AuthNotifier extends StateNotifier<AuthState> {
  AuthNotifier(this._repo) : super(const AuthState.initial());
  final AuthRepository _repo;

  Future<void> login(String identifier, String password, String tenantId) async {
    state = const AuthState.loading();
    try {
      final tokens = await _repo.loginWithPassword(
        identifier: identifier,
        password:   password,
        tenantId:   tenantId,
      );
      // flutter_secure_storage — encrypted on device, not SharedPreferences
      await _secureStorage.write(key: 'access_token',  value: tokens.accessToken);
      await _secureStorage.write(key: 'refresh_token', value: tokens.refreshToken);
      state = AuthState.authenticated(tokens.user);
    } catch (e) {
      state = AuthState.error(e.toString());
    }
  }

  Future<void> logout() async {
    await _repo.logout();
    await _secureStorage.deleteAll();
    state = const AuthState.unauthenticated();
  }
}
```

---

## Dynamic Home Page + Login — How It Works

Every institution has its own subdomain. Users see the **institution's public home page first** — not a login screen. Login is a button on the home page.

```
SUBDOMAIN ROUTING
─────────────────
abc-school.schools.eduforge.in      → School public home + login
xyz.colleges.eduforge.in            → College public home + login
vision.coaching.eduforge.in         → Coaching center home + login
ssc.eduforge.in                     → SSC exam domain home + login
rrb.eduforge.in                     → RRB exam domain home + login
upsc.eduforge.in                    → UPSC exam domain home + login
eduforge.in                         → Platform B2B landing page


TENANT RESOLUTION — EVERY REQUEST
──────────────────────────────────
User visits: abc-school.schools.eduforge.in
      │
      ▼
Cloudflare DNS → ECS Fargate (Django portal)
      │
      ▼
Django Middleware → extract subdomain → "abc-school"
      │
      ▼
Call Tenant Lambda: GET /api/v1/tenant/config/abc-school
(Cloudflare CDN caches this 1 hour — TTL_1HR · LAZY flag — zero DB hit on cache hit)
(If branding updated by admin → IMMEDIATE flag → purges CDN within 5 min)
(If user inactive 2+ days → CDN files deleted nightly at 3AM → re-fetched on return)
      │
      ▼
Returns branding JSON from Cloudflare R2:
{
  "tenant_id":         "sch_0501",
  "institution_name":  "ABC High School",
  "institution_type":  "SCHOOL",
  "logo_url":          "https://cdn.eduforge.in/tenants/sch_0501/logo.png",
  "favicon_url":       "https://cdn.eduforge.in/tenants/sch_0501/favicon.ico",
  "cover_image_url":   "https://cdn.eduforge.in/tenants/sch_0501/cover.jpg",
  "primary_color":     "#1E40AF",
  "secondary_color":   "#DBEAFE",
  "text_on_primary":   "#FFFFFF",
  "tagline":           "Excellence in Education Since 1995",
  "address":           "Hyderabad, Telangana",
  "phone":             "+91-40-12345678",
  "email":             "info@abcschool.edu.in",
  "established_year":  1995,
  "board":             "CBSE",
  "is_active":         true,
  "public_notices": [
    { "title": "Exam schedule released", "date": "2026-03-20", "priority": "high" },
    { "title": "PTM on Saturday 10 AM",  "date": "2026-03-22", "priority": "normal" }
  ],
  "social": { "youtube": "...", "instagram": "...", "facebook": "..." }
}
      │
      ▼
Render PUBLIC HOME PAGE with school branding (no auth required)
      │
      ▼ [Login button clicked]
Render LOGIN PAGE — same subdomain, same branding, no reload
      │
      ▼ [User submits credentials]
POST /api/v1/auth/token → Identity Lambda
      │
      ▼
JWT returned → redirect to role-based dashboard
```

---

## Public Home Page — Per Institution Type

### School / College
```
╔══════════════════════════════════════════════════════════════════╗
║ [logo]  ABC High School · Hyderabad          [Login]  [Contact] ║
╠══════════════════════════════════════════════════════════════════╣
║  [COVER IMAGE — campus photo from R2]                            ║
║  "Welcome to ABC High School"                                    ║
║  "Excellence in Education Since 1995 · CBSE · Grade 1–12"       ║
║  [Apply for Admission]    [View Results]    [Login →]            ║
╠══════════════╦═══════════════════╦═══════════════════════════════╣
║  ABOUT       ║  ANNOUNCEMENTS    ║  QUICK LINKS                  ║
║  Est. 1995   ║  ● Exam schedule  ║  → Admission Form             ║
║  CBSE Board  ║  ● PTM Saturday   ║  → Fee Payment                ║
║  2,400 stud. ║  ● Holiday notice ║  → Results                    ║
║  Grade 1–12  ║  ● Sports Day     ║  → Timetable                  ║
╠══════════════╩═══════════════════╩═══════════════════════════════╣
║  ACHIEVEMENTS       GALLERY       CONTACT       SOCIAL           ║
╚══════════════════════════════════════════════════════════════════╝
```

### Coaching Center
```
╔══════════════════════════════════════════════════════════════════╗
║ [logo]  Vision IIT Academy               [Login]  [Free Demo →] ║
╠══════════════════════════════════════════════════════════════════╣
║  "IIT JEE 2024 — 342 Selections · NEET 2024 — 189 Selections"   ║
║  [Join Now]    [View Batches]    [Free Demo Class]    [Login →]  ║
╠══════════════════════════════════════════════════════════════════╣
║  BATCHES          RESULTS 2024        FACULTY        CONTACT     ║
╚══════════════════════════════════════════════════════════════════╝
```

### Exam Domain (ssc.eduforge.in)
```
╔══════════════════════════════════════════════════════════════════╗
║ [EduForge SSC]  SSC Exam Prep             [Login]  [Join Free →]║
╠══════════════════════════════════════════════════════════════════╣
║  "2,00,000+ Questions · 500+ Mock Tests · Live AIR Rankings"    ║
║  [Start Free]     [View Plans ₹99/mo]                            ║
╠══════════════════════════════════════════════════════════════════╣
║  TODAY'S QUIZ    CURRENT AFFAIRS    TOPPERS    FREE MOCK TEST    ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## Login Page — Dynamic Branding

```
╔══════════════════════════════════════════════════════════════╗
║  [institution logo — from R2 CDN]                            ║
║  ABC High School                                             ║
║  Hyderabad, Telangana                                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║           Welcome Back                                       ║
║           Sign in to your account                            ║
║                                                              ║
║   Phone number or Email                                      ║
║   ┌──────────────────────────────────────────────────┐      ║
║   │  📱  9876543210                                   │      ║
║   └──────────────────────────────────────────────────┘      ║
║                                                              ║
║   Password                                                   ║
║   ┌──────────────────────────────────────────────────┐      ║
║   │  ••••••••••                             [Show]   │      ║
║   └──────────────────────────────────────────────────┘      ║
║                                                              ║
║   [✓] Remember me (30 days)     Forgot password? →          ║
║                                                              ║
║   ┌──────────────────────────────────────────────────┐      ║
║   │               Login  →                           │      ║  ← primary_color bg
║   └──────────────────────────────────────────────────┘      ║
║                                                              ║
║   ─────────────── or continue with ──────────────────        ║
║   [G  Sign in with Google]                                   ║
║                                                              ║
║   Institution portals: contact your admin for access.        ║
║   SSC / UPSC / Banking: Register free →     ← B2C only       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

> Logo, button color, accent = institution's `primary_color` from branding JSON.
> B2C exam domains (ssc, rrb, upsc, banking) show "Register free".
> Institution portals (school, college, coaching) never show self-registration.

---

## Login Flow — Complete

```
1. POST /api/v1/auth/token
   Content-Type: application/x-www-form-urlencoded
   X-Tenant-ID: sch_0501         ← set by middleware from subdomain

   username=9876543210&password=MyPass@123&grant_type=password

2. AuthService.authenticate()
   a. SELECT FROM platform.users WHERE phone=? OR email=?
   b. Check user exists in platform.user_tenants for this tenant_id
   c. Check user.is_active = true, locked_until < now()
   d. bcrypt.verify(password, user.password_hash)
   e. Check tenant is_active (call 02-tenancy sync)
   f. GET roles from 03-iam sync call
   g. Increment login_attempts on failure; reset on success

3. Access Token — JWT HS256, 15 min
   {
     "sub":              "usr_abc123",
     "tenant_id":        "sch_0501",
     "institution_type": "SCHOOL",
     "roles":            ["TEACHER"],
     "scopes":           ["read:students", "write:attendance"],
     "session_id":       "sess_xyz789",
     "iat": 1711123456,
     "exp": 1711124356
   }

4. Refresh Token — opaque UUID, 7 days
   Stored hashed in platform.sessions
   Set as HttpOnly · Secure · SameSite=Strict cookie

5. Session record created in platform.sessions

6. Response → redirect_to role-based dashboard
```

---

## Token Refresh

```python
# identity/app/api/auth.py

@router.post("/api/v1/auth/token/refresh")
async def refresh(request: Request, db: AsyncSession = Depends(get_db)):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(401, "No refresh token")

    session = await db.scalar(
        select(Session)
        .where(
            Session.refresh_token_hash == sha256(token),
            Session.is_active == True,
            Session.expires_at > datetime.utcnow(),
        )
    )
    if not session:
        raise HTTPException(401, "Session expired — please login again")

    user = await db.get(User, session.user_id)
    new_token = create_access_token(user, session.tenant_id)
    session.last_active_at = datetime.utcnow()
    await db.commit()

    return {"access_token": new_token, "expires_in": 900}
```

---

## Forgot Password — OTP Flow

```
1. GET /forgot-password → tenant-branded form

2. POST /api/v1/auth/otp/send
   { "phone": "9876543210", "purpose": "PASSWORD_RESET" }
   → Verify phone exists in tenant
   → Rate check: max 3 requests / 10 min (platform.otp_rate_limits)
   → Generate 6-digit OTP → bcrypt hash → store in platform.otps (10 min TTL)
   → SQS → 04-notifications → WhatsApp via MSG91
   → Response: { "masked_phone": "98****3210", "expires_in": 600 }

3. POST /api/v1/auth/otp/verify
   { "phone": "9876543210", "otp": "482910", "purpose": "PASSWORD_RESET" }
   → Hash input OTP → compare with stored hash
   → Check expiry, check attempts < max_attempts
   → Mark OTP used → return password_reset_token (5 min only)

4. POST /api/v1/auth/password/reset
   { "password_reset_token": "...", "new_password": "NewPass@123" }
   → Validate token (5 min), enforce password policy
   → bcrypt hash new password → update user
   → Invalidate ALL sessions for this user
   → Response: "Password updated. Please login again."
```

---

## Password Policy

```python
# identity/app/utils/security.py

import re

def validate_password(password: str) -> tuple[bool, str]:
    rules = [
        (len(password) >= 8,               "Minimum 8 characters required"),
        (re.search(r'[A-Z]', password),    "At least one uppercase letter"),
        (re.search(r'[a-z]', password),    "At least one lowercase letter"),
        (re.search(r'\d', password),       "At least one number"),
        (re.search(r'[!@#$%^&*]',password),"At least one special character"),
    ]
    for passes, message in rules:
        if not passes:
            return False, message
    return True, "OK"

# Lockout
MAX_ATTEMPTS   = 5
LOCK_15_MIN    = timedelta(minutes=15)   # after 5 failures
LOCK_24_HR     = timedelta(hours=24)     # after 10 failures
```

---

## OTP Storage — PostgreSQL Only (No Extra Service Needed)

```python
# identity/app/models/otp.py — SQLAlchemy 2.0

class OTP(Base):
    __tablename__  = "otps"
    __table_args__ = {"schema": "platform"}

    id:           Mapped[UUID]     = mapped_column(primary_key=True, default=uuid4)
    user_id:      Mapped[UUID]     = mapped_column(ForeignKey("platform.users.id"))
    otp_hash:     Mapped[str]      = mapped_column(String(255))
    purpose:      Mapped[str]      = mapped_column(String(50))
    # PASSWORD_RESET | ACCOUNT_DELETE | PHONE_CHANGE | EMAIL_CHANGE | PAYMENT_CONFIRM
    expires_at:   Mapped[datetime]
    attempts:     Mapped[int]      = mapped_column(SmallInteger, default=0)
    max_attempts: Mapped[int]      = mapped_column(SmallInteger, default=3)
    used_at:      Mapped[datetime] = mapped_column(nullable=True)
    created_at:   Mapped[datetime] = mapped_column(default=datetime.utcnow)


class OTPRateLimit(Base):
    __tablename__  = "otp_rate_limits"
    __table_args__ = {"schema": "platform"}

    phone:         Mapped[str]      = mapped_column(String(15), primary_key=True)
    window_start:  Mapped[datetime]
    request_count: Mapped[int]      = mapped_column(SmallInteger, default=0)
    # Rule: max 3 OTP requests per phone per 10 minutes
```

---

## Database Schema

```sql
-- Alembic: identity/migrations/versions/001_auth_tables.py

CREATE TABLE platform.users (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone             VARCHAR(15)  UNIQUE NOT NULL,
    email             VARCHAR(255) UNIQUE,
    password_hash     VARCHAR(255) NOT NULL,
    full_name         VARCHAR(255) NOT NULL,
    avatar_url        VARCHAR(500),
    is_active         BOOLEAN     DEFAULT true,
    is_phone_verified BOOLEAN     DEFAULT false,
    is_email_verified BOOLEAN     DEFAULT false,
    login_attempts    SMALLINT    DEFAULT 0,
    locked_until      TIMESTAMPTZ,
    last_login_at     TIMESTAMPTZ,
    last_login_ip     INET,
    created_at        TIMESTAMPTZ DEFAULT now(),
    updated_at        TIMESTAMPTZ DEFAULT now()
);

-- One user → many institutions (school + coaching + exam domain)
CREATE TABLE platform.user_tenants (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id          UUID        NOT NULL REFERENCES platform.users(id) ON DELETE CASCADE,
    tenant_id        VARCHAR(50) NOT NULL,
    institution_type VARCHAR(20) NOT NULL,
    -- SCHOOL | COLLEGE | COACHING | EXAM_DOMAIN | PLATFORM | TSP | B2B
    is_active        BOOLEAN     DEFAULT true,
    created_at       TIMESTAMPTZ DEFAULT now(),
    UNIQUE (user_id, tenant_id)
);
CREATE INDEX idx_user_tenants_tenant ON platform.user_tenants(tenant_id);

-- Sessions (refresh tokens)
CREATE TABLE platform.sessions (
    id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id            UUID        NOT NULL REFERENCES platform.users(id) ON DELETE CASCADE,
    tenant_id          VARCHAR(50) NOT NULL,
    refresh_token_hash VARCHAR(255) UNIQUE NOT NULL,
    device_id          VARCHAR(255),
    device_type        VARCHAR(10) DEFAULT 'WEB',   -- WEB | ANDROID | IOS
    ip_address         INET,
    user_agent         TEXT,
    is_active          BOOLEAN     DEFAULT true,
    created_at         TIMESTAMPTZ DEFAULT now(),
    last_active_at     TIMESTAMPTZ DEFAULT now(),
    expires_at         TIMESTAMPTZ NOT NULL
);

-- OTPs (critical ops only)
CREATE TABLE platform.otps (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id      UUID        NOT NULL REFERENCES platform.users(id) ON DELETE CASCADE,
    otp_hash     VARCHAR(255) NOT NULL,
    purpose      VARCHAR(50)  NOT NULL,
    expires_at   TIMESTAMPTZ  NOT NULL,
    attempts     SMALLINT     DEFAULT 0,
    max_attempts SMALLINT     DEFAULT 3,
    used_at      TIMESTAMPTZ,
    created_at   TIMESTAMPTZ  DEFAULT now()
);

-- OTP rate limiting
CREATE TABLE platform.otp_rate_limits (
    phone         VARCHAR(15)  PRIMARY KEY,
    window_start  TIMESTAMPTZ  NOT NULL,
    request_count SMALLINT     DEFAULT 0
);

-- Password reset tokens (5 min only)
CREATE TABLE platform.password_reset_tokens (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id    UUID        NOT NULL REFERENCES platform.users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMPTZ  NOT NULL,
    used_at    TIMESTAMPTZ,
    created_at TIMESTAMPTZ  DEFAULT now()
);

-- OAuth2 clients (B2B partners — auth code flow)
CREATE TABLE platform.oauth2_clients (
    id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id          VARCHAR(100) UNIQUE NOT NULL,
    client_secret_hash VARCHAR(255) NOT NULL,
    client_name        VARCHAR(255) NOT NULL,
    redirect_uris      TEXT[]       NOT NULL,
    scopes             TEXT[]       NOT NULL,
    grant_types        TEXT[]       DEFAULT ARRAY['authorization_code'],
    is_active          BOOLEAN      DEFAULT true,
    created_at         TIMESTAMPTZ  DEFAULT now()
);

-- OAuth2 authorization codes (PKCE, 10 min)
CREATE TABLE platform.oauth2_codes (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code           VARCHAR(255) UNIQUE NOT NULL,
    client_id      VARCHAR(100) NOT NULL,
    user_id        UUID         NOT NULL,
    tenant_id      VARCHAR(50)  NOT NULL,
    scopes         TEXT[]       NOT NULL,
    code_challenge VARCHAR(255),         -- PKCE S256
    redirect_uri   VARCHAR(500) NOT NULL,
    expires_at     TIMESTAMPTZ  NOT NULL, -- 10 minutes
    used_at        TIMESTAMPTZ,
    created_at     TIMESTAMPTZ  DEFAULT now()
);
```

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/` | ❌ | Institution public home page (tenant-branded) |
| GET | `/login` | ❌ | Dynamic login page (tenant-branded) |
| POST | `/api/v1/auth/token` | ❌ | OAuth2 — password / auth_code / client_credentials |
| POST | `/api/v1/auth/token/refresh` | 🍪 Cookie | Refresh access token |
| POST | `/api/v1/auth/token/revoke` | ✅ Bearer | Revoke token |
| GET | `/api/v1/auth/authorize` | ❌ | OAuth2 authorization endpoint (B2B) |
| GET | `/api/v1/auth/userinfo` | ✅ Bearer | OIDC user info |
| GET | `/.well-known/openid-configuration` | ❌ | OIDC discovery document |
| POST | `/api/v1/auth/logout` | ✅ | Logout current session |
| POST | `/api/v1/auth/logout/all` | ✅ | Logout all devices |
| POST | `/api/v1/auth/register` | ❌ | B2C self-registration (exam domain only) |
| POST | `/api/v1/auth/otp/send` | ❌/✅ | Send OTP — critical ops only |
| POST | `/api/v1/auth/otp/verify` | ❌/✅ | Verify OTP |
| POST | `/api/v1/auth/password/forgot` | ❌ | Request password reset |
| POST | `/api/v1/auth/password/reset` | 🔑 Token | Set new password |
| POST | `/api/v1/auth/password/change` | ✅ + OTP | Change password (logged in) |
| POST | `/api/v1/auth/phone/change` | ✅ + OTP | Change phone number |
| POST | `/api/v1/auth/email/change` | ✅ + OTP | Change email |
| GET | `/api/v1/auth/sessions` | ✅ | List all active sessions |
| DELETE | `/api/v1/auth/sessions/{id}` | ✅ | Revoke a session |
| GET | `/api/v1/auth/me` | ✅ | Current user profile |
| PATCH | `/api/v1/auth/me` | ✅ | Update name, avatar |
| POST | `/api/v1/auth/account/delete/request` | ✅ | Request deletion — sends dual OTP |
| POST | `/api/v1/auth/account/delete/confirm` | ✅ + 2× OTP | Confirm account deletion |
| GET | `/api/v1/tenant/config/{subdomain}` | ❌ | Tenant branding JSON (CDN-cached 1hr) |
| POST | `/api/v1/auth/google` | ❌ | Google OAuth2 callback |

---

## Google OAuth2 — Social Login

```python
# identity/app/services/google_auth_service.py

import httpx
from app.core.config import settings

GOOGLE_TOKEN_URL    = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

async def handle_google_callback(code: str, tenant_id: str, db: AsyncSession):
    async with httpx.AsyncClient() as client:
        # Exchange code for Google tokens
        token_res = await client.post(GOOGLE_TOKEN_URL, data={
            "code":          code,
            "client_id":     settings.GOOGLE_CLIENT_ID,      # AWS Secrets Manager
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri":  settings.GOOGLE_REDIRECT_URI,
            "grant_type":    "authorization_code",
        })
        # Get user info from Google
        info_res = await client.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {token_res.json()['access_token']}"}
        )
    info = info_res.json()
    # { id, email, name, picture }

    # Find existing user or create new
    user = await find_or_create_social_user(
        email=info["email"],
        name=info["name"],
        avatar_url=info["picture"],
        tenant_id=tenant_id,
        db=db,
    )
    return create_access_token(user, tenant_id)
```

---

## OAuth2 Scopes

```
read:profile          View own profile
write:profile         Edit own profile, upload avatar
read:students         View student records
write:students        Create, edit student records
read:attendance       View attendance records
write:attendance      Mark, edit attendance
read:fees             View fee records
write:fees            Record payments, create fee structures
read:results          View exam results
write:results         Enter, edit, publish marks
read:timetable        View timetable
write:timetable       Create, edit timetable
admin:institution     Full institution admin access
admin:platform        Full platform admin access
exam:take             Take exams (students only)
exam:create           Create, schedule exams (faculty)
api:read              B2B API read-only access
api:write             B2B API read + write access
```

---

## Post-Login Redirect — Role Based

| Group | Role | Dashboard |
|---|---|---|
| Group 1 | Platform Admin | `/admin/dashboard/` |
| Group 2 | Chairman / CEO | `/group/dashboard/` |
| Group 3 | Principal | `/school/dashboard/principal/` |
| Group 3 | HOD | `/school/dashboard/hod/` |
| Group 3 | Teacher | `/school/dashboard/teacher/` |
| Group 3 | Student | `/school/dashboard/student/` |
| Group 4 | Principal | `/college/dashboard/principal/` |
| Group 4 | Lecturer | `/college/dashboard/lecturer/` |
| Group 4 | Student | `/college/dashboard/student/` |
| Group 5 | Center Director | `/coaching/dashboard/director/` |
| Group 5 | Faculty | `/coaching/dashboard/faculty/` |
| Group 5 | Student | `/coaching/dashboard/student/` |
| Group 6 | Subscriber | `/{domain}/dashboard/` |
| Group 7 | TSP Operator | `/tsp/dashboard/` |
| Group 8 | Parent | `/parent/dashboard/` |
| Group 9 | B2B Partner | `/partner/dashboard/` |

---

## SQS Events (Critical Ops Only)

| Queue | Event | Trigger | Consumer |
|---|---|---|---|
| `notifications.otp` | `otp.password_reset` | Forgot password | 04-notifications |
| `notifications.otp` | `otp.account_delete` | Account delete request | 04-notifications |
| `notifications.otp` | `otp.phone_change` | Phone change request | 04-notifications |
| `notifications.otp` | `otp.email_change` | Email change request | 04-notifications |
| `notifications.alert` | `alert.new_device_login` | New device detected | 04-notifications |
| `data.deletion` | `account.deletion_confirmed` | Deletion confirmed | All modules |

> All regular flows (login, logout, token refresh, profile view/edit) = synchronous. No SQS.

---

## Security

| Concern | Implementation |
|---|---|
| Password hashing | passlib · bcrypt · cost 12 |
| JWT | python-jose · HS256 · secret in AWS Secrets Manager |
| Refresh token | Opaque UUID · SHA-256 hashed in PostgreSQL |
| OTP | 6-digit numeric · bcrypt hashed · 3 attempts · 10 min expiry |
| Rate limiting | PostgreSQL otp_rate_limits — 3 OTPs / 10 min per phone |
| Login throttle | 5 failures → 15 min lock · 10 failures → 24 hr lock |
| HTTPS | Cloudflare enforced — HTTP → HTTPS always |
| Cookie | HttpOnly · Secure · SameSite=Strict · scoped to subdomain |
| PKCE | S256 required for all authorization code flow (OAuth 2.1) |
| Tenant isolation | Middleware enforces subdomain ↔ tenant_id on every request |
| Secrets | AWS Secrets Manager — never in .env or code |
| SQL injection | SQLAlchemy parameterized queries only — no raw SQL |

---

## UI Components

| Component | Page | Notes |
|---|---|---|
| Tenant navbar | Home + Login | Logo from R2 · primary_color applied to buttons |
| Hero banner | Public home | Cover image from R2 · 3 CTA buttons |
| Announcement list | Public home | Latest notices from branding JSON |
| Login form | Login | Phone/email + password · show/hide · remember me |
| Google button | Login | Standard Google branding |
| Password strength meter | Register + Reset | Live: weak / fair / strong / very strong |
| OTP input (6-box) | Forgot password / critical ops | Auto-advance · auto-submit on last digit · countdown timer |
| Toast | All pages | Error (red) · Success (green) · Info (blue) · auto-dismiss 4s |
| Skeleton loader | Home + Login | While tenant branding loads from CDN |
| Session table | My Sessions | Sortable · device icon (web/android/ios) · IP · last active · [Revoke] |
| Empty state | Sessions | "No other active sessions" |
| Role redirect | Post-login | Server-side 302 to role dashboard |
| Chart | — | Not applicable to auth module |

---

## Module File Structure

```
identity/
├── app/
│   ├── main.py                      ← FastAPI app init + Mangum handler
│   ├── api/
│   │   ├── auth.py                  ← token, login, logout, refresh, revoke
│   │   ├── otp.py                   ← send OTP, verify OTP
│   │   ├── password.py              ← forgot, reset, change
│   │   ├── profile.py               ← me, update, avatar, sessions
│   │   ├── oauth2.py                ← authorize endpoint, B2B flows
│   │   └── social.py                ← Google OAuth2 callback
│   ├── models/
│   │   ├── user.py                  ← User, UserTenant
│   │   ├── session.py               ← Session
│   │   ├── otp.py                   ← OTP, OTPRateLimit
│   │   ├── password_reset.py        ← PasswordResetToken
│   │   └── oauth2_client.py         ← OAuth2Client, OAuth2Code
│   ├── schemas/
│   │   ├── auth.py                  ← TokenResponse, LoginRequest
│   │   ├── otp.py                   ← OTPSendRequest, OTPVerifyRequest
│   │   └── user.py                  ← UserProfile, UserUpdate
│   ├── services/
│   │   ├── auth_service.py          ← authenticate, create tokens
│   │   ├── otp_service.py           ← generate, verify, rate-limit
│   │   ├── password_service.py      ← hash, verify, policy
│   │   ├── session_service.py       ← create, list, revoke
│   │   └── google_auth_service.py   ← Google OAuth2
│   ├── middleware/
│   │   └── tenant.py                ← subdomain → tenant_id extraction
│   ├── utils/
│   │   ├── jwt.py                   ← create_access_token, verify_token
│   │   └── security.py              ← hash_token, generate_otp, validate_password
│   └── database.py                  ← async SQLAlchemy engine + session
├── migrations/
│   ├── env.py
│   └── versions/
│       └── 001_auth_tables.py
├── tests/
│   ├── test_login.py
│   ├── test_otp.py
│   ├── test_refresh.py
│   └── test_oauth2.py
├── handler.py                       ← Lambda entrypoint (Mangum)
└── requirements.txt
```

---

## Dependencies

```
# requirements.txt — identity service

fastapi==0.111.0
mangum==0.17.0           # Lambda ASGI adapter — free
python-jose[cryptography]==3.3.0   # JWT — free
passlib[bcrypt]==1.7.4   # Password hashing — free
sqlalchemy==2.0.30       # ORM — free
alembic==1.13.1          # Migrations — free
asyncpg==0.29.0          # Async PostgreSQL driver — free
httpx==0.27.0            # Async HTTP (Google OAuth) — free
pydantic==2.7.0          # Schema validation — free
boto3==1.34.0            # AWS SQS — free library
python-multipart         # OAuth2 form data parsing — free
uvicorn==0.29.0          # Local dev server — free
```

> All dependencies are free and open source.

---

## Inter-Module Connections

```
01-auth
  ├──→ 02-tenancy        SYNC HTTP   Verify tenant active · fetch branding config
  ├──→ 03-iam            SYNC HTTP   Fetch roles + scopes after successful login
  ├──→ 04-notifications  SQS         Send OTPs (critical ops only — see SQS table)
  └──→ ALL OTHER MODULES —           Every module validates Bearer JWT from auth
```
