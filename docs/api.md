# EduForge — API Reference

Base URLs:
- Identity Service: `http://localhost:8001/api/v1`
- Interactive Docs: `http://localhost:8001/docs`

---

## Authentication — Identity Service (port 8001)

### POST `/auth/otp/send`
Send OTP to mobile via WhatsApp (SMS fallback).

**Request**
```json
{
  "mobile": "9876543210"
}
```

**Response**
```json
{
  "message": "OTP sent",
  "dev_otp": "482913"   // only in DEBUG mode
}
```

---

### POST `/auth/otp/verify`
Verify OTP and receive JWT tokens.

**Request**
```json
{
  "mobile": "9876543210",
  "otp": "482913"
}
```

**Response**
```json
{
  "access_token": "eyJhbGci...",
  "refresh_token": "eyJhbGci...",
  "token_type": "bearer"
}
```

**Error**
```json
{ "detail": "Invalid or expired OTP" }   // 401
```

---

### POST `/auth/token/refresh`
Exchange refresh token for a new access token.

**Request**
```json
{
  "refresh_token": "eyJhbGci..."
}
```

**Response**
```json
{
  "access_token": "eyJhbGci...",
  "refresh_token": "eyJhbGci...",
  "token_type": "bearer"
}
```

---

### GET `/health`
Health check.

**Response**
```json
{ "status": "ok", "service": "identity" }
```

---

## JWT Token Structure

### Access Token Payload
```json
{
  "sub": "123",           // user_id
  "role": "student",      // role string
  "inst": 45,             // institution_id (null for platform users)
  "exp": 1711234567       // expiry timestamp
}
```

All services verify the JWT locally using `JWT_SECRET_KEY` — no network call needed.

---

## Planned Endpoints (upcoming branches)

### Exam Service (port 8003)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/exam/session/start` | Start exam session, get CDN URL |
| POST | `/exam/session/{id}/submit` | Submit all answers |
| GET | `/exam/session/{id}/recover` | Recover crashed session |
| GET | `/exam/results/{attempt_id}` | Get result (served from CDN) |

### Portal Service (port 8002)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/students/` | List students (staff only) |
| POST | `/students/` | Enrol new student |
| GET | `/attendance/{date}` | Get attendance for date |
| POST | `/attendance/` | Mark attendance |
| GET | `/fees/{student_id}` | Fee statement |

### MCQ / AI Service (port 8006)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/mcq/generate` | Generate MCQs via AI |
| POST | `/mcq/approve/{id}` | Approve question |
| GET | `/mcq/bank` | Browse question bank |

---

## Error Codes

| Code | Meaning |
|---|---|
| 400 | Bad request / validation error |
| 401 | Invalid or expired token / OTP |
| 403 | Insufficient permissions |
| 404 | Resource not found |
| 429 | Rate limit exceeded |
| 500 | Internal server error |
