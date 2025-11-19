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
            # Parse session_id from URL
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            session_id = query_params.get('session_id', [None])[0]
            
            # Load sessions from file
            sessions = load_sessions()
            
            if not session_id or session_id not in sessions:
                self.send_error(404, "Session not found")
                return
            
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
            message_content = data.get('content', '')
            
            session = sessions[session_id]
            
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
                    ai_message = """Welkom! Ik ben de Volentis HR Implementation Interview Agent.

Ik ga je helpen om:
✅ Een compleet implementatieplan voor de Volentis HR Agent te maken
✅ Een HR-verbeter-roadmap op te stellen

Laten we beginnen!

**Vraag 1:** In wat voor organisatie werk je? (sector, grootte, landen)"""
                else:
                    # Use Anthropic Claude
                    import anthropic
                    
                    api_key = os.getenv("ANTHROPIC_API_KEY")
                    if not api_key:
                        raise Exception("ANTHROPIC_API_KEY not configured in Vercel environment variables")
                    
                    client = anthropic.Anthropic(api_key=api_key)
                    
                    # Simple system prompt
                    system_prompt = """Je bent de Volentis HR Implementation Interview Agent.
Je helpt organisaties om de Volentis HR Agent te implementeren.
Stel ÉÉN vraag tegelijk. Wees zakelijk en helder."""
                    
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
                
                # Save updated session
                sessions[session_id] = session
                save_sessions(sessions)
                
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
                    "interview_complete": False
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
