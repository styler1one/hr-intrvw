# Verschillen tussen Lokale en Vercel Versie

## Architectuur Overzicht

### Lokale Versie (`/app`)
```
Frontend (HTML/JS) 
    ↓ WebSocket
Backend (FastAPI)
    ↓
File Storage (./sessions/*.json)
```

### Vercel Versie (`/vercel-deployment`)
```
Frontend (HTML/JS)
    ↓ REST API (polling)
Serverless Functions (FastAPI)
    ↓
In-Memory Storage (kan uitgebreid worden)
```

## Belangrijkste Verschillen

### 1. Communicatie Protocol

**Lokaal: WebSocket**
- Real-time bidirectionele communicatie
- Server kan berichten pushen naar client
- Persistent connection
- Lage latency

**Vercel: REST API + Polling**
- Request/Response pattern
- Client pollt elke 2 seconden voor updates
- Stateless connections
- Iets hogere latency maar goed genoeg

### 2. Session Storage

**Lokaal: File-based**
```python
# session_manager.py
def save_session(self, session_id, session):
    with open(f"./sessions/{session_id}.json", 'w') as f:
        json.dump(session, f)
```

**Vercel: In-Memory**
```python
# storage.py
class MemoryStorage:
    def __init__(self):
        self.sessions = {}  # Lost bij restart!
```

⚠️ **Belangrijk**: Voor productie moet je een database toevoegen (Vercel KV, Postgres, etc.)

### 3. API Endpoints

**Lokaal:**
- `GET /` - Root endpoint
- `POST /api/session/start` - Start sessie
- `WS /ws/interview/{session_id}` - WebSocket verbinding
- `GET /api/session/{session_id}` - Sessie info
- `GET /api/session/{session_id}/export` - Export data

**Vercel:**
- `GET /api` - Root endpoint
- `POST /api/session/start` - Start sessie
- `POST /api/session/{session_id}/chat` - Verstuur bericht (vervangt WebSocket)
- `GET /api/session/{session_id}` - Sessie info
- `GET /api/session/{session_id}/export` - Export data

### 4. File Structuur

**Lokaal:**
```
app/
├── backend/
│   ├── main.py (FastAPI app met WebSocket)
│   ├── interview_agent.py
│   ├── session_manager.py
│   └── templates.py
└── frontend/
    └── index-chatgpt.html
```

**Vercel:**
```
vercel-deployment/
├── api/ (Serverless functions)
│   ├── index.py
│   ├── templates_endpoint.py
│   ├── session_start.py
│   ├── chat.py (vervangt WebSocket)
│   ├── interview_agent.py
│   ├── storage.py (vervangt session_manager)
│   └── templates.py
├── public/
│   ├── index.html
│   └── config.js
├── vercel.json (Vercel configuratie)
├── requirements.txt
└── package.json
```

### 5. Deployment

**Lokaal:**
```bash
# Backend
cd app/backend
python main.py

# Frontend
cd app/frontend
python -m http.server 3000
```

**Vercel:**
```bash
# Alles in één commando
vercel --prod
```

## Feature Pariteit

| Feature | Lokaal | Vercel | Notes |
|---------|--------|--------|-------|
| Template Selectie | ✅ | ✅ | Identiek |
| Chat Interface | ✅ | ✅ | Polling ipv WebSocket |
| Progress Tracking | ✅ | ✅ | Identiek |
| Session Management | ✅ | ⚠️ | Vercel: tijdelijk (in-memory) |
| AI Suggestions | ✅ | ✅ | Identiek |
| Dark Mode | ✅ | ✅ | Identiek |
| Export Functie | ✅ | ✅ | Identiek |
| Multiple Templates | ✅ | ✅ | Quick/Standard/Extensive |

## Performance

### Lokale Versie
- **Latency**: <50ms (WebSocket)
- **Concurrent Users**: Beperkt door server resources
- **Scaling**: Handmatig (meer servers)
- **Kosten**: Server hosting kosten

### Vercel Versie
- **Latency**: ~2000ms (polling interval)
- **Concurrent Users**: Automatisch scaling
- **Scaling**: Automatisch (serverless)
- **Kosten**: Pay-per-use (Free tier beschikbaar)

## Wanneer Welke Versie?

### Gebruik Lokale Versie als:
- Je volledige controle wilt over infrastructure
- Je real-time (<100ms) responses nodig hebt
- Je al een server hebt
- Je complexe session persistence nodig hebt

### Gebruik Vercel Versie als:
- Je snel wilt deployen zonder server setup
- Je automatische scaling wilt
- Je geen server wilt beheren
- Polling (2s delay) acceptabel is
- Je global CDN wilt (snelle loading wereldwijd)

## Migratie Pad

### Van Lokaal naar Vercel:
1. Deploy Vercel versie
2. Test thoroughly
3. Voeg database toe (Vercel KV/Postgres)
4. Migreer sessions
5. Switch DNS

### Van Vercel naar Lokaal:
1. Setup server
2. Deploy lokale versie
3. Export sessions van Vercel
4. Import in lokale database
5. Switch DNS

## Toekomstige Verbeteringen

### Voor Vercel Versie:
1. **Database**: Vercel KV of Postgres voor session persistence
2. **Caching**: Redis voor template/fase instructions
3. **WebSocket**: Vercel Edge Functions (experimenteel)
4. **Authentication**: NextAuth.js of Auth0
5. **Rate Limiting**: Upstash Rate Limit

### Voor Lokale Versie:
1. **Clustering**: PM2 voor multiple processes
2. **Load Balancing**: Nginx
3. **Database**: PostgreSQL voor sessions
4. **Caching**: Redis
5. **Monitoring**: Prometheus + Grafana

## Code Hergebruik

Beide versies delen:
- ✅ `interview_agent.py` - Core AI logic
- ✅ `templates.py` - Template configuratie
- ✅ Frontend HTML/CSS/JS (met kleine aanpassingen)

Verschillend:
- ❌ `main.py` vs `api/*.py` - API layer
- ❌ `session_manager.py` vs `storage.py` - Storage layer
- ❌ WebSocket vs REST API calls in frontend

## Conclusie

Beide versies zijn volledig functioneel en bieden dezelfde features. De keuze hangt af van je requirements:

- **Vercel**: Makkelijk, snel, schaalbaar, geen server management
- **Lokaal**: Meer controle, real-time, complexere setup

Voor de meeste use cases is **Vercel de beste keuze** vanwege:
- Geen server setup nodig
- Automatische HTTPS
- Global CDN
- Automatische scaling
- Free tier beschikbaar
