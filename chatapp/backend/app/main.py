from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import Message, LLMResponse
from .llm_agent import *
from .db_settings import Base, engine
from . import db_models
from .filters import input_filter, output_filter

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
    # Create tables.
    Base.metadata.create_all(bind=engine)


@app.get("/healthcheck")
def healthcheck():
    return {}


# This level is no guard.
@app.post("/prompt-leaking-lv1")
async def api_prompt_leaking_lv1(message: Message) -> LLMResponse:
    try:
        answer = prompt_leaking_lv1(message.text)
        return LLMResponse(text=answer)
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")


# This level is implemented input/output filters.
@app.post("/prompt-leaking-lv2")
async def api_prompt_leaking_lv2(message: Message) -> LLMResponse:
    try:
        validated_message = input_filter(message)
        answer = prompt_leaking_lv2(validated_message.text)
        final_answer = output_filter(answer)
        return LLMResponse(text=final_answer)
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")


# This level is implemented prompt hardener.
@app.post("/prompt-leaking-lv3")
async def api_prompt_leaking_lv3(message: Message) -> LLMResponse:
    try:
        answer = prompt_leaking_lv3(message.text)
        return LLMResponse(text=answer)
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")


# This level is implemented NeMo-Guardrails.
@app.post("/prompt-leaking-lv4")
async def api_prompt_leaking_lv4(message: Message) -> LLMResponse:
    try:
        answer = await prompt_leaking_lv4(message.text)
        return LLMResponse(text=answer)
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")


# This level is no guard.
@app.post("/p2sql-injection-lv1")
async def api_p2sql_injection_lv1(message: Message) -> LLMResponse:
    try:
        answer = p2sql_injection_lv1(message.text)
        return LLMResponse(text=answer)
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")


# This level is implemented input/output filters.
@app.post("/p2sql-injection-lv2")
async def api_p2sql_injection_lv2(message: Message) -> LLMResponse:
    try:
        validated_message = input_filter(message)
        answer = p2sql_injection_lv2(validated_message.text)
        final_answer = output_filter(answer)
        return LLMResponse(text=final_answer)
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")


# This level is implemented defensive prompt template.
@app.post("/p2sql-injection-lv3")
async def api_p2sql_injection_lv3(message: Message) -> LLMResponse:
    try:
        answer = p2sql_injection_lv3(message.text)
        return LLMResponse(text=answer)
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")


# This level is implemented prompt hardener.
@app.post("/p2sql-injection-lv4")
async def api_p2sql_injection_lv4(message: Message) -> LLMResponse:
    try:
        answer = p2sql_injection_lv4(message.text)
        return LLMResponse(text=answer)
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")


# This level is implemented LLM-as-a-Judge.
@app.post("/p2sql-injection-lv5")
async def api_p2sql_injection_lv5(message: Message) -> LLMResponse:
    try:
        answer = p2sql_injection_lv5(message.text)
        return LLMResponse(text=answer)
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")


# This level is no guard.
@app.post("/llm4shell-lv1")
async def api_llm4shell_lv1(message: Message) -> LLMResponse:
    try:
        answer = llm4shell_lv1(message.text)
        return LLMResponse(text=answer)
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")


# This level is implemented input/output filters.
@app.post("/llm4shell-lv2")
async def api_llm4shell_lv2(message: Message) -> LLMResponse:
    try:
        validated_message = input_filter(message)
        answer = llm4shell_lv2(validated_message.text)
        final_answer = output_filter(answer)
        return LLMResponse(text=final_answer)
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")


# This level is implemented prompt hardener.
@app.post("/llm4shell-lv3")
async def api_llm4shell_lv3(message: Message) -> LLMResponse:
    try:
        answer = llm4shell_lv3(message.text)
        return LLMResponse(text=answer)
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")


# This level is implemented LLM-as-a-Judge.
@app.post("/llm4shell-lv4")
async def api_llm4shell_lv4(message: Message) -> LLMResponse:
    try:
        answer = llm4shell_lv4(message.text)
        return LLMResponse(text=answer)
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")
