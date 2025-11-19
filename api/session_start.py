"""
Session start API endpoint
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
from storage import get_storage
from templates import get_template

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StartSessionRequest(BaseModel):
    template_id: str = "standard"

@app.post("/api/session/start")
async def start_session(request: StartSessionRequest):
    """Start a new interview session with selected template"""
    session_id = str(uuid.uuid4())
    template = get_template(request.template_id)
    
    storage = get_storage()
    session = storage.create_session(session_id, request.template_id)
    
    return {
        "session_id": session_id,
        "template": template,
        "message": "Session created successfully"
    }
