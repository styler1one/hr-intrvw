# Volentis Interview Agent - Lokale Installatie

## 🚀 Quick Start (5 minuten)

### Vereisten
- Python 3.10 of hoger
- OpenAI API key (krijg je van https://platform.openai.com/api-keys)
- Een moderne webbrowser

### Stap 1: API Key verkrijgen

**Optie A: Gebruik Windsurf (Aanbevolen als je Windsurf hebt)**

Zie `WINDSURF_SETUP.md` voor gedetailleerde instructies.

**Optie B: Gebruik OpenAI**

1. Ga naar https://platform.openai.com/api-keys
2. Log in of maak een account
3. Klik op "Create new secret key"
4. Kopieer de key (begint met `sk-`)
5. **Belangrijk:** Zorg dat je account credits heeft (minimaal $5)

**Optie C: Gebruik Anthropic (Claude)**

1. Ga naar https://console.anthropic.com/
2. Maak een account
3. Ga naar API Keys
4. Kopieer de key (begint met `sk-ant-`)

### Stap 2: Backend installeren

Open een terminal/PowerShell in de `app/backend` folder:

```powershell
# Navigeer naar backend folder
cd "g:\My Drive\_Agentboss\InterviewAgent\app\backend"

# Maak een virtual environment
python -m venv venv

# Activeer virtual environment
.\venv\Scripts\Activate.ps1

# Installeer dependencies
pip install -r requirements.txt

# Kopieer .env.example naar .env
copy .env.example .env

# Open .env en vul je OpenAI API key in
notepad .env
```

In `.env`, vervang `sk-your-api-key-here` met je echte API key.

### Stap 3: Backend starten

```powershell
# Zorg dat je nog in de backend folder bent en venv actief is
python main.py
```

Je zou moeten zien:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

✅ Backend draait nu op http://localhost:8000

### Stap 4: Frontend openen

Open een NIEUWE terminal/PowerShell:

```powershell
# Navigeer naar frontend folder
cd "g:\My Drive\_Agentboss\InterviewAgent\app\frontend"

# Start een simpele webserver
python -m http.server 3000
```

Je zou moeten zien:
```
Serving HTTP on :: port 3000 (http://[::]:3000/) ...
```

✅ Frontend draait nu op http://localhost:3000

### Stap 5: Open in browser

Open je browser en ga naar:
```
http://localhost:3000
```

Je zou de Volentis Interview Agent moeten zien! 🎉

Klik op "Start Interview" om te beginnen.

---

## 🧪 Testen

### Test 1: Check of backend werkt

Open http://localhost:8000 in je browser.

Je zou moeten zien:
```json
{
  "message": "Volentis Interview Agent API",
  "version": "1.0.0",
  "status": "running"
}
```

### Test 2: Start een interview

1. Ga naar http://localhost:3000
2. Klik "Start Interview"
3. Je zou een welkomstbericht moeten zien
4. Type een antwoord en druk Enter
5. De agent zou moeten reageren

---

## 🐛 Troubleshooting

### Probleem: "ModuleNotFoundError: No module named 'fastapi'"

**Oplossing:**
```powershell
# Zorg dat virtual environment actief is
.\venv\Scripts\Activate.ps1

# Installeer dependencies opnieuw
pip install -r requirements.txt
```

### Probleem: "openai.AuthenticationError: Incorrect API key"

**Oplossing:**
- Check of je `.env` file bestaat in de backend folder
- Check of je API key correct is (begint met `sk-`)
- Check of je OpenAI account credits heeft

### Probleem: "WebSocket connection failed"

**Oplossing:**
- Check of backend draait op http://localhost:8000
- Check of er geen firewall de verbinding blokkeert
- Refresh de browser pagina

### Probleem: "Port 8000 is already in use"

**Oplossing:**
```powershell
# Stop het proces op port 8000
netstat -ano | findstr :8000
# Noteer de PID (laatste kolom)
taskkill /PID <PID> /F

# Of gebruik een andere port
# In .env: PORT=8001
# In frontend/index.html: wijzig API_URL naar http://localhost:8001
```

### Probleem: Agent reageert niet of geeft rare antwoorden

**Oplossing:**
- Check of je het juiste model gebruikt (gpt-4-turbo aanbevolen)
- Check of je OpenAI account genoeg credits heeft
- Kijk in de backend terminal voor error messages

---

## 📁 Project Structuur

```
app/
├── backend/
│   ├── main.py                 # FastAPI server
│   ├── interview_agent.py      # Interview Agent logica
│   ├── session_manager.py      # Session management
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example           # Environment variables template
│   └── .env                   # Your actual environment variables (niet in git!)
│
└── frontend/
    └── index.html             # Web interface
```

---

## 🔧 Configuratie

### Backend (.env)

```bash
# OpenAI API Key
OPENAI_API_KEY=sk-your-key-here

# Model (opties: gpt-4-turbo, gpt-4o, gpt-3.5-turbo)
LLM_MODEL=gpt-4-turbo

# Server
HOST=0.0.0.0
PORT=8000

# Frontend URL (voor CORS)
FRONTEND_URL=http://localhost:3000
```

### Model Keuze

- **gpt-4-turbo** (aanbevolen): Beste kwaliteit, ~$0.01/1K tokens
- **gpt-4o**: Sneller, goede kwaliteit, ~$0.005/1K tokens
- **gpt-3.5-turbo**: Goedkoop voor testen, ~$0.0005/1K tokens (minder goede kwaliteit)

Een volledig interview kost ongeveer:
- gpt-4-turbo: $0.50 - $1.00
- gpt-4o: $0.25 - $0.50
- gpt-3.5-turbo: $0.05 - $0.10

---

## 🚀 Volgende Stappen

### Fase 2-11 toevoegen

De huidige versie heeft alleen Fase 1 en 2 volledig geïmplementeerd.

Om alle 11 fases toe te voegen:

1. Open `backend/interview_agent.py`
2. Voeg fase-instructies toe aan `load_fase_instructions()`
3. Kopieer de instructies uit `Volentis_Interview_Agent_Config.md`

Voorbeeld:
```python
def load_fase_instructions(self):
    return {
        1: { ... },  # Al geïmplementeerd
        2: { ... },  # Al geïmplementeerd
        3: {
            "name": "HR-service & ticketdruk",
            "duration": "7 min",
            "instructions": """
            [Kopieer uit Volentis_Interview_Agent_Config.md Fase 3]
            """
        },
        # ... fases 4-11
    }
```

### Plan & Roadmap Generatie toevoegen

1. Maak `plan_agent.py` en `roadmap_agent.py` in backend
2. Voeg generatie logica toe in `main.py` na interview completion
3. Voeg export functionaliteit toe (PDF/Word)

### Database toevoegen

Voor productie, vervang file-based sessions met een database:

```python
# In session_manager.py
import psycopg2  # of sqlite3 voor simpel

class SessionManager:
    def __init__(self, db_url):
        self.conn = psycopg2.connect(db_url)
        # ... rest van implementatie
```

---

## 📞 Hulp Nodig?

- **Documentatie:** Zie `DEPLOYMENT_GUIDE.md` voor uitgebreide info
- **Agent Configs:** Zie `Volentis_Interview_Agent_Config.md`
- **Issues:** Check backend terminal voor error messages

---

## ✅ Checklist voor Productie

Voordat je live gaat:

- [ ] Alle 11 fases geïmplementeerd
- [ ] Plan & Roadmap generatie werkt
- [ ] Database ipv file-based sessions
- [ ] Authentication toegevoegd
- [ ] HTTPS/SSL certificaat
- [ ] Rate limiting
- [ ] Error monitoring (Sentry)
- [ ] Backup strategie
- [ ] Load testing gedaan
- [ ] Security audit gedaan

---

Veel succes! 🚀
