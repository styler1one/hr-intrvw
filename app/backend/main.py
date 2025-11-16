from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import uuid

from interview_agent import InterviewAgent
from session_manager import SessionManager

# Load environment variables
load_dotenv()

app = FastAPI(title="Volentis Interview Agent API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session manager
session_manager = SessionManager()

@app.get("/")
async def root():
    return {
        "message": "Volentis Interview Agent API",
        "version": "1.0.0",
        "status": "running"
    }

@app.post("/api/session/start")
async def start_session():
    """Start a new interview session"""
    session_id = str(uuid.uuid4())
    session_manager.create_session(session_id)
    
    return {
        "session_id": session_id,
        "message": "Session created successfully"
    }

@app.websocket("/ws/interview/{session_id}")
async def interview_websocket(websocket: WebSocket, session_id: str):
    await websocket.accept()
    
    # Get or create session
    session = session_manager.get_session(session_id)
    if not session:
        await websocket.send_json({
            "type": "error",
            "message": "Invalid session ID"
        })
        await websocket.close()
        return
    
    # Initialize interview agent with configured provider
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    
    # Get appropriate API key based on provider
    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
    elif provider == "anthropic":
        api_key = os.getenv("ANTHROPIC_API_KEY")
    elif provider == "windsurf":
        api_key = os.getenv("WINDSURF_API_KEY")
    else:
        api_key = os.getenv("OPENAI_API_KEY")  # fallback
    
    agent = InterviewAgent(
        provider=provider,
        api_key=api_key,
        model=os.getenv("LLM_MODEL", "gpt-4-turbo"),
        api_base=os.getenv("WINDSURF_API_BASE") if provider == "windsurf" else None
    )
    
    # Send welcome message only for new sessions (no messages yet)
    if len(session["messages"]) == 0:
        await websocket.send_json({
            "type": "agent_message",
            "content": """Welkom! Ik ben de Volentis HR Implementation Interview Agent.

Ik ga je helpen om:
✅ Een compleet implementatieplan voor de Volentis HR Agent te maken
✅ Een HR-verbeter-roadmap op te stellen

Dit interview duurt ongeveer 45-60 minuten en bestaat uit 11 fases.
Je kunt op elk moment pauzeren en later verder gaan.

Laten we beginnen!

**Vraag 1:** In wat voor organisatie werk je? (sector, grootte, landen)""",
            "progress": 0,
            "fase": 1,
            "fase_name": "Intro & context"
        })
    
    try:
        while True:
            # Receive user message
            data = await websocket.receive_json()
            user_message = data.get("content", "")
            
            if not user_message:
                continue
            
            # Add to session
            session["messages"].append({
                "role": "user",
                "content": user_message,
                "timestamp": datetime.now().isoformat()
            })
            
            # Get agent response
            print(f"Processing message for session {session_id}, fase {session['current_fase']}")
            try:
                response = await agent.process_message(
                    messages=session["messages"],
                    current_fase=session["current_fase"]
                )
                print(f"Response received: {len(response.get('content', ''))} chars")
            except Exception as e:
                print(f"Error in process_message: {e}")
                import traceback
                traceback.print_exc()
                raise
            
            # Add agent response to session
            session["messages"].append({
                "role": "assistant",
                "content": response["content"],
                "timestamp": datetime.now().isoformat()
            })
            
            # Check if fase is complete
            if response.get("fase_complete"):
                # Save partial JSON
                session["partial_data"][f"fase_{session['current_fase']}"] = response["partial_json"]
                session["current_fase"] += 1
                
                # Check if interview is complete
                if session["current_fase"] > 11:
                    session["status"] = "completed"
                    
                    # Send completion message
                    await websocket.send_json({
                        "type": "interview_complete",
                        "message": "Interview voltooid! Je documenten worden nu gegenereerd...",
                        "progress": 100
                    })
                    
                    # TODO: Trigger plan & roadmap generation
                    break
            
            # Calculate progress
            progress = (session["current_fase"] / 11) * 100
            
            # Send response
            await websocket.send_json({
                "type": "agent_message",
                "content": response["content"],
                "progress": progress,
                "fase": session["current_fase"],
                "fase_name": response.get("fase_name", "")
            })
            
    except WebSocketDisconnect:
        print(f"Client disconnected: {session_id}")
    except Exception as e:
        import traceback
        print(f"Error in websocket: {e}")
        traceback.print_exc()
        try:
            await websocket.send_json({
                "type": "error",
                "message": str(e)
            })
        except:
            pass
    finally:
        # Save session
        session_manager.save_session(session_id, session)

@app.get("/api/session/{session_id}")
async def get_session(session_id: str):
    """Get session data"""
    session = session_manager.get_session(session_id)
    if not session:
        return {"error": "Session not found"}
    
    return {
        "session_id": session_id,
        "status": session["status"],
        "current_fase": session["current_fase"],
        "progress": (session["current_fase"] / 11) * 100,
        "created_at": session["created_at"]
    }

@app.get("/api/session/{session_id}/export")
async def export_session(session_id: str):
    """Export complete session data for next agents"""
    session = session_manager.get_session(session_id)
    if not session:
        return {"error": "Session not found"}
    
    # Combine all partial data into one complete dataset
    complete_data = {
        "session_id": session_id,
        "created_at": session["created_at"],
        "completed_at": session["updated_at"],
        "status": session["status"],
        "interview_data": session["partial_data"],
        "conversation_history": session["messages"]
    }
    
    return complete_data

@app.post("/api/session/{session_id}/suggestions")
async def generate_suggestions(session_id: str, data: dict):
    """Generate AI suggestions based on current question and conversation context"""
    session = session_manager.get_session(session_id)
    if not session:
        return {"error": "Session not found"}
    
    current_question = data.get("question", "")
    
    # Initialize agent
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
    elif provider == "anthropic":
        api_key = os.getenv("ANTHROPIC_API_KEY")
    elif provider == "windsurf":
        api_key = os.getenv("WINDSURF_API_KEY")
    else:
        api_key = os.getenv("OPENAI_API_KEY")
    
    agent = InterviewAgent(
        provider=provider,
        api_key=api_key,
        model=os.getenv("LLM_MODEL", "gpt-4-turbo"),
        api_base=os.getenv("WINDSURF_API_BASE") if provider == "windsurf" else None
    )
    
    # Generate suggestions using LLM
    try:
        suggestions = await agent.generate_suggestions(
            messages=session["messages"],
            current_question=current_question
        )
        return {"suggestions": suggestions}
    except Exception as e:
        print(f"Error generating suggestions: {e}")
        # Fallback to generic suggestions
        return {
            "suggestions": [
                "Ja, dat klopt",
                "Nee, nog niet",
                "Deels, laat me toelichten",
                "Weet ik niet zeker"
            ]
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
