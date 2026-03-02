from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from contextlib import asynccontextmanager
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv
from pathlib import Path
import os
import logging

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from database import create_indexes, close_connection
from seed import seed_database
from routes.auth import router as auth_router
from routes.agents import router as agents_router
from routes.policies import router as policies_router
from routes.audit import router as audit_router
from routes.compliance import router as compliance_router
from routes.dashboard import router as dashboard_router
from routes.chat import router as chat_router
from rate_limiter import limiter


# Security headers middleware (B3)
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        return response


# Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_indexes()
    await seed_database()
    logger.info("GOVERN.AI startup complete")
    yield
    await close_connection()
    logger.info("GOVERN.AI shutdown complete")


app = FastAPI(lifespan=lifespan)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Security headers
app.add_middleware(SecurityHeadersMiddleware)

# Routers
app.include_router(auth_router)
app.include_router(agents_router)
app.include_router(policies_router)
app.include_router(audit_router)
app.include_router(compliance_router)
app.include_router(dashboard_router)
app.include_router(chat_router)


@app.get("/api/")
async def root():
    return {"message": "GOVERN.AI API - Sovereign AI Control Plane"}


# CORS
allowed_origins_str = os.environ.get('ALLOWED_ORIGINS', '')
cors_origins = [o.strip() for o in allowed_origins_str.split(',') if o.strip()] if allowed_origins_str else os.environ.get('CORS_ORIGINS', '*').split(',')
app.add_middleware(CORSMiddleware, allow_credentials=True, allow_origins=cors_origins, allow_methods=["*"], allow_headers=["*"])
