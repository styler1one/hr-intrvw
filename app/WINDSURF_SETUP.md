# Volentis Interview Agent - Windsurf Setup

## 🌊 Windsurf Configuratie

Als je Windsurf gebruikt, kun je de LLM API's gebruiken die al in Windsurf geconfigureerd zijn.

### Optie 1: Gebruik Windsurf's API Key

Als Windsurf een eigen API endpoint heeft:

1. Open `.env` in de backend folder
2. Configureer als volgt:

```bash
# LLM Provider
LLM_PROVIDER=windsurf

# Windsurf API configuratie
WINDSURF_API_KEY=your-windsurf-api-key
WINDSURF_API_BASE=https://api.windsurf.ai/v1

# Model (check welke models Windsurf ondersteunt)
LLM_MODEL=gpt-4-turbo
```

### Optie 2: Gebruik OpenAI via Windsurf

Als Windsurf OpenAI gebruikt:

```bash
# LLM Provider
LLM_PROVIDER=openai

# OpenAI API Key (van Windsurf configuratie)
OPENAI_API_KEY=sk-your-openai-key

# Model
LLM_MODEL=gpt-4-turbo
```

### Optie 3: Gebruik Anthropic (Claude)

Als je Claude wilt gebruiken:

```bash
# LLM Provider
LLM_PROVIDER=anthropic

# Anthropic API Key
ANTHROPIC_API_KEY=sk-ant-your-key

# Model (Claude 3 Opus is het beste)
LLM_MODEL=claude-3-opus-20240229
```

---

## 🔍 Windsurf API Key Vinden

### Methode 1: Windsurf Settings

1. Open Windsurf
2. Ga naar Settings/Preferences
3. Zoek naar "API" of "LLM" configuratie
4. Kopieer de API key

### Methode 2: Windsurf Config File

Windsurf slaat configuratie vaak op in:

**Windows:**
```
%APPDATA%\Windsurf\config.json
```

**Mac/Linux:**
```
~/.config/windsurf/config.json
```

Zoek in dit bestand naar:
- `apiKey`
- `openai_api_key`
- `anthropic_api_key`

### Methode 3: Environment Variables

Windsurf gebruikt mogelijk environment variables:

```powershell
# Check Windows environment variables
Get-ChildItem Env: | Where-Object { $_.Name -like "*API*" -or $_.Name -like "*WINDSURF*" }
```

---

## 🧪 Testen

### Test 1: Check welke provider werkt

Maak een test script `test_provider.py`:

```python
import os
from dotenv import load_dotenv
from interview_agent import InterviewAgent

load_dotenv()

# Test OpenAI
try:
    agent = InterviewAgent(
        provider="openai",
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4-turbo"
    )
    print("✅ OpenAI werkt!")
except Exception as e:
    print(f"❌ OpenAI error: {e}")

# Test Windsurf
try:
    agent = InterviewAgent(
        provider="windsurf",
        api_key=os.getenv("WINDSURF_API_KEY"),
        model="gpt-4-turbo",
        api_base=os.getenv("WINDSURF_API_BASE")
    )
    print("✅ Windsurf werkt!")
except Exception as e:
    print(f"❌ Windsurf error: {e}")

# Test Anthropic
try:
    agent = InterviewAgent(
        provider="anthropic",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        model="claude-3-opus-20240229"
    )
    print("✅ Anthropic werkt!")
except Exception as e:
    print(f"❌ Anthropic error: {e}")
```

Run:
```powershell
python test_provider.py
```

---

## 💡 Aanbevolen Configuratie

### Voor Ontwikkeling (Goedkoop)

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key
LLM_MODEL=gpt-3.5-turbo  # ~$0.05 per interview
```

### Voor Productie (Beste Kwaliteit)

**Optie A: OpenAI GPT-4 Turbo**
```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key
LLM_MODEL=gpt-4-turbo  # ~$0.50-1.00 per interview
```

**Optie B: Anthropic Claude 3 Opus**
```bash
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-key
LLM_MODEL=claude-3-opus-20240229  # ~$0.75-1.50 per interview
```

**Optie C: Windsurf (als beschikbaar)**
```bash
LLM_PROVIDER=windsurf
WINDSURF_API_KEY=your-key
WINDSURF_API_BASE=https://api.windsurf.ai/v1
LLM_MODEL=gpt-4-turbo
```

---

## 🔧 Troubleshooting

### Probleem: "Unsupported provider: windsurf"

**Oplossing:**
- Check of `LLM_PROVIDER=windsurf` correct gespeld is in `.env`
- Herstart de backend server

### Probleem: "Authentication failed"

**Oplossing:**
- Check of API key correct is
- Check of API key niet verlopen is
- Voor Windsurf: check of `WINDSURF_API_BASE` correct is

### Probleem: "Model not found"

**Oplossing:**
- Check welke models je provider ondersteunt
- Voor OpenAI: gpt-4-turbo, gpt-4o, gpt-3.5-turbo
- Voor Anthropic: claude-3-opus-20240229, claude-3-sonnet-20240229
- Voor Windsurf: check Windsurf documentatie

### Probleem: Windsurf API base URL onbekend

**Oplossing:**

Als Windsurf geen eigen API heeft, gebruik dan gewoon OpenAI:

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-openai-key  # Van Windsurf of direct van OpenAI
LLM_MODEL=gpt-4-turbo
```

---

## 📊 Provider Vergelijking

| Provider | Kosten/Interview | Kwaliteit | Snelheid | Beschikbaarheid |
|----------|------------------|-----------|----------|-----------------|
| GPT-3.5-turbo | $0.05 | ⭐⭐⭐ | ⚡⚡⚡ | ✅ Altijd |
| GPT-4-turbo | $0.50-1.00 | ⭐⭐⭐⭐⭐ | ⚡⚡ | ✅ Altijd |
| GPT-4o | $0.25-0.50 | ⭐⭐⭐⭐ | ⚡⚡⚡ | ✅ Altijd |
| Claude 3 Opus | $0.75-1.50 | ⭐⭐⭐⭐⭐ | ⚡⚡ | ✅ Altijd |
| Claude 3 Sonnet | $0.15-0.30 | ⭐⭐⭐⭐ | ⚡⚡⚡ | ✅ Altijd |
| Windsurf | ? | ? | ? | ❓ Afhankelijk |

---

## 🎯 Aanbeveling

**Voor nu:**
1. Probeer eerst OpenAI (makkelijkst)
2. Als je Claude wilt: gebruik Anthropic
3. Als Windsurf een eigen API heeft: gebruik die

**Beste keuze voor productie:**
- **GPT-4-turbo**: Beste balans prijs/kwaliteit
- **Claude 3 Opus**: Beste kwaliteit, iets duurder
- **GPT-4o**: Sneller, goede kwaliteit, goedkoper

---

Succes! 🚀
