from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path
import os
import logging
import pymongo

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

logger = logging.getLogger(__name__)

MONGO_URL = os.environ.get('MONGO_URL')
if not MONGO_URL:
    raise RuntimeError("MONGO_URL environment variable is required")
client = AsyncIOMotorClient(MONGO_URL)
db = client[os.environ['DB_NAME']]


async def create_indexes():
    await db.agents.create_index("id", unique=True, background=True)
    await db.agents.create_index("status", background=True)
    await db.agents.create_index("risk_level", background=True)
    await db.policies.create_index("id", unique=True, background=True)
    await db.policies.create_index("regulation", background=True)
    await db.policies.create_index("agent_id", background=True)
    await db.audit_logs.create_index("id", unique=True, background=True)
    await db.audit_logs.create_index([("timestamp", -1)], background=True)
    await db.audit_logs.create_index("outcome", background=True)
    await db.audit_logs.create_index("risk_level", background=True)
    await db.audit_logs.create_index("agent_name", background=True)
    await db.compliance_standards.create_index("id", unique=True, background=True)
    await db.compliance_standards.create_index("code", unique=True, background=True)
    await db.chat_messages.create_index([("session_id", 1), ("timestamp", 1)], background=True)
    await db.users.create_index("username", unique=True, background=True)
    await db.users.create_index("email", unique=True, background=True)
    await db.sox_controls.create_index("id", unique=True, background=True)
    await db.sox_controls.create_index("domain", background=True)
    await db.conflict_scans.create_index([("timestamp", pymongo.DESCENDING)], background=True)
    await db.resolved_conflicts.create_index("conflict_id", background=True)
    await db.resolved_conflicts.create_index([("resolved_at", pymongo.DESCENDING)], background=True)
    await db.score_history.create_index([("timestamp", pymongo.DESCENDING)], background=True)
    await db.score_history.create_index("entity_type", background=True)
    logger.info("All indexes created")


async def close_connection():
    client.close()
    logger.info("MongoDB connection closed")
