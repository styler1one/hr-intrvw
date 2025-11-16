# 🚀 Volentis Interview Agent - Quick Start

## ✅ Wat je nodig hebt

1. **Python 3.10+** - Check: `python --version`
2. **Een API Key** - Kies één van deze opties:

### Optie A: OpenAI (Aanbevolen - Makkelijkst)
- **Prijs:** ~$0.50-1.00 per interview
- **Kwaliteit:** ⭐⭐⭐⭐⭐
- **Setup:** 2 minuten

**Stappen:**
1. Ga naar https://platform.openai.com/api-keys
2. Log in (of maak account)
3. Klik "Create new secret key"
4. Kopieer de key (begint met `sk-`)
5. Zorg voor $5+ credits op je account

### Optie B: Anthropic Claude (Beste kwaliteit)
- **Prijs:** ~$0.75-1.50 per interview  
- **Kwaliteit:** ⭐⭐⭐⭐⭐
- **Setup:** 2 minuten

**Stappen:**
1. Ga naar https://console.anthropic.com/
2. Maak account
3. Ga naar API Keys
4. Kopieer key (begint met `sk-ant-`)

### Optie C: GPT-3.5 (Goedkoop voor testen)
- **Prijs:** ~$0.05 per interview
- **Kwaliteit:** ⭐⭐⭐
- **Setup:** Zelfde als Optie A, maar gebruik `gpt-3.5-turbo` model

---

## 📦 Installatie (5 minuten)

### Stap 1: Open Terminal in Backend folder

```powershell
cd "g:\My Drive\_Agentboss\InterviewAgent\app\backend"
```

### Stap 2: Maak Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Je ziet nu `(venv)` voor je prompt.

### Stap 3: Installeer Dependencies

```powershell
pip install -r requirements.txt
```

Dit duurt ~1 minuut.

### Stap 4: Configureer API Key

```powershell
# Kopieer template
copy .env.example .env

# Open in notepad
notepad .env
```

**Voor OpenAI:**
```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-actual-key-here
LLM_MODEL=gpt-4-turbo
```

**Voor Claude:**
```bash
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
LLM_MODEL=claude-3-opus-20240229
```

**Voor Goedkoop Testen:**
```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-actual-key-here
LLM_MODEL=gpt-3.5-turbo
```

Sla op en sluit notepad.

### Stap 5: Start Backend

```powershell
python main.py
```

Je zou moeten zien:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

✅ **Backend draait!** Laat dit terminal venster open.

---

## 🌐 Frontend Starten

### Stap 6: Open NIEUW Terminal venster

```powershell
cd "g:\My Drive\_Agentboss\InterviewAgent\app\frontend"
python -m http.server 3000
```

Je zou moeten zien:
```
Serving HTTP on :: port 3000
```

✅ **Frontend draait!**

---

## 🎉 Gebruik de App

### Stap 7: Open Browser

Ga naar: **http://localhost:3000**

Je zou een mooie interface moeten zien met:
- 🤖 Volentis Interview Agent header
- Progress bar
- "Start Interview" knop

### Stap 8: Start Interview

1. Klik "Start Interview"
2. Je krijgt een welkomstbericht
3. Beantwoord de vragen
4. De progress bar vult zich (0% → 100%)

---

## ✅ Test Checklist

- [ ] Backend draait op http://localhost:8000
- [ ] Frontend draait op http://localhost:3000
- [ ] Browser toont de interface
- [ ] "Start Interview" knop werkt
- [ ] Agent reageert op je antwoorden
- [ ] Progress bar werkt

---

## 🐛 Problemen?

### "ModuleNotFoundError"
```powershell
# Check of venv actief is
.\venv\Scripts\Activate.ps1

# Herinstalleer
pip install -r requirements.txt
```

### "Authentication failed"
- Check of API key correct is in `.env`
- Check of key begint met `sk-` (OpenAI) of `sk-ant-` (Anthropic)
- Check of je account credits heeft

### "Port already in use"
```powershell
# Stop proces op port 8000
netstat -ano | findstr :8000
# Noteer PID (laatste kolom)
taskkill /PID <PID> /F
```

### Agent reageert niet
- Check backend terminal voor errors
- Check of API key geldig is
- Check of je credits hebt

### "WebSocket connection failed"
- Refresh browser pagina
- Check of backend draait
- Check firewall settings

---

## 💰 Kosten

**Per volledig interview (45-60 min):**

| Model | Kosten | Kwaliteit |
|-------|--------|-----------|
| GPT-3.5-turbo | $0.05 | ⭐⭐⭐ |
| GPT-4o | $0.25-0.50 | ⭐⭐⭐⭐ |
| GPT-4-turbo | $0.50-1.00 | ⭐⭐⭐⭐⭐ |
| Claude 3 Sonnet | $0.15-0.30 | ⭐⭐⭐⭐ |
| Claude 3 Opus | $0.75-1.50 | ⭐⭐⭐⭐⭐ |

**Aanbeveling voor productie:** GPT-4-turbo (beste balans)

---

## 🎯 Volgende Stappen

### Nu werkend:
- ✅ Fase 1: Intro & context
- ✅ Fase 2: Stakeholders
- ⚠️ Fases 3-11: Basis geïmplementeerd (kunnen uitgebreid worden)

### Om te verbeteren:
1. **Alle 11 fases volledig implementeren**
   - Kopieer instructies uit `Volentis_Interview_Agent_Config.md`
   - Voeg toe aan `interview_agent.py`

2. **Plan & Roadmap generatie toevoegen**
   - Maak `plan_agent.py`
   - Maak `roadmap_agent.py`
   - Trigger na interview completion

3. **Export functionaliteit**
   - PDF export
   - Word export
   - Email functie

4. **Database toevoegen**
   - SQLite voor simpel
   - PostgreSQL voor productie

---

## 📞 Hulp Nodig?

**Documentatie:**
- `README.md` - Volledige installatie guide
- `WINDSURF_SETUP.md` - Windsurf specifieke info
- `DEPLOYMENT_GUIDE.md` - Productie deployment

**Config Files:**
- `Volentis_Interview_Agent_Config.md` - Agent configuratie
- `Volentis_Implementation_Plan_Agent_Config.md` - Plan agent
- `Volentis_Improvement_Roadmap_Agent_Config.md` - Roadmap agent

---

## 🎊 Klaar!

Je hebt nu een werkende Volentis Interview Agent! 🚀

**Test het door:**
1. Een volledig interview te doen
2. Verschillende antwoorden te proberen
3. Te kijken of de progress bar werkt
4. Te checken of sessions worden opgeslagen

**Veel succes!** 🎉
