# Test Credentials — GOVERN.AI

## Admin (seeded at first boot)
- Username: `admin`
- Password: `AdminGovern2026!`  (value of `ADMIN_PASSWORD` in `backend/.env`)
- Role: `admin`
- Email: `admin@govern.ai`

Note: The admin password is NO LONGER hardcoded in source/public files. It is read
from the `ADMIN_PASSWORD` env var (`backend/.env`, gitignored). If `ADMIN_PASSWORD`
is unset in a fresh environment, a secure random password is generated at first boot
and printed ONCE to the backend console/logs.

## Auth
- Login: `POST /api/auth/login` with `{"username": "...", "password": "..."}` → returns `{ "token": ..., "user": ... }`
- Current user: `GET /api/auth/me` (Bearer token)

## Health
- `GET /api/health` and `GET /health` → `{ status, database, llm_provider, version }`
