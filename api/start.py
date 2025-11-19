"""
POST /api/start - Start a new interview session
"""
from http.server import BaseHTTPRequestHandler
import json
import uuid
from datetime import datetime

# Import from config - use relative import for Vercel
try:
    from ._config import SESSIONS, get_template, save_sessions, load_sessions
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    from _config import SESSIONS, get_template, save_sessions, load_sessions

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST request to start session"""
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                body = self.rfile.read(content_length)
                data = json.loads(body.decode('utf-8'))
            else:
                data = {}
            
            template_id = data.get('template_id', 'standard')
            session_id = str(uuid.uuid4())
            template = get_template(template_id)
            
            # Create session
            session = {
                "session_id": session_id,
                "template_id": template_id,
                "template_name": template["name"],
                "total_fases": template["total_fases"],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "status": "in_progress",
                "current_fase": 1,
                "messages": [],
                "partial_data": {}
            }
            
            # Reload sessions to get latest state
            sessions = load_sessions()
            sessions[session_id] = session
            save_sessions(sessions)
            
            print(f"Session created: {session_id}")
            print(f"Total sessions: {len(sessions)}")
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            response = {
                "session_id": session_id,
                "template": template,
                "message": "Session created successfully"
            }
            
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
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
