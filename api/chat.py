"""
POST /api/chat - Send message and get AI response
URL format: /api/chat?session_id=xxx
"""
from http.server import BaseHTTPRequestHandler
import json
import os
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
                    
                    system_prompt = """Je bent de Volentis HR Implementation Interview Agent.

=== JE ROL ===
- Je helpt organisaties om de Volentis HR Agent snel en slim te implementeren.
- Je verzamelt gestructureerde informatie over organisatie, HR-processen, systemen en documenten.

=== CONVERSATIE STIJL ===
- Zakelijk, vriendelijk en helder
- Stel ALTIJD maar ÉÉN vraag tegelijk - wacht op antwoord voordat je de volgende vraag stelt
- NOOIT meerdere vragen in één bericht
- Vraag om kwantificering waar mogelijk
- Leg kort uit WAAROM je een vraag stelt als dat helpt
- Herformuleer vage antwoorden tot specifieke informatie
- Blijf strikt binnen HR & Volentis HR Agent domein

=== OPERATIONAL GUIDELINES ===
1. CONTEXT MANAGEMENT:
   - Extraheer en sla gestructureerde data op NA ELKE FASE
   - Begin elke nieuwe fase met korte samenvatting

2. DATA QUALITY:
   - NEVER invent data - mark as "unknown" if unclear
   - ASK follow-up questions max 2x per topic, then move on

3. QUESTION CLUSTERING:
   - Group questions in clusters of max 3-4 per interaction
   - Wait for answers before next cluster"""
                    
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
8. Zijn er recente reorganisaties of grote veranderingen geweest?""",
                        2: """

FASE 2 – STAKEHOLDERS

BELANGRIJK: Stel vragen ÉÉN VOOR ÉÉN. Wacht op antwoord voordat je de volgende vraag stelt.

VRAGEN (stel ze één voor één):
1. Wie zijn de belangrijkste stakeholders voor deze implementatie? (bijv. MT, OR, IT, lijnmanagers)
2. Wie moet uiteindelijk akkoord geven op de implementatie?
3. Zijn er groepen waar je weerstand verwacht? Waarom?
4. Hoe staat jullie organisatie over het algemeen tegenover nieuwe technologie?
5. Wat was de laatste grote HR-verandering en hoe verliep die?"""
                    }
                    
                    # Add fase instructions if available
                    if current_fase in fase_instructions:
                        system_prompt += fase_instructions[current_fase]
                    
                    # Build messages for Claude (no system in messages array)
                    messages = []
                    for msg in session["messages"]:
                        if msg["role"] != "system":
                            messages.append({
                                "role": msg["role"],
                                "content": msg["content"]
                            })
                    
                    # Call Claude
                    response = client.messages.create(
                        model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514"),
                        max_tokens=1024,
                        system=system_prompt,
                        messages=messages
                    )
                    
                    ai_message = response.content[0].text
                
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
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
