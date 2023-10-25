from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .llm_agent import prompt_leaking_lv1, p2sql_injection_lv1, p2sql_injection_lv2
from .db_settings import Base, engine

# Application.
app = FastAPI()

# Create tables.
Base.metadata.create_all(bind=engine)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    text: str = Field(title="Request message to LLM.", max_length=1000)


class LLMResponse(BaseModel):
    text: str


@app.get("/healthcheck")
def healthcheck():
    return {}


@app.post("/prompt-leaking-lv1")
async def api_prompt_leaking_lv1(message: Message) -> LLMResponse:
    try:
        answer = prompt_leaking_lv1(message.text)
        return LLMResponse(text=answer)
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")


@app.post("/p2sql-injection-lv1")
async def api_p2sql_injection_lv1(message: Message) -> LLMResponse:
    try:
        answer = p2sql_injection_lv1(message.text)
        return LLMResponse(text=answer)
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")


@app.post("/p2sql-injection-lv2")
async def api_p2sql_injection_lv2(message: Message) -> LLMResponse:
    try:
        answer = p2sql_injection_lv2(message.text)
        return LLMResponse(text=answer)
    except Exception as e:
        return LLMResponse(text=f"Error: {', '.join(map(str, e.args))}")
