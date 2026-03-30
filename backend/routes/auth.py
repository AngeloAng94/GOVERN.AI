from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timezone, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
import os
import uuid
import logging

from database import db
from models import UserCreate, UserLogin, AuditLog, AuditOutcome, ROLE_HIERARCHY

logger = logging.getLogger(__name__)

JWT_SECRET = os.environ['JWT_SECRET_KEY']
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 8
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=False)

# Import limiter from shared module
from rate_limiter import limiter

router = APIRouter(prefix="/api/auth", tags=["auth"])


def create_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRATION_HOURS)
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(status_code=401, detail="Authentication required")
    payload = verify_token(credentials.credentials)
    user = await db.users.find_one({"username": payload.get("sub")}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def require_role(min_role: str):
    async def role_checker(user: dict = Depends(get_current_user)):
        user_level = ROLE_HIERARCHY.get(user.get("role"), 0)
        required_level = ROLE_HIERARCHY.get(min_role, 0)
        if user_level < required_level:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return role_checker


async def get_current_user_from_token(token: str):
    """Validate a JWT token string directly (for SSE endpoints where headers aren't available)."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user = await db.users.find_one({"username": payload.get("sub")}, {"_id": 0})
        return user
    except JWTError:
        return None


@router.post("/login")
@limiter.limit("5/minute")
async def login(request: Request, data: UserLogin):
    user = await db.users.find_one({"username": data.username}, {"_id": 0})
    if not user or not pwd_context.verify(data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"sub": user["username"], "role": user["role"]})
    log = AuditLog(action="user_login", resource="/auth/login", outcome=AuditOutcome.allowed, details=f"User '{data.username}' logged in", user=data.username)
    await db.audit_logs.insert_one(log.model_dump())
    return {"token": token, "user": {"id": user["id"], "username": user["username"], "email": user["email"], "role": user["role"], "full_name": user.get("full_name", "")}}


@router.post("/register")
@limiter.limit("3/minute")
async def register(request: Request, data: UserCreate, admin: dict = Depends(require_role("admin"))):
    existing = await db.users.find_one({"$or": [{"username": data.username}, {"email": data.email}]})
    if existing:
        raise HTTPException(status_code=409, detail="Username or email already exists")
    user_doc = {
        "id": str(uuid.uuid4()),
        "username": data.username,
        "email": data.email,
        "password_hash": pwd_context.hash(data.password),
        "role": data.role.value,
        "full_name": data.full_name,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.users.insert_one(user_doc)
    log = AuditLog(action="user_registered", resource="/auth/register", outcome=AuditOutcome.allowed, details=f"User '{data.username}' registered by '{admin['username']}'", user=admin["username"])
    await db.audit_logs.insert_one(log.model_dump())
    return {"id": user_doc["id"], "username": user_doc["username"], "email": user_doc["email"], "role": user_doc["role"], "full_name": user_doc["full_name"]}


@router.get("/me")
async def get_me(user: dict = Depends(get_current_user)):
    return {"id": user["id"], "username": user["username"], "email": user["email"], "role": user["role"], "full_name": user.get("full_name", "")}


@router.post("/logout")
async def logout(user: dict = Depends(get_current_user)):
    log = AuditLog(action="user_logout", resource="/auth/logout", outcome=AuditOutcome.allowed, details=f"User '{user['username']}' logged out", user=user["username"])
    await db.audit_logs.insert_one(log.model_dump())
    return {"message": "Logged out successfully"}
