"""
POST /api/generate_checklist - Generate Implementation Checklist
Uses structured_data from session to create personalized checklist
"""
from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST request to generate checklist"""
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
            
            # Generate checklist
            checklist_content = self.generate_implementation_checklist(session)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"volentis_implementation_checklist_{timestamp}.md"
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'text/markdown')
            self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            self.wfile.write(checklist_content.encode('utf-8'))
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Checklist Generation Error: {e}")
            print(f"Traceback: {error_details}")
            self.send_error_response(500, str(e))
    
    def generate_implementation_checklist(self, session: dict) -> str:
        """Generate personalized implementation checklist"""
        lines = []
        
        # Header
        lines.append("# ✅ Volentis HR Agent")
        lines.append("# Implementation Checklist")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append(f"**Gegenereerd**: {datetime.now().strftime('%d %B %Y')}")
        
        # Get structured data
        structured_data = session.get('structured_data', {})
        fase_1 = structured_data.get('fase_1', {}).get('data', {})
        fase_3 = structured_data.get('fase_3', {}).get('data', {})
        fase_4 = structured_data.get('fase_4', {}).get('data', {})
        fase_5 = structured_data.get('fase_5', {}).get('data', {})
        fase_7 = structured_data.get('fase_7', {}).get('data', {})
        
        org_name = fase_1.get('organisatie_naam', 'Organisatie')
        lines.append(f"**Organisatie**: {org_name}")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # Category 1: Pre-Implementation
        lines.extend(self.generate_pre_implementation(fase_1, fase_3, fase_5))
        
        # Category 2: Technical Setup
        lines.extend(self.generate_technical_setup(fase_4, fase_5))
        
        # Category 3: Content Preparation
        lines.extend(self.generate_content_preparation(fase_3))
        
        # Category 4: Stakeholder Engagement
        lines.extend(self.generate_stakeholder_engagement(fase_1, fase_7))
        
        # Category 5: Go-Live Checklist
        lines.extend(self.generate_golive_checklist(fase_7))
        
        # Category 6: Post-Launch Monitoring
        lines.extend(self.generate_postlaunch_monitoring())
        
        # Footer
        lines.append("---")
        lines.append("")
        lines.append("## 📊 Voortgang Tracking")
        lines.append("")
        lines.append("**Totaal taken**: Zie checkboxes hierboven")
        lines.append("**Geschatte doorlooptijd**: 6-8 weken")
        lines.append("**Verantwoordelijke**: [Naam invullen]")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("*Deze checklist is gepersonaliseerd op basis van het Volentis HR Agent Implementation Interview.*")
        lines.append("*Update regelmatig en deel met het implementatieteam.*")
        
        return "\n".join(lines)
    
    def generate_pre_implementation(self, fase_1: dict, fase_3: dict, fase_5: dict) -> list:
        """Generate pre-implementation tasks"""
        lines = []
        lines.append("## 📋 1. Pre-Implementation Tasks")
        lines.append("")
        lines.append("### Organisatie & Planning")
        lines.append("- [ ] Kick-off meeting gepland met stakeholders")
        lines.append("- [ ] Project sponsor geïdentificeerd en committed")
        lines.append("- [ ] Implementatieteam samengesteld")
        lines.append("- [ ] Project timeline en milestones vastgesteld")
        lines.append("- [ ] Budget goedgekeurd")
        lines.append("")
        
        # Personalized based on data
        if fase_5.get('or_betrokkenheid_ai'):
            lines.append("### Medezeggenschap & Compliance")
            lines.append(f"- [ ] OR geïnformeerd over AI-implementatie")
            if 'goedkeuring' in str(fase_5.get('or_betrokkenheid_ai', '')).lower():
                lines.append(f"- [ ] OR goedkeuring verkregen")
            lines.append("")
        
        if fase_5.get('dpo_privacy_officer'):
            lines.append("### Privacy & Security")
            lines.append(f"- [ ] DPO/Privacy Officer betrokken")
            lines.append(f"- [ ] Privacy Impact Assessment uitgevoerd")
            lines.append("")
        
        lines.append("### Documentatie")
        
        documenten = fase_3.get('leidende_hr_documenten', '')
        if documenten and documenten != 'null':
            lines.append(f"- [ ] Alle HR-documenten verzameld ({documenten})")
        else:
            lines.append(f"- [ ] Alle HR-documenten verzameld")
        
        lines.append("- [ ] Document eigenaren geïdentificeerd")
        lines.append("- [ ] Update-frequentie per document vastgesteld")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        return lines
    
    def generate_technical_setup(self, fase_4: dict, fase_5: dict) -> list:
        """Generate technical setup tasks"""
        lines = []
        lines.append("## 💻 2. Technical Setup")
        lines.append("")
        
        # HRIS Integration
        hris = fase_4.get('hris_bronsysteem', '')
        if hris and hris != 'null':
            lines.append(f"### {hris} Integratie")
            lines.append(f"- [ ] API toegang tot {hris} geregeld")
            lines.append(f"- [ ] Test-omgeving {hris} beschikbaar")
            lines.append(f"- [ ] Data mapping {hris} → HR Agent gedaan")
        else:
            lines.append(f"### HRIS Integratie")
            lines.append(f"- [ ] API toegang tot HRIS geregeld")
            lines.append(f"- [ ] Test-omgeving HRIS beschikbaar")
        
        lines.append("")
        
        # Identity
        identity = fase_4.get('identity_systeem', '')
        if identity and identity != 'null':
            lines.append(f"### Identity Management ({identity})")
            lines.append(f"- [ ] SSO configuratie met {identity}")
            lines.append(f"- [ ] Gebruikersgroepen aangemaakt")
            lines.append(f"- [ ] Toegangsrechten gedefinieerd")
        else:
            lines.append(f"### Identity Management")
            lines.append(f"- [ ] SSO configuratie")
            lines.append(f"- [ ] Gebruikersgroepen aangemaakt")
        
        lines.append("")
        
        # Channels
        kanalen = fase_4.get('gewenste_kanalen_hr_agent', '')
        if kanalen and kanalen != 'null':
            lines.append(f"### Kanalen Setup")
            lines.append(f"- [ ] HR Agent beschikbaar in: {kanalen}")
            lines.append(f"- [ ] Integratie getest per kanaal")
        
        lines.append("")
        
        # Security
        if fase_5.get('extra_privacy_compliance_eisen'):
            lines.append(f"### Security & Compliance")
            eisen = fase_5.get('extra_privacy_compliance_eisen', '')
            lines.append(f"- [ ] Compliance vereisten geïmplementeerd: {eisen}")
            lines.append(f"- [ ] Security audit uitgevoerd")
            lines.append("")
        
        lines.append("### Infrastructure")
        lines.append("- [ ] Productie-omgeving opgezet")
        lines.append("- [ ] Backup & disaster recovery geregeld")
        lines.append("- [ ] Monitoring & logging geconfigureerd")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        return lines
    
    def generate_content_preparation(self, fase_3: dict) -> list:
        """Generate content preparation tasks"""
        lines = []
        lines.append("## 📚 3. Content Preparation")
        lines.append("")
        
        lines.append("### Content Upload")
        
        documenten = fase_3.get('leidende_hr_documenten', '')
        if documenten and documenten != 'null':
            for doc in documenten.split(','):
                doc = doc.strip()
                lines.append(f"- [ ] {doc} geüpload en gevalideerd")
        else:
            lines.append(f"- [ ] Alle HR-documenten geüpload")
        
        lines.append("")
        
        lines.append("### Content Quality")
        lines.append("- [ ] Alle documenten up-to-date")
        lines.append("- [ ] Inconsistenties opgelost")
        lines.append("- [ ] FAQ's toegevoegd voor veelgestelde vragen")
        lines.append("- [ ] Voorbeelden en use cases toegevoegd")
        lines.append("")
        
        # Processen
        processen = fase_3.get('primaire_processen_voor_agent', '')
        if processen and processen != 'null':
            lines.append("### Proces Documentatie")
            lines.append(f"- [ ] Processen gedocumenteerd: {processen}")
            lines.append(f"- [ ] Proces-flows toegevoegd waar relevant")
            lines.append("")
        
        # Complexiteit
        complex_processen = fase_3.get('complexe_processen_uitzonderingen', '')
        if complex_processen and complex_processen != 'null':
            lines.append("### Uitzonderingen & Edge Cases")
            lines.append(f"- [ ] Complexe gevallen gedocumenteerd: {complex_processen}")
            lines.append(f"- [ ] Escalatie-procedures gedefinieerd")
            lines.append("")
        
        lines.append("### Content Testing")
        lines.append("- [ ] Test-vragen gesteld aan HR Agent")
        lines.append("- [ ] Antwoorden gevalideerd door HR-experts")
        lines.append("- [ ] Content iteraties gedaan op basis van feedback")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        return lines
    
    def generate_stakeholder_engagement(self, fase_1: dict, fase_7: dict) -> list:
        """Generate stakeholder engagement tasks"""
        lines = []
        lines.append("## 👥 4. Stakeholder Engagement")
        lines.append("")
        
        lines.append("### Communicatie")
        
        comm_middelen = fase_7.get('effectieve_communicatiemiddelen', '')
        if comm_middelen and comm_middelen != 'null':
            lines.append(f"- [ ] Communicatieplan opgesteld (via: {comm_middelen})")
        else:
            lines.append(f"- [ ] Communicatieplan opgesteld")
        
        lines.append("- [ ] Aankondiging HR Agent naar organisatie")
        lines.append("- [ ] Benefits en use cases gecommuniceerd")
        lines.append("- [ ] FAQ voor medewerkers beschikbaar")
        lines.append("")
        
        # Ambassadeurs
        ambassadeurs = fase_7.get('potentiele_ambassadeurs', '')
        if ambassadeurs and ambassadeurs != 'null':
            lines.append("### Ambassadeurs")
            lines.append(f"- [ ] Ambassadeurs geïdentificeerd: {ambassadeurs}")
            lines.append(f"- [ ] Ambassadeurs getraind")
            lines.append(f"- [ ] Ambassadeurs actief in hun teams")
            lines.append("")
        
        # Training
        training = fase_7.get('training_behoeften', '')
        if training and training != 'null':
            lines.append("### Training")
            lines.append(f"- [ ] Training materiaal voorbereid: {training}")
            lines.append(f"- [ ] Training sessies gepland")
            lines.append(f"- [ ] Managers getraind")
            lines.append("")
        
        # Kritische groepen
        kritisch = fase_7.get('kritische_groepen', '')
        if kritisch and kritisch != 'null':
            lines.append("### Change Management")
            lines.append(f"- [ ] Extra aandacht voor: {kritisch}")
            lines.append(f"- [ ] Specifieke support geregeld voor kritische groepen")
            lines.append("")
        
        lines.append("### Pilot")
        lines.append("- [ ] Pilot groep geselecteerd (10-20 gebruikers)")
        lines.append("- [ ] Pilot kick-off gedaan")
        lines.append("- [ ] Pilot feedback verzameld")
        lines.append("- [ ] Aanpassingen gedaan op basis van pilot")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        return lines
    
    def generate_golive_checklist(self, fase_7: dict) -> list:
        """Generate go-live checklist"""
        lines = []
        lines.append("## 🚀 5. Go-Live Checklist")
        lines.append("")
        
        lines.append("### Pre-Launch (Week voor go-live)")
        lines.append("- [ ] Alle technische tests geslaagd")
        lines.append("- [ ] Content volledig en gevalideerd")
        lines.append("- [ ] Support team getraind")
        lines.append("- [ ] Escalatie-procedures getest")
        lines.append("- [ ] Backup plan gereed")
        lines.append("")
        
        lines.append("### Launch Day")
        lines.append("- [ ] HR Agent geactiveerd voor alle gebruikers")
        lines.append("- [ ] Monitoring actief")
        lines.append("- [ ] Support team stand-by")
        lines.append("- [ ] Communicatie verstuurd naar organisatie")
        lines.append("- [ ] Ambassadeurs actief in teams")
        lines.append("")
        
        lines.append("### Week 1 Post-Launch")
        lines.append("- [ ] Dagelijkse monitoring van gebruik")
        lines.append("- [ ] Snelle fixes voor acute problemen")
        lines.append("- [ ] Feedback verzamelen van early adopters")
        lines.append("- [ ] Support tickets analyseren")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        return lines
    
    def generate_postlaunch_monitoring(self) -> list:
        """Generate post-launch monitoring tasks"""
        lines = []
        lines.append("## 📊 6. Post-Launch Monitoring")
        lines.append("")
        
        lines.append("### Week 2-4")
        lines.append("- [ ] Gebruiksstatistieken analyseren")
        lines.append("- [ ] Tevredenheidsmetingen uitvoeren")
        lines.append("- [ ] Content gaps identificeren")
        lines.append("- [ ] Quick wins implementeren")
        lines.append("")
        
        lines.append("### Maand 2-3")
        lines.append("- [ ] Uitgebreide gebruikersonderzoek")
        lines.append("- [ ] ROI berekening maken")
        lines.append("- [ ] Optimalisaties doorvoeren")
        lines.append("- [ ] Success stories verzamelen")
        lines.append("")
        
        lines.append("### Continuous Improvement")
        lines.append("- [ ] Maandelijkse review meetings")
        lines.append("- [ ] Content updates op basis van nieuwe vragen")
        lines.append("- [ ] Feature requests prioriteren")
        lines.append("- [ ] Quarterly business review met Volentis")
        lines.append("")
        lines.append("---")
        lines.append("")
        
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
