"""
Storage layer for Vercel deployment
Uses environment variable to determine storage backend
"""
import json
import os
from datetime import datetime
from typing import Optional, Dict

class SessionStorage:
    """Abstract base class for session storage"""
    
    def create_session(self, session_id: str, template_id: str = "standard") -> dict:
        """Create a new session"""
        raise NotImplementedError
    
    def get_session(self, session_id: str) -> Optional[dict]:
        """Get session by ID"""
        raise NotImplementedError
    
    def update_session(self, session_id: str, session_data: dict) -> None:
        """Update session data"""
        raise NotImplementedError
    
    def delete_session(self, session_id: str) -> None:
        """Delete a session"""
        raise NotImplementedError


class MemoryStorage(SessionStorage):
    """In-memory storage for development/testing"""
    
    def __init__(self):
        self.sessions = {}
    
    def create_session(self, session_id: str, template_id: str = "standard") -> dict:
        from templates import get_template
        template = get_template(template_id)
        
        session = {
            "session_id": session_id,
            "template_id": template_id,
            "template_name": template["name"],
            "total_fases": template["total_fases"],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "status": "in_progress",
            "current_fase": 1,
            "messages": [],
            "partial_data": {}
        }
        self.sessions[session_id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[dict]:
        session = self.sessions.get(session_id)
        if session and "template_id" not in session:
            # Backwards compatibility
            session["template_id"] = "standard"
            session["template_name"] = "Standard Interview"
            session["total_fases"] = 11
        return session
    
    def update_session(self, session_id: str, session_data: dict) -> None:
        session_data["updated_at"] = datetime.now().isoformat()
        self.sessions[session_id] = session_data
    
    def delete_session(self, session_id: str) -> None:
        if session_id in self.sessions:
            del self.sessions[session_id]


# Global storage instance
_storage = None

def get_storage() -> SessionStorage:
    """Get storage instance based on environment"""
    global _storage
    if _storage is None:
        storage_type = os.getenv("STORAGE_TYPE", "memory")
        
        if storage_type == "memory":
            _storage = MemoryStorage()
        else:
            # Default to memory storage
            _storage = MemoryStorage()
    
    return _storage
