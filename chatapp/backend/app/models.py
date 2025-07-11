from pydantic import BaseModel, Field


class Message(BaseModel):
    text: str = Field(title="Request message to LLM.", max_length=10000)


class LLMResponse(BaseModel):
    text: str
