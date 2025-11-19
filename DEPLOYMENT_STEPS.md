# Stap-voor-stap Deployment naar Vercel

## Voorbereiding

### 1. Maak een Vercel account
- Ga naar https://vercel.com/signup
- Sign up met GitHub, GitLab of email

### 2. Installeer Vercel CLI (optioneel, kan ook via web)
```bash
npm install -g vercel
```

## Deployment via Web Interface (Makkelijkst)

### Stap 1: Push naar GitHub
```bash
cd vercel-deployment
git init
git add .
git commit -m "Initial Vercel deployment"
git remote add origin https://github.com/jouw-username/interview-agent-vercel.git
git push -u origin main
```

### Stap 2: Import in Vercel
1. Ga naar https://vercel.com/new
2. Klik "Import Git Repository"
3. Selecteer je GitHub repository
4. Vercel detecteert automatisch de configuratie
5. Klik "Deploy"

### Stap 3: Configureer Environment Variables
1. Ga naar je project in Vercel Dashboard
2. Klik "Settings" > "Environment Variables"
3. Voeg toe:
   ```
   OPENAI_API_KEY = sk-...
   LLM_PROVIDER = openai
   LLM_MODEL = gpt-4-turbo
   ```
4. Klik "Save"

### Stap 4: Redeploy
1. Ga naar "Deployments" tab
2. Klik op de laatste deployment
3. Klik "Redeploy"

## Deployment via CLI

### Stap 1: Login
```bash
vercel login
```

### Stap 2: Deploy
```bash
cd vercel-deployment
vercel
```

Beantwoord de vragen:
- Set up and deploy? **Y**
- Which scope? Kies je account
- Link to existing project? **N**
- What's your project's name? **interview-agent**
- In which directory is your code located? **./**

### Stap 3: Voeg Environment Variables toe
```bash
vercel env add OPENAI_API_KEY
# Plak je API key

vercel env add LLM_PROVIDER
# Type: openai

vercel env add LLM_MODEL  
# Type: gpt-4-turbo
```

### Stap 4: Deploy naar productie
```bash
vercel --prod
```

## Verificatie

### Test de API
```bash
# Vervang YOUR_DOMAIN met je Vercel URL
curl https://YOUR_DOMAIN.vercel.app/api/templates
```

Verwachte output:
```json
{
  "templates": {
    "quick": {...},
    "standard": {...},
    "extensive": {...}
  }
}
```

### Test de Frontend
Open in browser:
```
https://YOUR_DOMAIN.vercel.app
```

## Custom Domain (Optioneel)

### Stap 1: Voeg domain toe
1. Ga naar Project Settings > Domains
2. Voer je domain in (bijv. `interview.jouwbedrijf.nl`)
3. Klik "Add"

### Stap 2: Configureer DNS
Voeg deze records toe bij je DNS provider:

**Voor apex domain (jouwbedrijf.nl):**
```
Type: A
Name: @
Value: 76.76.21.21
```

**Voor subdomain (interview.jouwbedrijf.nl):**
```
Type: CNAME
Name: interview
Value: cname.vercel-dns.com
```

### Stap 3: Wacht op verificatie
Vercel verifieert automatisch (kan 24-48 uur duren)

## Troubleshooting

### "Function execution timed out"
- Verhoog timeout in `vercel.json`:
```json
{
  "functions": {
    "api/**/*.py": {
      "maxDuration": 30
    }
  }
}
```

### "Module not found"
- Check `requirements.txt`
- Redeploy met `vercel --prod --force`

### "Environment variable not found"
- Verifieer in Vercel Dashboard > Settings > Environment Variables
- Redeploy na toevoegen variables

### Sessions verdwijnen
- In-memory storage is tijdelijk
- Implementeer Vercel KV of Postgres voor persistence

## Monitoring

### Bekijk Logs
```bash
vercel logs YOUR_DOMAIN.vercel.app
```

Of in Dashboard:
1. Ga naar Deployments
2. Klik op deployment
3. Klik "Functions" tab

### Analytics
Vercel Pro heeft ingebouwde analytics:
- Pageviews
- API calls
- Performance metrics

## Kosten Optimalisatie

### Free Tier Limits
- 100GB bandwidth/maand
- 100 serverless function executions/dag
- 6000 build minutes/maand

### Tips om binnen Free Tier te blijven
1. Cache static assets
2. Optimaliseer API calls
3. Gebruik CDN voor images

### Upgrade naar Pro ($20/maand)
- Unlimited bandwidth
- Unlimited functions
- Custom domains
- Priority support

## Volgende Stappen

1. **Setup Monitoring**: Voeg Sentry toe voor error tracking
2. **Add Database**: Implementeer Vercel Postgres
3. **Enable Caching**: Cache template data
4. **Add Authentication**: Implementeer user login
5. **Setup CI/CD**: Automatisch deployen bij git push

## Support

- Vercel Docs: https://vercel.com/docs
- Vercel Community: https://github.com/vercel/vercel/discussions
- FastAPI on Vercel: https://vercel.com/guides/python-fastapi
