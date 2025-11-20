"""Test Implementation Readiness Report generation"""
import requests
import json

# Test data with comprehensive structured_data
test_session = {
    "template_id": "standard",
    "created_at": "2025-11-20T15:00:00",
    "updated_at": "2025-11-20T16:00:00",
    "current_fase": 6,
    "total_fases": 11,
    "messages": [],
    "structured_data": {
        "fase_1": {
            "fase_name": "Organisatie Context",
            "data": {
                "organisatie_naam": "TechStart BV",
                "sector": "HR Technology / SaaS",
                "aantal_medewerkers": 85,
                "landen_actief": "Nederland, België",
                "hr_team_grootte": 3,
                "hr_rol_geinterviewde": "Head of People",
                "keuze_reden_hr_agent": "20 uur per week kwijt aan repetitieve HR-vragen",
                "belangrijkste_hr_uitdagingen": "Verlofvragen, onboarding FAQ, arbeidsvoorwaarden",
                "doelen_6_12_maanden": "75% minder tijd aan repetitieve vragen, turnover van 18% naar 12%",
                "hr_strategie_2_3_jaar": "Groeien naar 150 medewerkers, focus op schaalbare processen"
            }
        },
        "fase_3": {
            "fase_name": "HR-Processen & Policies",
            "data": {
                "leidende_hr_documenten": "CAO, Personeelshandboek, Arbeidsvoorwaardenreglement",
                "document_locaties": "SharePoint, Google Drive",
                "update_frequentie_documenten": "Jaarlijks, bij CAO-wijzigingen",
                "primaire_processen_voor_agent": "Verlof, verzuim, onboarding, arbeidsvoorwaarden",
                "complexe_processen_uitzonderingen": "Internationale medewerkers hebben andere regelingen"
            }
        },
        "fase_4": {
            "fase_name": "HR-Systemen & Integraties",
            "data": {
                "hris_bronsysteem": "AFAS",
                "andere_relevante_systemen": "Payroll (Nmbrs), Planning (Shiftbase)",
                "identity_systeem": "Azure AD / Entra ID",
                "huidige_login_methode": "Microsoft SSO",
                "gewenste_kanalen_hr_agent": "Microsoft Teams, Intranet",
                "it_contactpersoon": "Jan de Vries (IT Manager)"
            }
        },
        "fase_5": {
            "fase_name": "Beveiliging, Privacy & Compliance",
            "data": {
                "extra_privacy_compliance_eisen": "ISO 27001 certificering vereist",
                "verboden_datacategorieen": "Medische gegevens mogen niet in chat",
                "dpo_privacy_officer": "Ja, Maria Jansen",
                "or_betrokkenheid_ai": "OR moet geïnformeerd worden, geen formele goedkeuring nodig",
                "eerdere_ai_chatbot_trajecten": "Nee, eerste AI-implementatie"
            }
        },
        "fase_6": {
            "fase_name": "Doelen, KPI's & Succescriteria",
            "data": {
                "persoonlijke_succes_definitie": "Meer tijd voor strategisch werk",
                "concrete_doelen": "75% reductie repetitieve vragen, 15 uur per week besparen",
                "huidige_kpis": "Response tijd, aantal tickets, medewerkerstevredenheid",
                "tevredenheid_targets": "eNPS van 7.2 naar 8.5",
                "belangrijke_stakeholders": "CEO, HR-team, IT Manager",
                "baseline_metingen": "Ja, 20 uur/week aan repetitieve vragen"
            }
        },
        "fase_7": {
            "fase_name": "Change & Adoptie",
            "data": {
                "gebruikelijke_introductie_methode": "Teams announcements, lunch & learn sessies",
                "effectieve_communicatiemiddelen": "Teams, Email, Intranet",
                "kritische_groepen": "Oudere medewerkers minder tech-savvy",
                "potentiele_ambassadeurs": "HR Business Partner, 2 team leads",
                "training_behoeften": "Korte demo voor managers",
                "change_management_capaciteit": "Beperkt, focus op quick wins"
            }
        }
    }
}

print("Testing Implementation Readiness Report generation...")
print("=" * 60)

response = requests.post(
    "https://hr.agentboss.nl/api/generate_report",
    json={"session": test_session}
)

print(f"Status: {response.status_code}")

if response.status_code == 200:
    # Save report
    with open("test_implementation_report.md", "w", encoding="utf-8") as f:
        f.write(response.text)
    
    print("✅ Report generated successfully!")
    print(f"📄 Saved to: test_implementation_report.md")
    print(f"📏 Length: {len(response.text)} characters")
    print("")
    print("Preview (first 1000 chars):")
    print("=" * 60)
    print(response.text[:1000])
    print("=" * 60)
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
