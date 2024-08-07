from fastapi import FastAPI, Depends
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


@app.post("/prompt-leaking-lv1")
async def api_prompt_leaking_lv1(message: Message = Depends(input_filter)) -> LLMResponse:
    try:
        answer = prompt_leaking_lv1(message.text)
        return LLMResponse(text=output_filter(answer))
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")


@app.post("/p2sql-injection-lv1")
async def api_p2sql_injection_lv1(message: Message = Depends(input_filter)) -> LLMResponse:
    try:
        answer = p2sql_injection_lv1(message.text)
        return LLMResponse(text=output_filter(answer))
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")


@app.post("/p2sql-injection-lv2")
async def api_p2sql_injection_lv2(message: Message = Depends(input_filter)) -> LLMResponse:
    try:
        answer = p2sql_injection_lv2(message.text)
        return LLMResponse(text=output_filter(answer))
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")


@app.post("/llm4shell-lv1")
async def api_llm4shell_lv1(message: Message = Depends(input_filter)) -> LLMResponse:
    try:
        answer = llm4shell_lv1(message.text)
        return LLMResponse(text=output_filter(answer))
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")


@app.post("/llm4shell-lv2")
async def api_llm4shell_lv2(message: Message = Depends(input_filter)) -> LLMResponse:
    try:
        answer = llm4shell_lv2(message.text)
        return LLMResponse(text=output_filter(answer))
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")
