import os
import sys
import types
from unittest.mock import MagicMock

# ── 1. Required environment variables (must be set before any app import) ──────
os.environ.update({
    "DB_USERNAME":                 "test",
    "DB_PASSWORD":                 "test",
    "DB_HOST":                     "localhost",
    "DB_NAME":                     "test",
    "SECRET_KEY":                  "test-secret-key-do-not-use-in-production",
    "ALGORITHM":                   "HS256",
    "ACCESS_TOKEN_EXPIRE_MINUTES": "60",
    "LLM_PROVIDER":                "openai",
    "OPENAI_API_KEY":              "test-key",
    "OPENAI_BASE_URL":             "",
    "OPENAI_MODEL_NAME":           "gpt-4o-mini",
    "OPENAI_MAX_TOKENS":           "500",
    "OPENAI_TEMPERATURE":          "0.9",
    "OPENAI_VERBOSE":              "false",
    "OLLAMA_BASE_URL":             "http://localhost:11434",
    "OLLAMA_MODEL_NAME":           "llama3.2",
    "OLLAMA_VERBOSE":              "false",
    "BEDROCK_REGION_NAME":           "us-east-1",
    "BEDROCK_MODEL_ID":              "anthropic.claude-3-5-sonnet-20241022-v2:0",
    "BEDROCK_AWS_ACCESS_KEY_ID":     "test-access-key",
    "BEDROCK_AWS_SECRET_ACCESS_KEY": "test-secret-key",
    "BEDROCK_AWS_SESSION_TOKEN":     "",
    "BEDROCK_MAX_TOKENS":            "256",
    "BEDROCK_TEMPERATURE":           "0.9",
    "BEDROCK_VERBOSE":               "false",
    "GEMINI_API_KEY":                "test-gemini-key",
    "GEMINI_MODEL_NAME":             "gemini-1.5-pro",
    "GEMINI_MAX_TOKENS":             "256",
    "GEMINI_TEMPERATURE":            "0.9",
    "GEMINI_VERBOSE":                "false",
    "DK_API_URL":                  "https://example.com",
    "DK_FIREWALL_ID":              "test-fw",
    "DK_TOKEN":                    "test-token",
})

# ── 2. Mock LLM / NeMo modules to prevent import errors ───────────────────────
_LLM_MODULES = [
    "langchain",
    "langchain.chains",
    "langchain.prompts",
    "langchain.document_loaders",
    "langchain.chat_models",
    "langchain.utilities",
    "langchain.utilities.sql_database",
    "langchain_community",
    "langchain_community.llms",
    "langchain_aws",
    "langchain_google_genai",
    "langchain_experimental",
    "langchain_experimental.sql",
    "langchain_experimental.pal_chain",
    "langchain_experimental.pal_chain.base",
    "langchain_openai",
    "nemoguardrails",
    "nemoguardrails.integrations",
    "nemoguardrails.integrations.langchain",
    "nemoguardrails.integrations.langchain.runnable_rails",
    "openai",
]
for _mod in _LLM_MODULES:
    sys.modules.setdefault(_mod, MagicMock())

# ── 3. Replace app.db_settings with a SQLite-backed module before any app import
#       This prevents SQLAlchemy from loading the PyMySQL driver at import time.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import StaticPool

# StaticPool ensures all connections share the same in-memory database
_test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
_TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=_test_engine)
_Base = declarative_base()

_db_settings_stub = types.ModuleType("app.db_settings")
_db_settings_stub.engine = _test_engine
_db_settings_stub.SessionLocal = _TestingSession
_db_settings_stub.Base = _Base
sys.modules["app.db_settings"] = _db_settings_stub

# ── 4. App imports (after env vars, mocks, and db_settings stub are ready) ─────
import pytest
from fastapi.testclient import TestClient
from passlib.context import CryptContext

from app.main import app
from app.auth import get_db, get_password_hash
from app import auth as _auth_module
from app import db_models

Base = _Base  # models registered their tables on this Base via the stub

# ── 5. Speed up bcrypt for tests ───────────────────────────────────────────────
# Default rounds=12 makes each hash ~1s in constrained environments.
# rounds=4 (minimum) reduces it to ~10ms while keeping the same code path.
_auth_module.pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=4
)


def _override_get_db():
    db = _TestingSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = _override_get_db

# ── 6. Replace startup handler ─────────────────────────────────────────────────
# Clear ALL existing handlers so the original startup_event (which calls
# Base.metadata.create_all with the real MySQL engine) never runs.
# db_session fixture handles table creation explicitly, so no startup needed.
app.router.on_startup.clear()
app.router.on_shutdown.clear()


# ── 7. Fixtures ────────────────────────────────────────────────────────────────
@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=_test_engine)
    db = _TestingSession()
    db.add(db_models.User(
        username="alice",
        email="alice@example.com",
        full_name="Alice",
        hashed_password=get_password_hash("alice123"),
        is_active=True,
        is_superuser=False,
    ))
    db.add(db_models.User(
        username="inactive_user",
        email="inactive@example.com",
        full_name="Inactive",
        hashed_password=get_password_hash("inactive123"),
        is_active=False,
        is_superuser=False,
    ))
    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=_test_engine)


@pytest.fixture
def client(db_session):
    with TestClient(app) as c:
        yield c
