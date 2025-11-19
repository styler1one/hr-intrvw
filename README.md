# Volentis Interview Agent - Vercel Deployment

AI-powered interview agent voor HR implementatie planning, geoptimaliseerd voor Vercel deployment.

## 🚀 Quick Start

### Vercel Deployment (Aanbevolen)

Deze repository is gekoppeld aan Vercel en deployt automatisch bij elke push naar `main`.

**Setup:**
1. Ga naar [Vercel Dashboard](https://vercel.com/dashboard)
2. Klik op je project
3. Ga naar **Settings** > **Environment Variables**
4. Voeg toe:
   ```
   OPENAI_API_KEY = sk-...
   LLM_PROVIDER = openai
   LLM_MODEL = gpt-4-turbo
   ```
5. Redeploy (gebeurt automatisch bij push)

**Live URL:** Je app is beschikbaar op `https://your-project.vercel.app`

### Lokaal Testen

```bash
# Installeer Vercel CLI
npm install -g vercel

# Start development server
vercel dev

# Open http://localhost:3000
```

## 📁 Project Structuur

```
├── api/                      # Serverless Functions
│   ├── index.py             # Root endpoint
│   ├── templates_endpoint.py # GET /api/templates
│   ├── session_start.py     # POST /api/session/start
│   ├── chat.py              # Chat API (REST)
│   ├── interview_agent.py   # Core AI logic
│   ├── storage.py           # Session storage
│   └── templates.py         # Template configuratie
├── public/                   # Static files
│   ├── index.html           # Frontend
│   └── config.js            # API configuratie
├── vercel.json              # Vercel configuratie
├── requirements.txt         # Python dependencies
└── package.json             # NPM scripts
```

## ✨ Features

- ✅ **3 Interview Templates**: Quick (5 fases), Standard (11 fases), Extensive (15 fases)
- ✅ **AI-Powered Chat**: OpenAI GPT-4 voor intelligente vragen
- ✅ **Smart Suggestions**: Context-aware antwoord suggesties
- ✅ **Progress Tracking**: Real-time voortgang per template
- ✅ **Session Management**: Bewaar en hervat interviews
- ✅ **Dark Mode**: Oogvriendelijke interface
- ✅ **Export**: Download interview data

## 🔧 Technologie Stack

**Backend:**
- FastAPI (Serverless Functions)
- OpenAI GPT-4
- Python 3.9+

**Frontend:**
- Vanilla JavaScript
- Tailwind CSS
- REST API (polling)

**Deployment:**
- Vercel (Serverless)
- Automatische HTTPS
- Global CDN

## 📚 Documentatie

- **[DEPLOYMENT_STEPS.md](./DEPLOYMENT_STEPS.md)** - Stap-voor-stap deployment guide
- **[DIFFERENCES.md](./DIFFERENCES.md)** - Verschillen lokaal vs Vercel
- **[README_VERCEL.md](./README_VERCEL.md)** - Technische details Vercel setup

## 🔑 Environment Variables

Vereist in Vercel Dashboard:

| Variable | Beschrijving | Voorbeeld |
|----------|--------------|-----------|
| `OPENAI_API_KEY` | OpenAI API key | `sk-...` |
| `LLM_PROVIDER` | LLM provider | `openai` |
| `LLM_MODEL` | Model naam | `gpt-4-turbo` |

Optioneel:

| Variable | Beschrijving | Default |
|----------|--------------|---------|
| `STORAGE_TYPE` | Storage backend | `memory` |

## 🎯 API Endpoints

| Endpoint | Method | Beschrijving |
|----------|--------|--------------|
| `/api/templates` | GET | Haal templates op |
| `/api/session/start` | POST | Start nieuwe sessie |
| `/api/session/{id}/chat` | POST | Verstuur bericht |
| `/api/session/{id}` | GET | Haal sessie info op |
| `/api/session/{id}/export` | GET | Exporteer sessie data |

## 🔄 Deployment Flow

```
Git Push → GitHub → Vercel
                      ↓
              Automatische Build
                      ↓
              Serverless Deploy
                      ↓
                Live Update
```

## 📊 Vercel Limits (Free Tier)

- ✅ 100GB bandwidth/maand
- ✅ 100 serverless function invocations/dag
- ✅ Unlimited static requests
- ✅ Automatische HTTPS
- ✅ Global CDN

## 🚨 Belangrijke Notities

### Session Persistence
⚠️ **Huidige versie gebruikt in-memory storage** - sessions verdwijnen bij restart.

Voor productie:
- Implementeer Vercel KV (Redis)
- Of gebruik Vercel Postgres
- Zie [README_VERCEL.md](./README_VERCEL.md) voor details

### WebSocket vs REST
Deze versie gebruikt REST API met polling (2s interval) in plaats van WebSocket.
- ✅ Werkt op Vercel
- ✅ Goed genoeg voor dit use case
- ⚠️ Iets hogere latency dan WebSocket

## 🛠️ Development

### Lokaal Draaien

```bash
# Clone repository
git clone https://github.com/styler1one/hr-intrvw.git
cd hr-intrvw

# Maak .env file
echo "OPENAI_API_KEY=sk-..." > .env
echo "LLM_PROVIDER=openai" >> .env
echo "LLM_MODEL=gpt-4-turbo" >> .env

# Start Vercel dev server
vercel dev
```

### Deployment

```bash
# Deploy naar preview
vercel

# Deploy naar productie
vercel --prod
```

## 🐛 Troubleshooting

### "Function execution timed out"
- Verhoog timeout in `vercel.json` (max 30s op Free tier)

### "Environment variable not found"
- Check Vercel Dashboard > Settings > Environment Variables
- Redeploy na toevoegen variables

### Sessions verdwijnen
- In-memory storage is tijdelijk
- Implementeer database voor persistence

## 📞 Support

- **Vercel Docs**: https://vercel.com/docs
- **FastAPI on Vercel**: https://vercel.com/guides/python-fastapi
- **GitHub Issues**: https://github.com/styler1one/hr-intrvw/issues

## 📝 License

MIT License - zie LICENSE file voor details

## 🎉 Credits

Ontwikkeld door AgentBoss voor Volentis HR Agent implementaties.

---

**Status:** ✅ Production Ready  
**Version:** 1.0.0  
**Last Updated:** November 2025
