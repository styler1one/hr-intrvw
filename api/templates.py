"""
Interview Templates Configuration
Defines different interview templates with varying depth and duration
"""

INTERVIEW_TEMPLATES = {
    "quick": {
        "id": "quick",
        "name": "Quick Interview",
        "description": "Snelle scan van de belangrijkste punten",
        "duration": "20 minuten",
        "total_fases": 5,
        "icon": "⚡",
        "fases": [1, 2, 3, 4, 5],
        "questions_per_fase": "2-3",
        "use_case": "Eerste kennismaking, quick scan, tijdsdruk"
    },
    "standard": {
        "id": "standard",
        "name": "Standard Interview",
        "description": "Volledig interview met alle essentiële onderdelen",
        "duration": "45 minuten",
        "total_fases": 11,
        "icon": "📋",
        "fases": list(range(1, 12)),
        "questions_per_fase": "5-8",
        "use_case": "Standaard implementatie, volledige analyse"
    },
    "extensive": {
        "id": "extensive",
        "name": "Extensive Interview",
        "description": "Diepgaand interview met extra detailvragen",
        "duration": "90 minuten",
        "total_fases": 15,
        "icon": "🔍",
        "fases": list(range(1, 16)),
        "questions_per_fase": "8-12",
        "use_case": "Complexe organisaties, enterprise implementaties"
    }
}

# Extended fase instructions for extensive template
EXTENDED_FASE_INSTRUCTIONS = {
    12: {
        "name": "Change Management & Training",
        "duration": "8 min",
        "instructions": """FASE 12 – CHANGE MANAGEMENT & TRAINING

BELANGRIJK: Stel vragen ÉÉN VOOR ÉÉN. Wacht op antwoord voordat je de volgende vraag stelt.

VRAGEN (stel ze één voor één):
1. Hoe gaan jullie medewerkers voorbereiden op de HR Agent?
2. Welke training is nodig voor verschillende gebruikersgroepen?
3. Wie wordt de interne champion/ambassadeur voor de HR Agent?
4. Hoe gaan jullie adoptie meten en stimuleren?
5. Wat is het communicatieplan naar de organisatie?
6. Zijn er eerdere change management ervaringen waar je van kunt leren?
7. Hoe ga je om met medewerkers die liever persoonlijk contact hebben?
8. Wat is het plan voor continue verbetering na go-live?

FASE AFSLUITING:
Na alle vragen: geef korte samenvatting (max 5 bullets) en vraag: "Klopt dit?"

Als bevestigd, output JSON met:
- change_management_approach
- training_plan
- communication_strategy
- adoption_metrics"""
    },
    13: {
        "name": "Technical Infrastructure",
        "duration": "8 min",
        "instructions": """FASE 13 – TECHNICAL INFRASTRUCTURE

BELANGRIJK: Stel vragen ÉÉN VOOR ÉÉN. Wacht op antwoord voordat je de volgende vraag stelt.

VRAGEN (stel ze één voor één):
1. Wat is jullie huidige IT infrastructuur? (cloud, on-premise, hybrid)
2. Welke security requirements zijn er? (ISO, NEN, GDPR)
3. Hoe is de netwerkarchitectuur? (VPN, firewalls, access controls)
4. Wat zijn de performance requirements? (response times, uptime)
5. Hoe gaan jullie data backups en disaster recovery regelen?
6. Zijn er API's nodig met andere systemen?
7. Wat is het deployment model? (SaaS, private cloud, on-premise)
8. Wie is verantwoordelijk voor technisch beheer?

FASE AFSLUITING:
Na alle vragen: geef korte samenvatting (max 5 bullets) en vraag: "Klopt dit?"

Als bevestigd, output JSON met:
- infrastructure_setup
- security_requirements
- integration_architecture
- deployment_model"""
    },
    14: {
        "name": "Governance & Compliance",
        "duration": "7 min",
        "instructions": """FASE 14 – GOVERNANCE & COMPLIANCE

BELANGRIJK: Stel vragen ÉÉN VOOR ÉÉN. Wacht op antwoord voordat je de volgende vraag stelt.

VRAGEN (stel ze één voor één):
1. Welke compliance eisen zijn er? (AVG, GDPR, sector-specifiek)
2. Hoe wordt data governance geregeld?
3. Wat zijn de audit requirements?
4. Wie is verantwoordelijk voor compliance monitoring?
5. Hoe gaan jullie om met data retention en verwijdering?
6. Zijn er specifieke privacy impact assessments nodig?
7. Wat is het proces voor security incidents?
8. Hoe worden toegangsrechten beheerd?

FASE AFSLUITING:
Na alle vragen: geef korte samenvatting (max 5 bullets) en vraag: "Klopt dit?"

Als bevestigd, output JSON met:
- compliance_requirements
- governance_framework
- data_policies
- audit_procedures"""
    },
    15: {
        "name": "Long-term Vision & Scaling",
        "duration": "7 min",
        "instructions": """FASE 15 – LONG-TERM VISION & SCALING

BELANGRIJK: Stel vragen ÉÉN VOOR ÉÉN. Wacht op antwoord voordat je de volgende vraag stelt.

VRAGEN (stel ze één voor één):
1. Wat is de lange termijn visie voor HR automation? (3-5 jaar)
2. Hoe zie je de HR Agent evolueren over tijd?
3. Welke extra use cases zie je in de toekomst?
4. Hoe ga je schalen naar andere landen/regio's?
5. Wat zijn de groeiplannen van de organisatie?
6. Hoe past de HR Agent in de bredere digitale transformatie?
7. Wat zijn de verwachte ROI en business case op lange termijn?
8. Hoe zorg je voor continue innovatie en verbetering?

FASE AFSLUITING:
Na alle vragen: geef korte samenvatting (max 5 bullets) en vraag: "Klopt dit?"

Als bevestigd, output JSON met:
- long_term_vision
- scaling_strategy
- future_use_cases
- roi_expectations"""
    }
}

def get_template(template_id: str) -> dict:
    """Get template configuration by ID"""
    return INTERVIEW_TEMPLATES.get(template_id, INTERVIEW_TEMPLATES["standard"])

def get_all_templates() -> dict:
    """Get all available templates"""
    return INTERVIEW_TEMPLATES

def get_fase_count(template_id: str) -> int:
    """Get total number of fases for a template"""
    template = get_template(template_id)
    return template["total_fases"]

def get_fase_list(template_id: str) -> list:
    """Get list of fase numbers for a template"""
    template = get_template(template_id)
    return template["fases"]
