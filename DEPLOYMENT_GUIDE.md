# Volentis Interview Agent Suite - Deployment Guide

## 🎯 Doel
Deze guide helpt je om de Volentis Interview Agent Suite live te zetten voor eindgebruikers.

---

## 📋 Pre-Deployment Checklist

### 1. Technische Requirements

**Backend/Platform:**
- [ ] LLM API toegang (OpenAI, Anthropic, of andere)
- [ ] Database voor state management (PostgreSQL, MongoDB, of andere)
- [ ] Backend framework (Node.js, Python FastAPI, of andere)
- [ ] Session management systeem
- [ ] JSON validation library

**Frontend:**
- [ ] Chat interface (React, Vue, of andere)
- [ ] Progress bar component
- [ ] File upload functionaliteit (voor documenten)
- [ ] Export functionaliteit (PDF/Word voor plannen)

**Infrastructure:**
- [ ] Hosting environment (AWS, Azure, GCP, of andere)
- [ ] SSL certificaat voor HTTPS
- [ ] Backup strategie
- [ ] Monitoring & logging

---

## 🏗️ Architectuur Overzicht

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                              │
│  - Chat Interface                                            │
│  - Progress Tracking                                         │
│  - Document Upload                                           │
│  - Export Functionaliteit                                    │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTPS/WebSocket
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR                              │
│  - Session Management                                        │
│  - Agent Routing                                             │
│  - State Management                                          │
│  - Validation Pipeline                                       │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│Interview │  │   Plan   │  │ Roadmap  │
│  Agent   │  │  Agent   │  │  Agent   │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │
     └─────────────┼─────────────┘
                   ▼
         ┌──────────────────┐
         │   LLM API        │
         │ (GPT-4, Claude)  │
         └──────────────────┘
                   │
                   ▼
         ┌──────────────────┐
         │    DATABASE      │
         │ - Sessions       │
         │ - Partial JSON   │
         │ - Final Output   │
         └──────────────────┘
```

---

## 🔧 Implementatie Stappen

### STAP 1: Backend Setup

**1.1 Orchestrator Implementeren**

Maak een orchestrator die:
- Sessions beheert (user_id, session_id, timestamp)
- Agent routing doet (welke agent wanneer)
- State opslaat (partial JSON per fase)
- Validatie uitvoert (JSON schema checks)

**Voorbeeld (Python/FastAPI):**

```python
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
import json

app = FastAPI()

class InterviewSession:
    def __init__(self, session_id, user_id):
        self.session_id = session_id
        self.user_id = user_id
        self.current_fase = 1
        self.partial_data = {}
        self.messages = []
        
    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})
        
    def save_partial_json(self, fase, data):
        self.partial_data[f"fase_{fase}"] = data
        
    def get_full_json(self):
        # Merge all partial JSONs
        merged = {}
        for fase_data in self.partial_data.values():
            merged.update(fase_data.get("fields", {}))
        return merged

@app.websocket("/ws/interview/{session_id}")
async def interview_websocket(websocket: WebSocket, session_id: str):
    await websocket.accept()
    session = InterviewSession(session_id, user_id="current_user")
    
    # Send initial message
    await websocket.send_json({
        "type": "agent_message",
        "content": "Welkom! Ik ben de Volentis HR Implementation Interview Agent...",
        "progress": 0
    })
    
    while True:
        # Receive user message
        data = await websocket.receive_json()
        user_message = data["message"]
        
        # Add to session
        session.add_message("user", user_message)
        
        # Call Interview Agent
        agent_response = await call_interview_agent(
            session.messages,
            session.current_fase
        )
        
        # Check if fase complete
        if agent_response.get("fase_complete"):
            # Extract and validate partial JSON
            partial_json = agent_response.get("partial_json")
            if validate_partial_json(partial_json, session.current_fase):
                session.save_partial_json(session.current_fase, partial_json)
                session.current_fase += 1
            else:
                # Retry with error feedback
                await websocket.send_json({
                    "type": "validation_error",
                    "error": "Data incomplete, asking follow-up..."
                })
        
        # Send agent response
        await websocket.send_json({
            "type": "agent_message",
            "content": agent_response["content"],
            "progress": (session.current_fase / 11) * 100
        })
        
        # Check if interview complete
        if session.current_fase > 11:
            # Trigger Plan & Roadmap agents
            full_json = session.get_full_json()
            await generate_outputs(session_id, full_json)
            break
```

**1.2 LLM Integration**

```python
import openai  # of anthropic

async def call_interview_agent(messages, current_fase):
    # Load system prompt + fase-specific instructions
    system_prompt = load_system_prompt()
    fase_instructions = load_fase_instructions(current_fase)
    
    # Construct prompt
    full_prompt = f"{system_prompt}\n\n{fase_instructions}"
    
    # Call LLM
    response = await openai.ChatCompletion.acreate(
        model="gpt-4-turbo",  # of gpt-4o, claude-3-opus
        messages=[
            {"role": "system", "content": full_prompt},
            *messages
        ],
        temperature=0.7,
        max_tokens=2000
    )
    
    # Parse response
    agent_message = response.choices[0].message.content
    
    # Check for JSON output (fase complete)
    partial_json = extract_json_from_response(agent_message)
    
    return {
        "content": agent_message,
        "fase_complete": partial_json is not None,
        "partial_json": partial_json
    }
```

**1.3 Validation Pipeline**

```python
from jsonschema import validate, ValidationError

def validate_partial_json(data, fase):
    schema = load_fase_schema(fase)
    try:
        validate(instance=data, schema=schema)
        return True
    except ValidationError as e:
        print(f"Validation error: {e}")
        return False

def load_fase_schema(fase):
    # Load JSON schema per fase
    schemas = {
        1: {
            "type": "object",
            "required": ["org_profile", "hr_team_profile"],
            "properties": {
                "org_profile": {"type": "object"},
                "hr_team_profile": {"type": "object"}
            }
        },
        # ... schemas voor andere fases
    }
    return schemas.get(fase, {})
```

---

### STAP 2: Frontend Setup

**2.1 Chat Interface**

```jsx
// React example
import React, { useState, useEffect } from 'react';
import { useWebSocket } from 'react-use-websocket';

function InterviewChat({ sessionId }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [progress, setProgress] = useState(0);
  
  const { sendJsonMessage, lastJsonMessage } = useWebSocket(
    `wss://your-domain.com/ws/interview/${sessionId}`
  );
  
  useEffect(() => {
    if (lastJsonMessage) {
      if (lastJsonMessage.type === 'agent_message') {
        setMessages(prev => [...prev, {
          role: 'agent',
          content: lastJsonMessage.content
        }]);
        setProgress(lastJsonMessage.progress);
      }
    }
  }, [lastJsonMessage]);
  
  const handleSend = () => {
    setMessages(prev => [...prev, { role: 'user', content: input }]);
    sendJsonMessage({ message: input });
    setInput('');
  };
  
  return (
    <div className="interview-container">
      <div className="progress-bar">
        <div className="progress-fill" style={{ width: `${progress}%` }}>
          {Math.round(progress)}%
        </div>
      </div>
      
      <div className="messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            {msg.content}
          </div>
        ))}
      </div>
      
      <div className="input-area">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Type je antwoord..."
        />
        <button onClick={handleSend}>Verstuur</button>
      </div>
    </div>
  );
}
```

**2.2 Progress Tracking Component**

```jsx
function ProgressTracker({ currentFase, totalFases }) {
  const fases = [
    "Intro & context",
    "Stakeholders",
    "HR-service",
    "Processen",
    "Systemen",
    "Documentatie",
    "Change readiness",
    "Doelen & KPI's",
    "Compliance",
    "Verbeterkansen",
    "Samenvatting"
  ];
  
  return (
    <div className="progress-tracker">
      {fases.map((fase, idx) => (
        <div 
          key={idx}
          className={`fase-step ${idx + 1 === currentFase ? 'active' : ''} ${idx + 1 < currentFase ? 'completed' : ''}`}
        >
          <div className="fase-number">{idx + 1}</div>
          <div className="fase-name">{fase}</div>
        </div>
      ))}
    </div>
  );
}
```

---

### STAP 3: Plan & Roadmap Generation

**3.1 Trigger na Interview**

```python
async def generate_outputs(session_id, interview_data):
    # Parallel generation
    plan_task = asyncio.create_task(generate_plan(interview_data))
    roadmap_task = asyncio.create_task(generate_roadmap(interview_data))
    
    plan, roadmap = await asyncio.gather(plan_task, roadmap_task)
    
    # Save to database
    save_outputs(session_id, plan, roadmap)
    
    # Notify user
    await notify_user(session_id, "Documenten zijn klaar!")

async def generate_plan(interview_data):
    system_prompt = load_plan_agent_prompt()
    
    response = await openai.ChatCompletion.acreate(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Genereer implementatieplan op basis van:\n\n{json.dumps(interview_data, indent=2)}"}
        ],
        temperature=0.7,
        max_tokens=8000
    )
    
    return response.choices[0].message.content

async def generate_roadmap(interview_data):
    # Similar to generate_plan
    pass
```

**3.2 Export Functionaliteit**

```python
from docx import Document
from markdown import markdown
import pdfkit

@app.get("/export/{session_id}/{doc_type}")
async def export_document(session_id: str, doc_type: str, format: str = "pdf"):
    # Load document (plan or roadmap)
    doc_content = load_document(session_id, doc_type)
    
    if format == "pdf":
        # Convert markdown to PDF
        html = markdown(doc_content)
        pdf = pdfkit.from_string(html, False)
        return Response(content=pdf, media_type="application/pdf")
    
    elif format == "docx":
        # Convert to Word
        doc = Document()
        # Add content...
        return doc
```

---

### STAP 4: Database Schema

```sql
-- Sessions table
CREATE TABLE interview_sessions (
    session_id UUID PRIMARY KEY,
    user_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    current_fase INT DEFAULT 1,
    status VARCHAR(50) DEFAULT 'in_progress',
    completeness_score INT,
    overall_confidence VARCHAR(20)
);

-- Partial data per fase
CREATE TABLE fase_data (
    id SERIAL PRIMARY KEY,
    session_id UUID REFERENCES interview_sessions(session_id),
    fase_number INT,
    data JSONB,
    confidence VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Messages
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    session_id UUID REFERENCES interview_sessions(session_id),
    role VARCHAR(20),
    content TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Generated documents
CREATE TABLE generated_documents (
    id SERIAL PRIMARY KEY,
    session_id UUID REFERENCES interview_sessions(session_id),
    doc_type VARCHAR(50), -- 'plan' or 'roadmap'
    content TEXT,
    format VARCHAR(20), -- 'markdown', 'html', 'pdf'
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

### STAP 5: Configuratie & Secrets

**5.1 Environment Variables**

```bash
# .env file
LLM_API_KEY=sk-...
LLM_MODEL=gpt-4-turbo
DATABASE_URL=postgresql://user:pass@localhost:5432/volentis
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key
FRONTEND_URL=https://your-domain.com
MAX_SESSION_DURATION=7200  # 2 hours
```

**5.2 Config Files**

Plaats de agent configs in je backend:
```
/config
  /agents
    - interview_agent_system_prompt.txt
    - plan_agent_system_prompt.txt
    - roadmap_agent_system_prompt.txt
  /fase_instructions
    - fase_1.txt
    - fase_2.txt
    - ...
  /schemas
    - fase_1_schema.json
    - fase_2_schema.json
    - ...
```

---

### STAP 6: Testing

**6.1 Unit Tests**

```python
import pytest

def test_partial_json_validation():
    data = {
        "fase": 1,
        "fields": {
            "org_profile": {"name": "Test Org", "employee_count": 100}
        }
    }
    assert validate_partial_json(data, 1) == True

def test_session_management():
    session = InterviewSession("test-123", "user-1")
    session.add_message("user", "Test")
    assert len(session.messages) == 1
```

**6.2 Integration Tests**

```python
@pytest.mark.asyncio
async def test_full_interview_flow():
    session_id = "test-session"
    
    # Simulate interview
    responses = [
        "We zijn een IT bedrijf met 200 medewerkers",
        "Ik ben HR Manager",
        # ... meer antwoorden
    ]
    
    for response in responses:
        result = await process_user_message(session_id, response)
        assert result["status"] == "success"
    
    # Check final output
    final_data = get_session_data(session_id)
    assert final_data["completeness_score"] > 80
```

**6.3 End-to-End Test**

Test met echte gebruiker:
- [ ] Volledig interview doorlopen (alle 11 fases)
- [ ] Check partial JSON per fase
- [ ] Check final merged JSON
- [ ] Check gegenereerde plan & roadmap
- [ ] Check export functionaliteit

---

### STAP 7: Deployment

**7.1 Docker Setup**

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/volentis
      - LLM_API_KEY=${LLM_API_KEY}
    depends_on:
      - db
      - redis
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8000
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=volentis
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

**7.2 Deploy naar Cloud**

**Option A: AWS**
```bash
# Deploy to AWS ECS
aws ecs create-cluster --cluster-name volentis-cluster
aws ecs create-service --cluster volentis-cluster --service-name interview-agent
```

**Option B: Vercel (Frontend) + Railway (Backend)**
```bash
# Frontend to Vercel
vercel deploy --prod

# Backend to Railway
railway up
```

**Option C: DigitalOcean App Platform**
```bash
doctl apps create --spec app.yaml
```

---

### STAP 8: Monitoring & Logging

**8.1 Logging Setup**

```python
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

# Log important events
logger.info("Interview started", extra={
    "session_id": session_id,
    "user_id": user_id,
    "timestamp": datetime.now().isoformat()
})
```

**8.2 Monitoring Dashboard**

Gebruik tools zoals:
- **Sentry** voor error tracking
- **Datadog/New Relic** voor performance monitoring
- **Grafana** voor custom dashboards

Key metrics om te tracken:
- Interview completion rate
- Average interview duration
- Fase drop-off rates
- LLM API latency
- Validation failure rate
- User satisfaction (CSAT)

---

### STAP 9: Security

**9.1 Authentication**

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def verify_token(credentials = Depends(security)):
    token = credentials.credentials
    # Verify JWT token
    if not is_valid_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    return get_user_from_token(token)

@app.websocket("/ws/interview/{session_id}")
async def interview_websocket(
    websocket: WebSocket,
    session_id: str,
    user = Depends(verify_token)
):
    # ... interview logic
```

**9.2 Rate Limiting**

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/interview/start")
@limiter.limit("5/minute")
async def start_interview(request: Request):
    # ... logic
```

**9.3 Data Encryption**

- [ ] HTTPS/TLS voor alle communicatie
- [ ] Encrypt sensitive data at rest (database)
- [ ] Encrypt LLM API keys
- [ ] Regular security audits

---

### STAP 10: User Onboarding

**10.1 Landing Page**

```jsx
function LandingPage() {
  return (
    <div className="landing">
      <h1>Volentis HR Agent Implementatie Assistent</h1>
      <p>Beantwoord vragen over je organisatie en ontvang:</p>
      <ul>
        <li>✅ Een compleet implementatieplan</li>
        <li>✅ Een HR-verbeter-roadmap</li>
        <li>✅ Geprioriteerde quick wins</li>
      </ul>
      <p><strong>Tijdsduur:</strong> 45-60 minuten</p>
      <button onClick={startInterview}>Start Interview</button>
    </div>
  );
}
```

**10.2 Tutorial/Help**

- [ ] Intro video (2-3 min)
- [ ] Tooltips bij complexe vragen
- [ ] "Waarom vragen we dit?" uitleg per fase
- [ ] Voorbeeld antwoorden
- [ ] FAQ sectie

---

## 🚀 Go-Live Checklist

### Pre-Launch
- [ ] Alle unit tests passed
- [ ] Integration tests passed
- [ ] End-to-end test succesvol
- [ ] Security audit gedaan
- [ ] Performance test gedaan (10+ concurrent users)
- [ ] Backup strategie getest
- [ ] Monitoring dashboard live
- [ ] Error alerting geconfigureerd
- [ ] Documentation compleet

### Launch Day
- [ ] Deploy naar productie
- [ ] Smoke tests op productie
- [ ] Monitor eerste sessies closely
- [ ] Support team standby
- [ ] Rollback plan klaar

### Post-Launch (Week 1)
- [ ] Dagelijkse monitoring
- [ ] User feedback verzamelen
- [ ] Bug fixes prioriteren
- [ ] Performance optimalisaties
- [ ] Documentation updates

---

## 📊 Success Metrics

Track deze metrics na launch:

| Metric | Target | Actual |
|--------|--------|--------|
| Interview completion rate | >80% | - |
| Average duration | 45-60 min | - |
| User satisfaction (CSAT) | >8/10 | - |
| Plan quality score | >85% | - |
| System uptime | >99.5% | - |
| API response time | <2s | - |

---

## 🆘 Troubleshooting

### Probleem: Interview hangt bij bepaalde fase
**Oplossing:** Check LLM API rate limits, verhoog timeout, check fase-instructies

### Probleem: Validation fails vaak
**Oplossing:** Relax JSON schema, verbeter retry logic, geef betere feedback aan agent

### Probleem: Lage completion rate
**Oplossing:** Verkort interview, maak vragen optioneel, voeg save/resume functie toe

### Probleem: Slechte plan kwaliteit
**Oplossing:** Verbeter system prompts, gebruik betere LLM model, voeg human review stap toe

---

## 📞 Support & Maintenance

**Support kanalen:**
- Email: support@volentis.ai
- Chat: In-app support chat
- Documentation: docs.volentis.ai

**Maintenance schema:**
- **Dagelijks:** Monitor logs, check error rates
- **Wekelijks:** Review user feedback, update prompts
- **Maandelijks:** Performance review, cost optimization
- **Kwartaal:** Major updates, new features

---

## 🎓 Training voor Support Team

**Support team moet weten:**
1. Hoe het interview proces werkt (11 fases)
2. Wat elke fase vraagt en waarom
3. Hoe validation werkt
4. Hoe plan/roadmap gegenereerd worden
5. Common issues en oplossingen
6. Hoe data te exporteren/delen
7. Privacy & security protocols

**Training materiaal:**
- Deze deployment guide
- Agent config files
- Demo video's
- FAQ document
- Troubleshooting playbook

---

Succes met de deployment! 🚀
