from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .models import Message, LLMResponse, LoginRequest, Token, UserResponse
from .llm_agent import *
from .db_settings import Base, engine
from . import db_models
from .filters import input_filter, output_filter
from .auth import (
    get_db,
    authenticate_user,
    create_access_token,
    get_current_active_user,
)
from .settings import settings

# Application.
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)


# ── Auth ──────────────────────────────────────────────────────────────────────

@app.get("/healthcheck")
def healthcheck():
    return {}


@app.post("/auth/login", response_model=Token)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/auth/me", response_model=UserResponse)
def read_me(current_user: db_models.User = Depends(get_current_active_user)):
    return current_user


# ── Prompt Leaking ────────────────────────────────────────────────────────────

# This level is no guard.
@app.post("/prompt-leaking-lv1")
async def api_prompt_leaking_lv1(
    message: Message,
    _: db_models.User = Depends(get_current_active_user),
) -> LLMResponse:
    try:
        answer = prompt_leaking_lv1(message.text)
        return LLMResponse(text=answer)
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")


# This level is implemented input/output filters.
@app.post("/prompt-leaking-lv2")
async def api_prompt_leaking_lv2(
    message: Message,
    _: db_models.User = Depends(get_current_active_user),
) -> LLMResponse:
    try:
        validated_message = input_filter(message)
        answer = prompt_leaking_lv2(validated_message.text)
        final_answer = output_filter(answer)
        return LLMResponse(text=final_answer)
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")


# This level is implemented prompt hardener.
@app.post("/prompt-leaking-lv3")
async def api_prompt_leaking_lv3(
    message: Message,
    _: db_models.User = Depends(get_current_active_user),
) -> LLMResponse:
    try:
        answer = prompt_leaking_lv3(message.text)
        return LLMResponse(text=answer)
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")


# This level is implemented NeMo-Guardrails.
@app.post("/prompt-leaking-lv4")
async def api_prompt_leaking_lv4(
    message: Message,
    _: db_models.User = Depends(get_current_active_user),
) -> LLMResponse:
    try:
        answer = await prompt_leaking_lv4(message.text)
        return LLMResponse(text=answer)
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")


# This level is implemented DeepKeep.
@app.post("/prompt-leaking-lv5")
async def api_prompt_leaking_lv5(
    message: Message,
    _: db_models.User = Depends(get_current_active_user),
) -> LLMResponse:
    try:
        answer = await prompt_leaking_lv5(message.text)
        return LLMResponse(text=answer)
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")


# ── Indirect Prompt Injection ─────────────────────────────────────────────────

# This level is no guard.
@app.post("/indirect-pi-lv1")
async def api_indirect_pi_lv1(
    message: Message,
    _: db_models.User = Depends(get_current_active_user),
) -> LLMResponse:
    try:
        answer = indirect_pi_lv1(message.text)
        return LLMResponse(text=answer)
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")


# ── Prompt-to-SQL Injection ───────────────────────────────────────────────────

# This level is no guard.
@app.post("/p2sql-injection-lv1")
async def api_p2sql_injection_lv1(
    message: Message,
    _: db_models.User = Depends(get_current_active_user),
) -> LLMResponse:
    try:
        answer = p2sql_injection_lv1(message.text)
        return LLMResponse(text=answer)
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")


# This level is implemented input/output filters.
@app.post("/p2sql-injection-lv2")
async def api_p2sql_injection_lv2(
    message: Message,
    _: db_models.User = Depends(get_current_active_user),
) -> LLMResponse:
    try:
        validated_message = input_filter(message)
        answer = p2sql_injection_lv2(validated_message.text)
        final_answer = output_filter(answer)
        return LLMResponse(text=final_answer)
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")


# This level is implemented defensive prompt template.
@app.post("/p2sql-injection-lv3")
async def api_p2sql_injection_lv3(
    message: Message,
    _: db_models.User = Depends(get_current_active_user),
) -> LLMResponse:
    try:
        answer = p2sql_injection_lv3(message.text)
        return LLMResponse(text=answer)
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")


# This level is implemented prompt hardener.
@app.post("/p2sql-injection-lv4")
async def api_p2sql_injection_lv4(
    message: Message,
    _: db_models.User = Depends(get_current_active_user),
) -> LLMResponse:
    try:
        answer = p2sql_injection_lv4(message.text)
        return LLMResponse(text=answer)
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")


# This level is implemented LLM-as-a-Judge.
@app.post("/p2sql-injection-lv5")
async def api_p2sql_injection_lv5(
    message: Message,
    _: db_models.User = Depends(get_current_active_user),
) -> LLMResponse:
    try:
        answer = p2sql_injection_lv5(message.text)
        return LLMResponse(text=answer)
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")


# ── LLM4Shell ────────────────────────────────────────────────────────────────

# This level is no guard.
@app.post("/llm4shell-lv1")
async def api_llm4shell_lv1(
    message: Message,
    _: db_models.User = Depends(get_current_active_user),
) -> LLMResponse:
    try:
        answer = llm4shell_lv1(message.text)
        return LLMResponse(text=answer)
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")


# This level is implemented input/output filters.
@app.post("/llm4shell-lv2")
async def api_llm4shell_lv2(
    message: Message,
    _: db_models.User = Depends(get_current_active_user),
) -> LLMResponse:
    try:
        validated_message = input_filter(message)
        answer = llm4shell_lv2(validated_message.text)
        final_answer = output_filter(answer)
        return LLMResponse(text=final_answer)
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")


# This level is implemented prompt hardener.
@app.post("/llm4shell-lv3")
async def api_llm4shell_lv3(
    message: Message,
    _: db_models.User = Depends(get_current_active_user),
) -> LLMResponse:
    try:
        answer = llm4shell_lv3(message.text)
        return LLMResponse(text=answer)
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")


# This level is implemented LLM-as-a-Judge.
@app.post("/llm4shell-lv4")
async def api_llm4shell_lv4(
    message: Message,
    _: db_models.User = Depends(get_current_active_user),
) -> LLMResponse:
    try:
        answer = llm4shell_lv4(message.text)
        return LLMResponse(text=answer)
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")
