"""
Shared configuration for API endpoints
"""

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
