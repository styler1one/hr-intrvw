"""
POST /api/export - Export interview data in various formats
Supports: JSON, CSV, Markdown
"""
from http.server import BaseHTTPRequestHandler
import json
import csv
from io import StringIO
from datetime import datetime
from urllib.parse import parse_qs, urlparse

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST request to export interview data"""
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
            
            # Get session data
            session = data.get('session', {})
            export_format = data.get('format', 'json').lower()
            
            if not session:
                self.send_error_response(400, "No session data provided")
                return
            
            # Generate export based on format
            if export_format == 'json':
                content, content_type, filename = self.export_json(session)
            elif export_format == 'csv':
                content, content_type, filename = self.export_csv(session)
            elif export_format == 'md' or export_format == 'markdown':
                content, content_type, filename = self.export_markdown(session)
            else:
                self.send_error_response(400, f"Unsupported format: {export_format}")
                return
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            self.wfile.write(content.encode('utf-8'))
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Export Error: {e}")
            print(f"Traceback: {error_details}")
            self.send_error_response(500, str(e))
    
    def export_json(self, session: dict) -> tuple:
        """Export as JSON"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"volentis_interview_{timestamp}.json"
        
        # Create clean export data
        export_data = {
            "interview_metadata": {
                "template": session.get("template_id", "standard"),
                "started_at": session.get("created_at", ""),
                "completed_at": session.get("updated_at", ""),
                "total_fases": session.get("total_fases", 11),
                "current_fase": session.get("current_fase", 1),
                "total_messages": len(session.get("messages", []))
            },
            "structured_data": session.get("structured_data", {}),
            "conversation": [
                {
                    "role": msg.get("role"),
                    "content": msg.get("content"),
                    "timestamp": msg.get("timestamp")
                }
                for msg in session.get("messages", [])
            ],
            "statistics": {
                "followup_stats": session.get("followup_stats", {}),
                "progress_percentage": (session.get("current_fase", 1) / session.get("total_fases", 11)) * 100
            }
        }
        
        content = json.dumps(export_data, indent=2, ensure_ascii=False)
        return content, 'application/json', filename
    
    def export_csv(self, session: dict) -> tuple:
        """Export as CSV (flattened structured data)"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"volentis_interview_{timestamp}.csv"
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow(['Fase', 'Veld', 'Waarde'])
        
        # Write structured data
        structured_data = session.get("structured_data", {})
        for fase_key, fase_data in structured_data.items():
            fase_name = fase_data.get("fase_name", fase_key)
            data = fase_data.get("data", {})
            
            for field, value in data.items():
                # Convert lists/dicts to string
                if isinstance(value, (list, dict)):
                    value = json.dumps(value, ensure_ascii=False)
                writer.writerow([fase_name, field, value])
        
        content = output.getvalue()
        return content, 'text/csv', filename
    
    def export_markdown(self, session: dict) -> tuple:
        """Export as Markdown"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"volentis_interview_{timestamp}.md"
        
        lines = []
        lines.append("# Volentis HR Agent - Interview Export")
        lines.append("")
        lines.append(f"**Export Datum**: {datetime.now().strftime('%d %B %Y, %H:%M')}")
        lines.append(f"**Template**: {session.get('template_id', 'standard').title()}")
        lines.append(f"**Voortgang**: {session.get('current_fase', 1)}/{session.get('total_fases', 11)} fases")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # Structured data per fase
        structured_data = session.get("structured_data", {})
        if structured_data:
            lines.append("## 📊 Verzamelde Informatie")
            lines.append("")
            
            for fase_key in sorted(structured_data.keys()):
                fase_data = structured_data[fase_key]
                fase_name = fase_data.get("fase_name", fase_key)
                data = fase_data.get("data", {})
                
                lines.append(f"### {fase_name}")
                lines.append("")
                
                for field, value in data.items():
                    # Format field name
                    field_display = field.replace('_', ' ').title()
                    
                    # Format value
                    if value is None or value == "null":
                        value_display = "*Niet ingevuld*"
                    elif isinstance(value, list):
                        value_display = ", ".join(str(v) for v in value)
                    elif isinstance(value, dict):
                        value_display = json.dumps(value, indent=2, ensure_ascii=False)
                    else:
                        value_display = str(value)
                    
                    lines.append(f"- **{field_display}**: {value_display}")
                
                lines.append("")
        
        # Conversation summary
        messages = session.get("messages", [])
        if messages:
            lines.append("## 💬 Gesprek Samenvatting")
            lines.append("")
            lines.append(f"**Totaal berichten**: {len(messages)}")
            
            followup_stats = session.get("followup_stats", {})
            if followup_stats:
                total_q = followup_stats.get("total_questions", 0)
                followup_q = followup_stats.get("followup_questions", 0)
                if total_q > 0:
                    percentage = (followup_q / total_q) * 100
                    lines.append(f"**Doorvraag-ratio**: {followup_q}/{total_q} ({percentage:.0f}%)")
            
            lines.append("")
        
        content = "\n".join(lines)
        return content, 'text/markdown', filename
    
    def send_error_response(self, status_code: int, message: str):
        """Send error response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        error_data = {
            "error": message,
            "status": status_code
        }
        self.wfile.write(json.dumps(error_data).encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
