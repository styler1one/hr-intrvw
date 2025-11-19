# Volentis Interview Agent - Vercel Deployment

Deze versie is geoptimaliseerd voor deployment op Vercel met serverless functions.

## Verschillen met lokale versie

### Architectuur
- **Lokaal**: WebSocket-based real-time communicatie
- **Vercel**: REST API met polling (geen WebSocket support)

### Storage
- **Lokaal**: File-based sessions in `./sessions` directory
- **Vercel**: In-memory storage (kan uitgebreid worden met Vercel KV/PostgreSQL)

### API Endpoints
Alle endpoints zijn nu serverless functions in de `/api` directory:
- `GET /api/templates` - Haal templates op
- `POST /api/session/start` - Start nieuwe sessie
- `POST /api/session/{id}/chat` - Verstuur bericht en ontvang response
- `GET /api/session/{id}` - Haal sessie info op
- `GET /api/session/{id}/export` - Exporteer sessie data

## Deployment naar Vercel

### 1. Installeer Vercel CLI
```bash
npm install -g vercel
```

### 2. Login bij Vercel
```bash
vercel login
```

### 3. Configureer environment variables
Maak een `.env` file aan (niet committen!):
```env
OPENAI_API_KEY=your_openai_api_key_here
LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo
```

### 4. Deploy naar Vercel
```bash
cd vercel-deployment
vercel
```

Bij eerste deployment:
- Kies een project naam
- Selecteer je Vercel account
- Bevestig de settings

### 5. Voeg environment variables toe in Vercel Dashboard
1. Ga naar https://vercel.com/dashboard
2. Selecteer je project
3. Ga naar Settings > Environment Variables
4. Voeg toe:
   - `OPENAI_API_KEY` = je OpenAI API key
   - `LLM_PROVIDER` = `openai`
   - `LLM_MODEL` = `gpt-4-turbo`

### 6. Redeploy
```bash
vercel --prod
```

## Frontend aanpassingen

De frontend in `/public/index.html` moet aangepast worden om:
1. REST API te gebruiken in plaats van WebSocket
2. Polling te implementeren voor real-time updates
3. API base URL aan te passen naar je Vercel domain

Vervang in `index.html`:
```javascript
const API_BASE = 'https://your-project.vercel.app';
```

## Beperkingen

### Session Persistence
De huidige implementatie gebruikt in-memory storage. Voor productie:

**Optie 1: Vercel KV (Redis)**
```bash
vercel link
vercel env pull
```

Voeg toe aan `storage.py`:
```python
from vercel_kv import KV

class VercelKVStorage(SessionStorage):
    def __init__(self):
        self.kv = KV()
    
    def create_session(self, session_id: str, template_id: str = "standard") -> dict:
        # Implementation
        pass
```

**Optie 2: PostgreSQL (Vercel Postgres)**
```bash
vercel postgres create
```

### WebSocket Alternative
Omdat Vercel geen WebSocket ondersteunt, gebruikt deze versie polling:
- Frontend pollt elke 2 seconden voor updates
- Niet zo real-time als WebSocket maar werkt goed voor dit use case

## Testing Lokaal

Test de Vercel deployment lokaal:
```bash
cd vercel-deployment
vercel dev
```

Dit start een lokale development server die de Vercel environment simuleert.

## Monitoring

Bekijk logs in Vercel Dashboard:
1. Ga naar je project
2. Klik op "Deployments"
3. Selecteer een deployment
4. Klik op "Functions" tab voor logs

## Kosten

Vercel Free tier:
- 100GB bandwidth/maand
- 100 serverless function invocations/dag
- Voldoende voor testing en kleine deployments

Voor productie: Upgrade naar Pro ($20/maand) voor:
- Unlimited bandwidth
- Unlimited functions
- Custom domains
- Analytics

## Support

Voor vragen over deze deployment:
- Vercel Docs: https://vercel.com/docs
- FastAPI on Vercel: https://vercel.com/guides/python-fastapi

## Volgende Stappen

1. **Database toevoegen**: Implementeer Vercel KV of Postgres voor session persistence
2. **Authentication**: Voeg user authentication toe
3. **Rate Limiting**: Implementeer rate limiting voor API endpoints
4. **Caching**: Cache template data en fase instructions
5. **Monitoring**: Voeg Sentry of Vercel Analytics toe
