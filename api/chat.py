"""
Chat API endpoint for Vercel deployment (REST-based, no WebSocket)
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from datetime import datetime
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

class ChatMessage(BaseModel):
    content: str

@app.post("/api/session/{session_id}/chat")
async def chat(session_id: str, message: ChatMessage):
    """Process a chat message and return agent response"""
    storage = get_storage()
    session = storage.get_session(session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Add user message to session
    session["messages"].append({
        "role": "user",
        "content": message.content,
        "timestamp": datetime.now().isoformat()
    })
    
    # Initialize agent
    from interview_agent import InterviewAgent
    
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
    elif provider == "anthropic":
        api_key = os.getenv("ANTHROPIC_API_KEY")
    else:
        api_key = os.getenv("OPENAI_API_KEY")
    
    agent = InterviewAgent(
        provider=provider,
        api_key=api_key,
        model=os.getenv("LLM_MODEL", "gpt-4-turbo"),
        template_id=session.get("template_id", "standard")
    )
    
    # Process message
    try:
        response = await agent.process_message(
            messages=session["messages"],
            current_fase=session["current_fase"]
        )
        
        # Add agent response to session
        session["messages"].append({
            "role": "assistant",
            "content": response["content"],
            "timestamp": datetime.now().isoformat()
        })
        
        # Check if fase is complete
        if response.get("fase_complete"):
            session["partial_data"][f"fase_{session['current_fase']}"] = response["partial_json"]
            session["current_fase"] += 1
            
            total_fases = session.get("total_fases", 11)
            if session["current_fase"] > total_fases:
                session["status"] = "completed"
        
        # Calculate progress
        total_fases = session.get("total_fases", 11)
        progress = (session["current_fase"] / total_fases) * 100
        
        # Save session
        storage.update_session(session_id, session)
        
        return {
            "type": "agent_message",
            "content": response["content"],
            "progress": progress,
            "fase": session["current_fase"],
            "fase_name": response.get("fase_name", ""),
            "fase_complete": response.get("fase_complete", False),
            "interview_complete": session["status"] == "completed"
        }
        
    except Exception as e:
        print(f"Error processing message: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/session/{session_id}")
async def get_session(session_id: str):
    """Get session data"""
    storage = get_storage()
    session = storage.get_session(session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    total_fases = session.get("total_fases", 11)
    
    return {
        "session_id": session_id,
        "status": session["status"],
        "current_fase": session["current_fase"],
        "progress": (session["current_fase"] / total_fases) * 100,
        "created_at": session["created_at"],
        "template_id": session.get("template_id", "standard"),
        "template_name": session.get("template_name", "Standard Interview"),
        "total_fases": total_fases
    }

@app.get("/api/session/{session_id}/export")
async def export_session(session_id: str):
    """Export complete session data"""
    storage = get_storage()
    session = storage.get_session(session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "session_id": session_id,
        "status": session["status"],
        "created_at": session["created_at"],
        "conversation_history": session["messages"],
        "collected_data": session["partial_data"],
        "template_id": session.get("template_id", "standard"),
        "template_name": session.get("template_name", "Standard Interview")
    }
