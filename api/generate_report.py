"""
POST /api/generate_report - Generate Implementation Readiness Report
Uses structured_data from session to create comprehensive report
"""
from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime

# Import fase definitions
try:
    from .fase_definitions import FASE_DEFINITIONS
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    from fase_definitions import FASE_DEFINITIONS

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST request to generate report"""
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
            
            # Get session data
            session = data.get('session', {})
            
            if not session:
                self.send_error_response(400, "No session data provided")
                return
            
            # Generate report
            report_content = self.generate_implementation_report(session)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"volentis_implementation_readiness_{timestamp}.md"
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'text/markdown')
            self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            self.wfile.write(report_content.encode('utf-8'))
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Report Generation Error: {e}")
            print(f"Traceback: {error_details}")
            self.send_error_response(500, str(e))
    
    def generate_implementation_report(self, session: dict) -> str:
        """Generate comprehensive implementation readiness report"""
        lines = []
        
        # Header
        lines.append("# 📋 Volentis HR Agent")
        lines.append("# Implementation Readiness Report")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append(f"**Rapport Datum**: {datetime.now().strftime('%d %B %Y')}")
        lines.append(f"**Interview Template**: {session.get('template_id', 'standard').title()}")
        lines.append(f"**Interview Voortgang**: {session.get('current_fase', 1)}/{session.get('total_fases', 11)} fases")
        lines.append("")
        
        # Get structured data
        structured_data = session.get('structured_data', {})
        
        # Executive Summary
        lines.extend(self.generate_executive_summary(structured_data, session))
        
        # Organisatieprofiel
        lines.extend(self.generate_organisation_profile(structured_data))
        
        # Technisch Landschap
        lines.extend(self.generate_technical_landscape(structured_data))
        
        # Content Inventory
        lines.extend(self.generate_content_inventory(structured_data))
        
        # Doelen & KPI's
        lines.extend(self.generate_goals_kpis(structured_data))
        
        # Risico's & Blockers
        lines.extend(self.generate_risks_blockers(structured_data))
        
        # Aanbevolen Aanpak
        lines.extend(self.generate_recommended_approach(structured_data))
        
        # Next Steps
        lines.extend(self.generate_next_steps())
        
        return "\n".join(lines)
    
    def generate_executive_summary(self, structured_data: dict, session: dict) -> list:
        """Generate executive summary section"""
        lines = []
        lines.append("## 📊 Executive Summary")
        lines.append("")
        
        # Extract key info from fase 1
        fase_1 = structured_data.get('fase_1', {}).get('data', {})
        
        org_name = fase_1.get('organisatie_naam', 'De organisatie')
        sector = fase_1.get('sector', 'onbekend')
        medewerkers = fase_1.get('aantal_medewerkers', 'onbekend aantal')
        
        lines.append(f"**Organisatie**: {org_name}")
        lines.append(f"**Sector**: {sector}")
        lines.append(f"**Omvang**: {medewerkers} medewerkers")
        lines.append("")
        
        # Keuze reden
        keuze_reden = fase_1.get('keuze_reden_hr_agent', '')
        if keuze_reden and keuze_reden != 'null':
            lines.append(f"**Reden voor HR Agent**: {keuze_reden}")
            lines.append("")
        
        # Doelen
        doelen = fase_1.get('doelen_6_12_maanden', '')
        if doelen and doelen != 'null':
            lines.append(f"**Doelen (6-12 maanden)**: {doelen}")
            lines.append("")
        
        lines.append("---")
        lines.append("")
        
        return lines
    
    def generate_organisation_profile(self, structured_data: dict) -> list:
        """Generate organisation profile section"""
        lines = []
        lines.append("## 🏢 Organisatieprofiel")
        lines.append("")
        
        fase_1 = structured_data.get('fase_1', {}).get('data', {})
        
        if fase_1:
            lines.append("### Algemeen")
            for key, value in fase_1.items():
                if value and value != 'null':
                    field_name = key.replace('_', ' ').title()
                    lines.append(f"- **{field_name}**: {value}")
            lines.append("")
        
        lines.append("---")
        lines.append("")
        
        return lines
    
    def generate_technical_landscape(self, structured_data: dict) -> list:
        """Generate technical landscape section"""
        lines = []
        lines.append("## 💻 Technisch Landschap")
        lines.append("")
        
        fase_4 = structured_data.get('fase_4', {}).get('data', {})
        
        if fase_4:
            # HRIS
            hris = fase_4.get('hris_bronsysteem', '')
            if hris and hris != 'null':
                lines.append(f"### HRIS Bronsysteem")
                lines.append(f"{hris}")
                lines.append("")
            
            # Andere systemen
            andere_systemen = fase_4.get('andere_relevante_systemen', '')
            if andere_systemen and andere_systemen != 'null':
                lines.append(f"### Andere Systemen")
                lines.append(f"{andere_systemen}")
                lines.append("")
            
            # Identity
            identity = fase_4.get('identity_systeem', '')
            if identity and identity != 'null':
                lines.append(f"### Identity Management")
                lines.append(f"{identity}")
                lines.append("")
            
            # Gewenste kanalen
            kanalen = fase_4.get('gewenste_kanalen_hr_agent', '')
            if kanalen and kanalen != 'null':
                lines.append(f"### Gewenste Kanalen voor HR Agent")
                lines.append(f"{kanalen}")
                lines.append("")
        else:
            lines.append("*Technische informatie nog niet verzameld*")
            lines.append("")
        
        lines.append("---")
        lines.append("")
        
        return lines
    
    def generate_content_inventory(self, structured_data: dict) -> list:
        """Generate content inventory section"""
        lines = []
        lines.append("## 📚 Content Inventory")
        lines.append("")
        
        fase_3 = structured_data.get('fase_3', {}).get('data', {})
        
        if fase_3:
            # Documenten
            documenten = fase_3.get('leidende_hr_documenten', '')
            if documenten and documenten != 'null':
                lines.append(f"### Leidende HR Documenten")
                lines.append(f"{documenten}")
                lines.append("")
            
            # Locaties
            locaties = fase_3.get('document_locaties', '')
            if locaties and locaties != 'null':
                lines.append(f"### Document Locaties")
                lines.append(f"{locaties}")
                lines.append("")
            
            # Processen
            processen = fase_3.get('primaire_processen_voor_agent', '')
            if processen and processen != 'null':
                lines.append(f"### Primaire Processen")
                lines.append(f"{processen}")
                lines.append("")
            
            # Complexiteit
            complex_processen = fase_3.get('complexe_processen_uitzonderingen', '')
            if complex_processen and complex_processen != 'null':
                lines.append(f"### Complexe Processen / Uitzonderingen")
                lines.append(f"⚠️ {complex_processen}")
                lines.append("")
        else:
            lines.append("*Content informatie nog niet verzameld*")
            lines.append("")
        
        lines.append("---")
        lines.append("")
        
        return lines
    
    def generate_goals_kpis(self, structured_data: dict) -> list:
        """Generate goals and KPIs section"""
        lines = []
        lines.append("## 🎯 Doelen & KPI's")
        lines.append("")
        
        fase_6 = structured_data.get('fase_6', {}).get('data', {})
        
        if fase_6:
            # Doelen
            doelen = fase_6.get('concrete_doelen', '')
            if doelen and doelen != 'null':
                lines.append(f"### Concrete Doelen")
                lines.append(f"{doelen}")
                lines.append("")
            
            # KPI's
            kpis = fase_6.get('huidige_kpis', '')
            if kpis and kpis != 'null':
                lines.append(f"### Huidige KPI's")
                lines.append(f"{kpis}")
                lines.append("")
            
            # Stakeholders
            stakeholders = fase_6.get('belangrijke_stakeholders', '')
            if stakeholders and stakeholders != 'null':
                lines.append(f"### Belangrijke Stakeholders")
                lines.append(f"{stakeholders}")
                lines.append("")
        else:
            lines.append("*Doelen en KPI's nog niet verzameld*")
            lines.append("")
        
        lines.append("---")
        lines.append("")
        
        return lines
    
    def generate_risks_blockers(self, structured_data: dict) -> list:
        """Generate risks and blockers section"""
        lines = []
        lines.append("## ⚠️ Risico's & Blockers")
        lines.append("")
        
        fase_5 = structured_data.get('fase_5', {}).get('data', {})
        fase_7 = structured_data.get('fase_7', {}).get('data', {})
        
        # Privacy & Compliance
        if fase_5:
            privacy_eisen = fase_5.get('extra_privacy_compliance_eisen', '')
            if privacy_eisen and privacy_eisen != 'null':
                lines.append(f"### Privacy & Compliance")
                lines.append(f"{privacy_eisen}")
                lines.append("")
            
            or_betrokkenheid = fase_5.get('or_betrokkenheid_ai', '')
            if or_betrokkenheid and or_betrokkenheid != 'null':
                lines.append(f"### OR / Medezeggenschap")
                lines.append(f"{or_betrokkenheid}")
                lines.append("")
        
        # Change risico's
        if fase_7:
            kritische_groepen = fase_7.get('kritische_groepen', '')
            if kritische_groepen and kritische_groepen != 'null':
                lines.append(f"### Kritische Groepen")
                lines.append(f"⚠️ {kritische_groepen}")
                lines.append("")
        
        if not fase_5 and not fase_7:
            lines.append("*Risico-informatie nog niet verzameld*")
            lines.append("")
        
        lines.append("---")
        lines.append("")
        
        return lines
    
    def generate_recommended_approach(self, structured_data: dict) -> list:
        """Generate recommended approach section"""
        lines = []
        lines.append("## 🚀 Aanbevolen Aanpak")
        lines.append("")
        
        lines.append("### Fase 1: Voorbereiding (Week 1-2)")
        lines.append("- [ ] Verzamel alle HR-documenten en policies")
        lines.append("- [ ] Identificeer en onboard key stakeholders")
        lines.append("- [ ] Setup technische toegang (HRIS, identity)")
        lines.append("- [ ] Plan kick-off meeting")
        lines.append("")
        
        lines.append("### Fase 2: Configuratie (Week 3-4)")
        lines.append("- [ ] Upload content naar HR Agent")
        lines.append("- [ ] Configureer integraties")
        lines.append("- [ ] Setup gebruikersgroepen en rechten")
        lines.append("- [ ] Test basis functionaliteit")
        lines.append("")
        
        lines.append("### Fase 3: Pilot (Week 5-6)")
        lines.append("- [ ] Selecteer pilot groep (10-20 gebruikers)")
        lines.append("- [ ] Train ambassadeurs")
        lines.append("- [ ] Start pilot met monitoring")
        lines.append("- [ ] Verzamel feedback en optimaliseer")
        lines.append("")
        
        lines.append("### Fase 4: Roll-out (Week 7-8)")
        lines.append("- [ ] Communiceer naar hele organisatie")
        lines.append("- [ ] Activeer voor alle gebruikers")
        lines.append("- [ ] Monitor gebruik en tevredenheid")
        lines.append("- [ ] Continuous improvement")
        lines.append("")
        
        lines.append("---")
        lines.append("")
        
        return lines
    
    def generate_next_steps(self) -> list:
        """Generate next steps section"""
        lines = []
        lines.append("## 📝 Volgende Stappen")
        lines.append("")
        
        lines.append("### Voor Klant")
        lines.append("1. **Review** dit rapport met key stakeholders")
        lines.append("2. **Verzamel** alle benodigde HR-documenten")
        lines.append("3. **Identificeer** technische contactpersoon voor integraties")
        lines.append("4. **Plan** kick-off meeting met Volentis")
        lines.append("5. **Communiceer** naar organisatie over komende implementatie")
        lines.append("")
        
        lines.append("### Voor Volentis")
        lines.append("1. **Analyseer** verzamelde data")
        lines.append("2. **Bereid voor** technische setup")
        lines.append("3. **Plan** implementatie roadmap")
        lines.append("4. **Schedule** kick-off meeting")
        lines.append("5. **Prepare** training materialen")
        lines.append("")
        
        lines.append("---")
        lines.append("")
        lines.append("*Dit rapport is gegenereerd op basis van het Volentis HR Agent Implementation Interview.*")
        lines.append("*Voor vragen of aanvullingen, neem contact op met uw Volentis consultant.*")
        
        return lines
    
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
