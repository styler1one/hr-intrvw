"""
POST /api/chat - Send message and get AI response
URL format: /api/chat?session_id=xxx
"""
from http.server import BaseHTTPRequestHandler
import json
import os
import re
from datetime import datetime
from urllib.parse import urlparse, parse_qs

# Import from config - use relative import for Vercel
try:
    from ._config import SESSIONS, get_template, save_sessions, load_sessions
except ImportError:
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from _config import SESSIONS, get_template, save_sessions, load_sessions

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST request to send chat message"""
        try:
            # Read request body - expect session data to be sent from frontend
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
            
            message_content = data.get('content', '')
            session = data.get('session', {})
            
            # If no session provided, create minimal session
            if not session:
                session = {
                    "messages": [],
                    "current_fase": 1,
                    "total_fases": 11
                }
            
            # Add user message
            session["messages"].append({
                "role": "user",
                "content": message_content,
                "timestamp": datetime.now().isoformat()
            })
            
            # Get AI response
            try:
                # Check if this is the first message (start)
                if message_content.lower() == 'start':
                    ai_message = """Hallo! Fijn dat je er bent. 👋

Ik ga je helpen om de Volentis HR Agent succesvol te implementeren in jouw organisatie. We gaan samen alle belangrijke informatie doornemen, zodat we een implementatiestrategie op maat kunnen maken.

Dit gesprek duurt ongeveer 45 minuten en je kunt altijd pauzeren als dat nodig is.

**Laten we beginnen met jouw organisatie:**

Kun je me vertellen in wat voor organisatie je werkt? Denk aan de sector, de grootte (aantal medewerkers) en in welke landen jullie actief zijn."""
                else:
                    # Use Anthropic Claude
                    from anthropic import Anthropic
                    
                    api_key = os.getenv("ANTHROPIC_API_KEY")
                    if not api_key:
                        raise Exception("ANTHROPIC_API_KEY not configured in Vercel environment variables")
                    
                    # Initialize client with minimal parameters
                    client = Anthropic(api_key=api_key)
                    
                    # Full system prompt with fase instructions
                    current_fase = session.get("current_fase", 1)
                    
                    system_prompt = """Je bent een ervaren HR-consultant van Volentis met 15+ jaar ervaring in:
- HR-transformatie en digitalisering bij middelgrote tot grote organisaties
- Change management bij complexe HR-implementaties
- Organisatieanalyse en procesoptimalisatie
- Stakeholder management op C-level en operationeel niveau
- HR-technologie en AI-implementaties

=== JOUW EXPERTISE ===
Je herkent direct HR-uitdagingen en weet welke vragen essentieel zijn. Je gebruikt consultancy frameworks zoals:
- McKinsey 7S voor organisatieanalyse
- ADKAR voor change management
- HR Value Chain voor procesoptimalisatie

Je spreekt de taal van verschillende sectoren (IT, Healthcare, Finance, Retail, Manufacturing) en begrijpt hun specifieke HR-uitdagingen.

=== GESPREKSSTIJL ===
- **Warm maar professioneel**: Bouw vertrouwen op, toon oprechte interesse
- **Nieuwsgierig en diepgaand**: Stel doorvragen bij oppervlakkige antwoorden
- **Empathisch**: Toon begrip voor uitdagingen en frustraties
- **Contextueel**: Bouw voort op eerdere antwoorden, maak verbindingen
- **Validatief**: Vat regelmatig samen en check begrip

=== BELANGRIJKE PRINCIPES ===
1. **Diepgang boven snelheid**: Stel ALTIJD doorvragen bij oppervlakkige antwoorden
   - Bij korte antwoorden (<10 woorden): "Kun je daar wat meer over vertellen?"
   - Bij vage antwoorden: "Kun je een concreet voorbeeld geven?"
   - Bij algemene uitspraken: "Hoe uit zich dat in de praktijk?"

2. **Vraag naar concrete voorbeelden en cijfers**:
   - "Hoeveel tijd kost dat per week/maand?"
   - "Kun je dat kwantificeren in aantal medewerkers/uren/kosten?"
   - "Hoe vaak komt dat voor?"

3. **Onderzoek de 'waarom' achter elk antwoord**:
   - "Wat is de belangrijkste reden daarvoor?"
   - "Waar komt dat door, denk je?"
   - "Wat maakt dat dit nu speelt?"

4. **Verbind antwoorden met eerdere informatie**:
   - "Je noemde eerder dat [X]. Hoe hangt dat samen met [Y]?"
   - "Dat sluit aan bij wat je zei over [X]..."
   - "Als ik het goed begrijp, [samenvatting]. Klopt dat?"

5. **Toon empathie voor uitdagingen**:
   - Bij frustratie: "Dat klinkt inderdaad frustrerend. Veel organisaties worstelen hiermee."
   - Bij tijdsdruk: "Tijdgebrek is een van de grootste uitdagingen in HR. Logisch dat dit speelt."
   - Bij complexiteit: "Dat herken ik. Dit is precies waar veel HR-teams mee kampen."

=== CONVERSATIE REGELS ===
- Stel ALTIJD maar ÉÉN vraag tegelijk - wacht op antwoord
- NOOIT meerdere vragen in één bericht
- Bij oppervlakkig antwoord: stel 1-2 doorvragen voordat je verder gaat
- Geef regelmatig (elke 3-4 vragen) een korte samenvatting
- Refereer aan eerdere antwoorden om context te tonen
- Leg kort uit WAAROM je een vraag stelt als dat helpt

=== OPERATIONAL GUIDELINES ===
1. CONTEXT MANAGEMENT:
   - Extraheer en sla gestructureerde data op NA ELKE FASE
   - Begin elke nieuwe fase met korte samenvatting van vorige fase

2. DATA QUALITY:
   - NEVER invent data - mark as "unknown" if unclear
   - ASK follow-up questions max 2x per topic, then move on
   - Validate inconsistencies: "Ik hoor je zeggen [X], maar eerder gaf je aan [Y]. Kun je dat toelichten?"

3. OUTPUT STRUCTURE:
   - Generate PARTIAL JSON after each fase
   - Each fase outputs only its own fields

=== OUTPUT FORMAT ===
After each fase, output JSON in this format:
```json
{
  "fase": number,
  "fase_name": "string",
  "confidence": "high | medium | low",
  "fields": {
    // only fields relevant to this fase
  }
}
```"""
                    
                    # Add fase-specific instructions
                    fase_instructions = {
                        1: """

FASE 1 – INTRO & CONTEXT

BELANGRIJK: Stel vragen ÉÉN VOOR ÉÉN. Wacht op antwoord voordat je de volgende vraag stelt.

VRAGEN (stel ze één voor één):
1. In wat voor organisatie werk je? (sector, grootte, aantal medewerkers, locaties)
2. Wat is jouw rol binnen HR?
3. Waarom kijken jullie nu naar een HR Agent zoals Volentis?
4. Wat hoop je over 6-12 maanden verbeterd te hebben?
5. Wat is de HR-strategie voor de komende 2-3 jaar?
6. Hoe zou je de organisatiecultuur beschrijven?
7. Hoe is de werkdruk binnen HR?
8. Zijn er recente reorganisaties of grote veranderingen geweest?

FASE AFSLUITING:
Na alle vragen: geef korte samenvatting (max 5 bullets) en vraag: "Klopt dit?"

Als bevestigd, output JSON met:
- org_profile
- hr_team_profile
- strategic_focus
- organizational_culture""",
                        2: """

FASE 2 – STAKEHOLDERS

BELANGRIJK: Stel vragen ÉÉN VOOR ÉÉN. Wacht op antwoord voordat je de volgende vraag stelt.

VRAGEN (stel ze één voor één):
1. Wie zijn de belangrijkste stakeholders voor deze implementatie? (bijv. MT, OR, IT, lijnmanagers)
2. Wie moet uiteindelijk akkoord geven op de implementatie?
3. Zijn er groepen waar je weerstand verwacht? Waarom?
4. Hoe staat jullie organisatie over het algemeen tegenover nieuwe technologie?
5. Wat was de laatste grote HR-verandering en hoe verliep die?

FASE AFSLUITING:
Na alle vragen: geef korte samenvatting (max 5 bullets) en vraag: "Klopt dit?"

Als bevestigd, output JSON met:
- stakeholders
- change_history
- change_readiness_preliminary"""
                    }
                    
                    # Add fase instructions if available
                    if current_fase in fase_instructions:
                        system_prompt += fase_instructions[current_fase]
                    
                    # Build messages for Claude (no system in messages array)
                    # Use last 10 messages to manage context window
                    messages = []
                    recent_messages = session["messages"][-10:] if len(session["messages"]) > 10 else session["messages"]
                    for msg in recent_messages:
                        if msg["role"] != "system":
                            messages.append({
                                "role": msg["role"],
                                "content": msg["content"]
                            })
                    
                    # Call Claude with retry logic for overload errors
                    import time
                    max_retries = 3
                    retry_delay = 2  # seconds
                    
                    for attempt in range(max_retries):
                        try:
                            response = client.messages.create(
                                model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514"),
                                max_tokens=1024,
                                system=system_prompt,
                                messages=messages
                            )
                            ai_message = response.content[0].text
                            break  # Success, exit retry loop
                        except Exception as e:
                            error_str = str(e)
                            # Check if it's an overload error (529)
                            if "overloaded" in error_str.lower() or "529" in error_str:
                                if attempt < max_retries - 1:
                                    # Wait before retry
                                    time.sleep(retry_delay * (attempt + 1))  # Exponential backoff
                                    continue
                                else:
                                    # Last attempt failed
                                    raise Exception(f"API overbelast na {max_retries} pogingen. Probeer het over een paar seconden opnieuw.")
                            else:
                                # Other error, don't retry
                                raise
                
                # Check for JSON output (fase complete)
                partial_json = self.extract_json(ai_message)
                fase_complete = partial_json is not None
                
                # If fase complete, increment fase counter
                if fase_complete:
                    session["current_fase"] = session.get("current_fase", 1) + 1
                    # Store fase data
                    if "fase_data" not in session:
                        session["fase_data"] = {}
                    if partial_json:
                        fase_num = partial_json.get("fase", current_fase)
                        session["fase_data"][f"fase_{fase_num}"] = partial_json
                
                # Add AI response to session
                session["messages"].append({
                    "role": "assistant",
                    "content": ai_message,
                    "timestamp": datetime.now().isoformat()
                })
                
                session["updated_at"] = datetime.now().isoformat()
                
                # Calculate progress
                total_fases = session.get("total_fases", 11)
                current_fase = session.get("current_fase", 1)
                progress = (current_fase / total_fases) * 100
                
                # Send response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.end_headers()
                
                response_data = {
                    "type": "agent_message",
                    "content": ai_message,
                    "progress": progress,
                    "fase": current_fase,
                    "fase_name": f"Fase {current_fase}",
                    "fase_complete": False,
                    "interview_complete": False,
                    "session": session  # Return updated session to frontend
                }
                
                self.wfile.write(json.dumps(response_data).encode())
                
            except Exception as e:
                import traceback
                error_details = traceback.format_exc()
                print(f"AI Error: {e}")
                print(f"Traceback: {error_details}")
                
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = {
                    "type": "error",
                    "message": f"AI Error: {str(e)}",
                    "details": error_details
                }
                self.wfile.write(json.dumps(error_response).encode())
                
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Chat Error: {e}")
            print(f"Traceback: {error_details}")
            
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": str(e),
                "details": error_details
            }).encode())
    
    def extract_json(self, text: str):
        """Extract JSON from agent response"""
        # Look for JSON code blocks
        json_pattern = r'```json\s*(.*?)\s*```'
        matches = re.findall(json_pattern, text, re.DOTALL)
        
        if matches:
            try:
                return json.loads(matches[0])
            except json.JSONDecodeError:
                pass
        
        # Try to find JSON without code blocks
        try:
            # Find anything that looks like JSON
            json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
            matches = re.findall(json_pattern, text, re.DOTALL)
            if matches:
                return json.loads(matches[-1])  # Take last match
        except:
            pass
        
        return None
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
