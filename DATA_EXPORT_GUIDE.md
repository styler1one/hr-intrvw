# Data Export Guide - Voor Volgende Agents

## 📊 Overzicht

Na het Interview Agent proces is alle verzamelde data beschikbaar voor de volgende agents:
1. **Implementation Plan Agent**
2. **Improvement Roadmap Agent**

## 🗂️ Waar staat de data?

### Locatie op disk:
```
g:\My Drive\_Agentboss\InterviewAgent\app\backend\sessions\{session_id}.json
```

### API Endpoints:

#### 1. Session Info (Summary)
```
GET http://localhost:8000/api/session/{session_id}
```

**Response:**
```json
{
  "session_id": "66763c93-7fb9-4584-b0bd-6e03fd6ac24d",
  "status": "in_progress",
  "current_fase": 2,
  "progress": 18,
  "created_at": "2025-11-15T21:57:20"
}
```

#### 2. Complete Export (Voor volgende agents)
```
GET http://localhost:8000/api/session/{session_id}/export
```

**Response:**
```json
{
  "session_id": "...",
  "created_at": "...",
  "completed_at": "...",
  "status": "completed",
  "interview_data": {
    "fase_1": {
      "org_profile": {...},
      "hr_team_profile": {...},
      "strategic_focus": {...},
      "organizational_culture": {...}
    },
    "fase_2": {
      "stakeholders": {...},
      "change_history": {...},
      "change_readiness_preliminary": {...}
    },
    // ... alle fases
  },
  "conversation_history": [
    {
      "role": "user",
      "content": "...",
      "timestamp": "..."
    },
    {
      "role": "assistant",
      "content": "...",
      "timestamp": "..."
    }
  ]
}
```

## 📋 Data Structuur

### Interview Data (per fase):

**Fase 1 - Intro & Context:**
- `org_profile` - Organisatie details
- `hr_team_profile` - HR team samenstelling
- `strategic_focus` - Strategische doelen
- `organizational_culture` - Cultuur & context

**Fase 2 - Stakeholders:**
- `stakeholders` - Lijst van stakeholders met details
- `change_history` - Recente veranderingen
- `change_readiness_preliminary` - Change readiness score

**Fase 3-11:** (Nog te definiëren in agent config)
- HR Processen
- Systemen & Integraties
- Documentatie
- Doelen & KPI's
- Compliance
- Verbeterkansen
- etc.

## 🔄 Gebruik voor volgende agents:

### Implementation Plan Agent:

```python
import requests

# Haal interview data op
session_id = "66763c93-7fb9-4584-b0bd-6e03fd6ac24d"
response = requests.get(f"http://localhost:8000/api/session/{session_id}/export")
interview_data = response.json()

# Gebruik de data
org_profile = interview_data["interview_data"]["fase_1"]["org_profile"]
stakeholders = interview_data["interview_data"]["fase_2"]["stakeholders"]

# Genereer implementatieplan
implementation_plan = generate_plan(
    organization=org_profile,
    stakeholders=stakeholders,
    # ... etc
)
```

### Improvement Roadmap Agent:

```python
# Haal interview data op
response = requests.get(f"http://localhost:8000/api/session/{session_id}/export")
interview_data = response.json()

# Gebruik de data
pain_points = interview_data["interview_data"]["fase_3"]["pain_points"]
goals = interview_data["interview_data"]["fase_8"]["goals"]

# Genereer roadmap
roadmap = generate_roadmap(
    pain_points=pain_points,
    goals=goals,
    # ... etc
)
```

## 💾 Direct File Access:

Als je direct toegang wilt tot het JSON bestand:

```python
import json
from pathlib import Path

session_id = "66763c93-7fb9-4584-b0bd-6e03fd6ac24d"
session_file = Path(f"./sessions/{session_id}.json")

with open(session_file, 'r', encoding='utf-8') as f:
    session_data = json.load(f)

# Gebruik de data
interview_data = session_data["partial_data"]
messages = session_data["messages"]
```

## 🎯 Volgende Stappen:

1. **Interview Agent** → Verzamelt data en slaat op in sessions/
2. **Export API** → Maakt data beschikbaar via `/export` endpoint
3. **Implementation Plan Agent** → Haalt data op en genereert plan
4. **Improvement Roadmap Agent** → Haalt data op en genereert roadmap

## 📝 Voorbeeld Session ID's:

Na een interview krijg je een session_id terug. Bewaar deze om later de data op te halen:

```javascript
// Frontend - Na interview
const sessionId = "66763c93-7fb9-4584-b0bd-6e03fd6ac24d";
localStorage.setItem('interview_session_id', sessionId);

// Later - Voor volgende agent
const sessionId = localStorage.getItem('interview_session_id');
fetch(`/api/session/${sessionId}/export`)
  .then(res => res.json())
  .then(data => {
    // Stuur naar Implementation Plan Agent
    generateImplementationPlan(data);
  });
```

## 🔐 Security Note:

In productie moet je:
- ✅ Authenticatie toevoegen aan export endpoint
- ✅ Session data encrypten
- ✅ Access control implementeren
- ✅ Audit logging toevoegen
