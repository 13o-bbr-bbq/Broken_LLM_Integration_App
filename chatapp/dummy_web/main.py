from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# Deploy content in "/static"
app.mount("/static", StaticFiles(directory="static"), name="static")

class ContentRequest(BaseModel):
    topic: str

@app.get("/")
async def root():
    return FileResponse("static/index.html")
