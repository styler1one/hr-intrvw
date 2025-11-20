"""Test Implementation Checklist generation"""
import requests
import json

# Use same test data as report
test_session = {
    "template_id": "standard",
    "created_at": "2025-11-20T15:00:00",
    "updated_at": "2025-11-20T16:00:00",
    "current_fase": 7,
    "total_fases": 11,
    "messages": [],
    "structured_data": {
        "fase_1": {
            "fase_name": "Organisatie Context",
            "data": {
                "organisatie_naam": "TechStart BV",
                "sector": "HR Technology / SaaS",
                "aantal_medewerkers": 85
            }
        },
        "fase_3": {
            "fase_name": "HR-Processen & Policies",
            "data": {
                "leidende_hr_documenten": "CAO, Personeelshandboek, Arbeidsvoorwaardenreglement",
                "document_locaties": "SharePoint, Google Drive",
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
                "gewenste_kanalen_hr_agent": "Microsoft Teams, Intranet"
            }
        },
        "fase_5": {
            "fase_name": "Beveiliging, Privacy & Compliance",
            "data": {
                "extra_privacy_compliance_eisen": "ISO 27001 certificering vereist",
                "dpo_privacy_officer": "Ja, Maria Jansen",
                "or_betrokkenheid_ai": "OR moet geïnformeerd worden, geen formele goedkeuring nodig"
            }
        },
        "fase_7": {
            "fase_name": "Change & Adoptie",
            "data": {
                "effectieve_communicatiemiddelen": "Teams, Email, Intranet",
                "kritische_groepen": "Oudere medewerkers minder tech-savvy",
                "potentiele_ambassadeurs": "HR Business Partner, 2 team leads",
                "training_behoeften": "Korte demo voor managers"
            }
        }
    }
}

print("Testing Implementation Checklist generation...")
print("=" * 60)

response = requests.post(
    "https://hr.agentboss.nl/api/generate_checklist",
    json={"session": test_session}
)

print(f"Status: {response.status_code}")

if response.status_code == 200:
    # Save checklist
    with open("test_implementation_checklist.md", "w", encoding="utf-8") as f:
        f.write(response.text)
    
    print("✅ Checklist generated successfully!")
    print(f"📄 Saved to: test_implementation_checklist.md")
    print(f"📏 Length: {len(response.text)} characters")
    
    # Count checkboxes
    checkbox_count = response.text.count("- [ ]")
    print(f"✅ Total checkboxes: {checkbox_count}")
    
    print("")
    print("Preview (first 1000 chars):")
    print("=" * 60)
    print(response.text[:1000])
    print("=" * 60)
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
