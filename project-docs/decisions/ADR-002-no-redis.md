# ADR-002 — No Redis

**Date:** 2026-04-01  
**Status:** Accepted

## Decision

Do not use Redis. Replace all Redis use cases with PostgreSQL + Cloudflare.

## Replacements

| Redis Use Case | Replacement |
|---|---|
| OTP storage (5 min TTL) | `identity.otps` table with `expires_at` |
| Rate limiting | `identity.rate_limits` + COUNT query |
| JWT validation | Stateless JWT — no network call |
| Fragment cache | Cloudflare CDN `Cache-Control` |
| Session store | Stateless JWT + refresh token in DB |
| Nightly cleanup | AWS EventBridge cron at 2 AM IST |

## Saving

₹16,800/year + zero ops overhead.
