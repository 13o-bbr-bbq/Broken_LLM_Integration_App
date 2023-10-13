from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .llm_agent import llm_controller
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


@app.post("/chat")
async def run_llm(message: Message) -> LLMResponse:
    try:
        answer = llm_controller(message.text)
        return LLMResponse(text=answer)
    except Exception as e:
        return LLMResponse(text=f"Error: {str(e)}")
