"""
POST /api/suggestions - Generate context-aware answer suggestions
"""
from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Generate suggestions based on question and conversation context"""
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
            
            question = data.get('question', '')
            session = data.get('session', {})
            messages = session.get('messages', [])
            
            # Use Claude to generate context-aware suggestions
            try:
                from anthropic import Anthropic
                
                api_key = os.getenv("ANTHROPIC_API_KEY")
                if not api_key:
                    raise Exception("ANTHROPIC_API_KEY not configured")
                
                client = Anthropic(api_key=api_key)
                
                # Build context from conversation history
                context = "Conversatie tot nu toe:\n"
                for msg in messages[-6:]:  # Last 3 exchanges
                    role = "Interviewer" if msg["role"] == "assistant" else "Kandidaat"
                    context += f"{role}: {msg['content']}\n"
                
                # Create prompt for suggestions
                prompt = f"""Gebaseerd op deze conversatie:

{context}

De interviewer heeft zojuist gevraagd: "{question}"

Genereer 3-4 korte, relevante antwoord-suggesties (max 8 woorden per suggestie) die de kandidaat zou kunnen geven. 
De suggesties moeten:
- Relevant zijn voor de vraag
- Passen bij de context van het gesprek
- Variëren in detail/diepgang
- Natuurlijk klinken in het Nederlands

Geef alleen de suggesties, gescheiden door newlines, zonder nummering of extra tekst."""

                response = client.messages.create(
                    model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514"),
                    max_tokens=200,
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }]
                )
                
                # Parse suggestions from response
                suggestions_text = response.content[0].text.strip()
                suggestions = [s.strip() for s in suggestions_text.split('\n') if s.strip()]
                
                # Limit to 4 suggestions
                suggestions = suggestions[:4]
                
            except Exception as e:
                print(f"Error generating suggestions: {e}")
                # Fallback suggestions
                suggestions = [
                    "Ja, dat klopt",
                    "Nee, nog niet",
                    "Deels, laat me toelichten",
                    "Weet ik niet zeker"
                ]
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            response_data = {
                "suggestions": suggestions
            }
            
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            print(f"Suggestions Error: {e}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
