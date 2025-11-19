"""
GET /api/templates - Return all interview templates
"""
from http.server import BaseHTTPRequestHandler
import json

# Import from config - use relative import for Vercel
try:
    from ._config import INTERVIEW_TEMPLATES
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    from _config import INTERVIEW_TEMPLATES

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET request for templates"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        response = {
            "templates": INTERVIEW_TEMPLATES
        }
        
        self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
