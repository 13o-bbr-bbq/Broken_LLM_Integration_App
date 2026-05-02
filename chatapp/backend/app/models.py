from typing import Optional
from pydantic import BaseModel, Field


class Message(BaseModel):
    text: str = Field(title="Request message to LLM.", max_length=10000)


class LLMResponse(BaseModel):
    text: str


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    is_active: bool

    class Config:
        from_attributes = True
