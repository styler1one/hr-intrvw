"""
Shared configuration for API endpoints
"""
import os
import json

# Use environment variable or file-based storage for sessions
# Note: This is a temporary solution - for production use a database
SESSIONS_FILE = '/tmp/sessions.json' if os.path.exists('/tmp') else 'sessions.json'

def load_sessions():
    """Load sessions from file"""
    try:
        if os.path.exists(SESSIONS_FILE):
            with open(SESSIONS_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading sessions: {e}")
    return {}

def save_sessions(sessions):
    """Save sessions to file"""
    try:
        with open(SESSIONS_FILE, 'w') as f:
            json.dump(sessions, f)
    except Exception as e:
        print(f"Error saving sessions: {e}")

# Load existing sessions
SESSIONS = load_sessions()

INTERVIEW_TEMPLATES = {
    "quick": {
        "id": "quick",
        "name": "Quick Interview",
        "description": "Snelle scan van de belangrijkste punten",
        "duration": "20 minuten",
        "total_fases": 5,
        "icon": "⚡",
        "fases": [1, 2, 3, 4, 5],
        "questions_per_fase": "2-3",
        "use_case": "Eerste kennismaking, quick scan, tijdsdruk"
    },
    "standard": {
        "id": "standard",
        "name": "Standard Interview",
        "description": "Volledig interview met alle essentiële onderdelen",
        "duration": "45 minuten",
        "total_fases": 11,
        "icon": "📋",
        "fases": list(range(1, 12)),
        "questions_per_fase": "5-8",
        "use_case": "Standaard implementatie, volledige analyse"
    },
    "extensive": {
        "id": "extensive",
        "name": "Extensive Interview",
        "description": "Diepgaand interview met extra detailvragen",
        "duration": "90 minuten",
        "total_fases": 15,
        "icon": "🔍",
        "fases": list(range(1, 16)),
        "questions_per_fase": "8-12",
        "use_case": "Complexe organisaties, enterprise implementaties"
    }
}

# Simple in-memory storage (sessions will be lost on function restart)
SESSIONS = {}

def get_template(template_id: str) -> dict:
    """Get template by ID"""
    return INTERVIEW_TEMPLATES.get(template_id, INTERVIEW_TEMPLATES["standard"])
