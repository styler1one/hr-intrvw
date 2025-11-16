import json
from datetime import datetime
from pathlib import Path

class SessionManager:
    def __init__(self, storage_dir="./sessions"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.sessions = {}
    
    def create_session(self, session_id: str):
        """Create a new session"""
        session = {
            "session_id": session_id,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "status": "in_progress",
            "current_fase": 1,
            "messages": [],
            "partial_data": {}
        }
        self.sessions[session_id] = session
        self.save_session(session_id, session)
        return session
    
    def get_session(self, session_id: str):
        """Get session by ID"""
        if session_id in self.sessions:
            return self.sessions[session_id]
        
        # Try to load from disk
        session_file = self.storage_dir / f"{session_id}.json"
        if session_file.exists():
            with open(session_file, 'r', encoding='utf-8') as f:
                session = json.load(f)
                self.sessions[session_id] = session
                return session
        
        return None
    
    def save_session(self, session_id: str, session: dict):
        """Save session to disk"""
        session["updated_at"] = datetime.now().isoformat()
        self.sessions[session_id] = session
        
        session_file = self.storage_dir / f"{session_id}.json"
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session, f, indent=2, ensure_ascii=False)
    
    def get_all_sessions(self):
        """Get all sessions"""
        return list(self.sessions.values())
