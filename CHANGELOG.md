# Changelog

All notable changes to the Volentis Interview Agent project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-11-16

### Added
- **Core Interview Agent**: Multi-fase interview systeem met 11 fases
- **Backend API**: FastAPI WebSocket-based interview systeem
- **Frontend**: Modern chat interface met ChatGPT-stijl UI
- **Session Management**: Persistente sessies met pause/resume functionaliteit
- **Multi-LLM Support**: OpenAI, Anthropic, en Windsurf providers
- **Smart AI Suggestions**: 
  - AI-powered suggesties via LLM
  - Context-aware suggesties gebaseerd op conversatie geschiedenis
  - Meerdere suggesties selecteren mogelijk
  - Auto-scroll functionaliteit
  - Fallback naar generieke suggesties bij API fouten
- **Progress Tracking**: Visuele voortgangsindicator per fase
- **Back Button**: Mogelijkheid om terug te gaan naar vorige vraag
- **Fase Systemen**: 
  - Fase 1: Intro & Context
  - Fase 2: HR Processen & Uitdagingen
  - Fase 3: Huidige Systemen & Tools
  - Fase 4: Gewenste Resultaten
  - Fase 5-11: Verdere implementatie details

### Technical
- FastAPI backend met WebSocket support
- Session persistence met JSON storage
- Multi-provider LLM integratie
- Responsive Tailwind CSS UI
- Real-time chat updates
- Error handling en fallback mechanismen

### Documentation
- README.md met installatie instructies
- ROADMAP.md met toekomstige features
- API documentatie
