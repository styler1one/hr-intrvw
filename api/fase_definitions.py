"""
Fase-definities voor de Volentis HR Agent Interview
Elke fase heeft duidelijke doelen, kernvragen, output fields en advies-haakjes
"""

FASE_DEFINITIONS = {
    1: {
        "fase_number": 1,
        "fase_name": "Organisatie Context",
        "doel": "Begrijpen wie de klant is, wat HR vandaag moet leveren en waarom ze voor de HR Agent hebben gekozen",
        "kern_vragen": [
            "In wat voor organisatie werk je? (sector, grootte, aantal medewerkers, locaties)",
            "Wat is jouw rol binnen HR en hoe is het HR-team opgebouwd?",
            "Wat was voor jullie de belangrijkste reden om voor de Volentis HR Agent te kiezen?",
            "Welke specifieke HR-uitdagingen hopen jullie hiermee op te lossen?",
            "Wat hoop je over 6-12 maanden verbeterd te hebben met de HR Agent?",
            "Wat is de bredere HR-strategie voor de komende 2-3 jaar waar de HR Agent in past?"
        ],
        "output_fields": [
            "organisatie_naam",
            "sector",
            "aantal_medewerkers",
            "landen_actief",
            "hr_team_grootte",
            "hr_rol_geinterviewde",
            "keuze_reden_hr_agent",
            "belangrijkste_hr_uitdagingen",
            "doelen_6_12_maanden",
            "hr_strategie_2_3_jaar"
        ],
        "advies_haakje": "Identificeer strategische HR-thema's waar Volentis breder kan adviseren (transformatie, analytics, employee experience)"
    },
    
    2: {
        "fase_number": 2,
        "fase_name": "Huidige HR-Service & Ticketing",
        "doel": "Begrijpen hoeveel 'noise' er nu is en waar de HR Agent de grootste impact heeft",
        "kern_vragen": [
            "Hoe komen HR-vragen nu binnen? (e-mail, telefoon, portaal, ticketsysteem, Teams)",
            "Hebben jullie cijfers over hoeveel HR-vragen of tickets er per maand zijn?",
            "Welke 5-10 vraagtypen komen het meest voor? (verlof, verzuim, contract, salaris, etc.)",
            "Hoe lang duurt het gemiddeld voordat medewerkers een antwoord krijgen?",
            "Waar klaagt men intern het meest over in contact met HR?",
            "Zijn er piekperiodes in HR-vragen? (CAO-wijzigingen, beoordelingen, jaarwissel)",
            "Hoeveel tijd besteedt het HR-team nu per week aan het beantwoorden van repetitieve vragen?"
        ],
        "output_fields": [
            "hr_vragen_kanalen",
            "volume_vragen_per_maand",
            "top_vraagtypen",
            "gemiddelde_responstijd",
            "belangrijkste_klachten",
            "piekperiodes",
            "tijd_per_week_repetitieve_vragen"
        ],
        "advies_haakje": "Bereken ROI van HR Agent op basis van tijdsbesparing en verbeterde employee experience"
    },
    
    3: {
        "fase_number": 3,
        "fase_name": "HR-Processen & Policies",
        "doel": "Inventariseren welke content en processen de HR Agent moet kennen",
        "kern_vragen": [
            "Welke HR-documenten en policies zijn leidend? (CAO, handboek, protocols)",
            "Waar staan deze documenten nu opgeslagen? (SharePoint, intranet, AFAS, fileshares)",
            "Hoe vaak worden deze documenten geüpdatet en wie is eigenaar?",
            "Zijn er grote verschillen tussen groepen medewerkers? (per land, cao, afdeling)",
            "Welke processen moet de HR Agent zeker ondersteunen? (verlof, verzuim, declaraties, etc.)",
            "Zijn er processen waarvan je nu al weet: die zijn complex, met veel uitzonderingen?"
        ],
        "output_fields": [
            "leidende_hr_documenten",
            "document_locaties",
            "update_frequentie_documenten",
            "document_eigenaren",
            "verschillen_tussen_groepen",
            "primaire_processen_voor_agent",
            "complexe_processen_uitzonderingen"
        ],
        "advies_haakje": "Identificeer content-gaps en documentatie-verbeteringen voor bredere HR-digitalisering"
    },
    
    4: {
        "fase_number": 4,
        "fase_name": "HR-Systemen & Integraties",
        "doel": "Technische omgeving begrijpen om implementatie te versnellen",
        "kern_vragen": [
            "Welke HR-systemen gebruiken jullie nu als bronsysteem? (AFAS, SAP, Workday, etc.)",
            "Welke andere systemen zijn relevant voor HR-processen? (payroll, planning, LMS, verzuim)",
            "Is er een centraal identity systeem? (Azure AD / Entra ID)",
            "Hoe loggen medewerkers nu in voor HR-diensten?",
            "In welke systemen ziet u het liefst dat de HR Agent beschikbaar komt? (Teams, intranet, portal)",
            "Is er een IT-contactpersoon voor integraties en beveiliging?"
        ],
        "output_fields": [
            "hris_bronsysteem",
            "andere_relevante_systemen",
            "identity_systeem",
            "huidige_login_methode",
            "gewenste_kanalen_hr_agent",
            "it_contactpersoon"
        ],
        "advies_haakje": "Identificeer integratie-kansen en mogelijke API-koppelingen voor bredere HR-automatisering"
    },
    
    5: {
        "fase_number": 5,
        "fase_name": "Beveiliging, Privacy & Compliance",
        "doel": "Randvoorwaarden helder krijgen, geen verrassingen later",
        "kern_vragen": [
            "Zijn er specifieke privacy- of compliance-eisen bovenop AVG/GDPR?",
            "Zijn er datacategorieën die de HR Agent niet mag verwerken of tonen?",
            "Hebben jullie een interne DPO of privacy officer die betrokken moet worden?",
            "Moeten we rekening houden met de OR rond de inzet van AI?",
            "Zijn er eerdere trajecten met AI of chatbots geweest? Wat waren de lessen?",
            "Zijn er audit-requirements of certificeringen waar we rekening mee moeten houden?"
        ],
        "output_fields": [
            "extra_privacy_compliance_eisen",
            "verboden_datacategorieen",
            "dpo_privacy_officer",
            "or_betrokkenheid_ai",
            "eerdere_ai_chatbot_trajecten",
            "audit_requirements"
        ],
        "advies_haakje": "Adviseer over AI-governance en responsible AI-implementatie in HR"
    },
    
    6: {
        "fase_number": 6,
        "fase_name": "Doelen, KPI's & Succescriteria",
        "doel": "Zorgen dat de implementatie meetbaar succesvol is",
        "kern_vragen": [
            "Als de HR Agent over 6 maanden perfect zou werken, wat maakt het dan een succes voor jou persoonlijk?",
            "Welke concrete doelen wil je halen? (minder tickets, kortere doorlooptijd, hogere tevredenheid)",
            "Welke KPI's meten jullie vandaag al in HR-service?",
            "Zijn er targets qua medewerkerstevredenheid? (eNPS, HR-NPS)",
            "Wie in de organisatie moet overtuigd zijn dat dit geslaagd is?",
            "Zijn er baseline metingen beschikbaar om voortgang te meten?"
        ],
        "output_fields": [
            "persoonlijke_succes_definitie",
            "concrete_doelen",
            "huidige_kpis",
            "tevredenheid_targets",
            "belangrijke_stakeholders",
            "baseline_metingen"
        ],
        "advies_haakje": "Stel HR-analytics dashboard voor om impact te meten en continue verbetering te sturen"
    },
    
    7: {
        "fase_number": 7,
        "fase_name": "Change & Adoptie",
        "doel": "Zorgen dat de HR Agent niet in een hoekje sterft",
        "kern_vragen": [
            "Hoe introduceert u normaal nieuwe HR-tools richting medewerkers?",
            "Welke communicatiemiddelen werken goed in jullie organisatie?",
            "Zijn er groepen die kritisch zijn op veranderingen of technologie?",
            "Wie kan ambassadeur zijn voor de HR Agent binnen de organisatie?",
            "Zijn er trainingen of korte demos nodig, en voor wie?",
            "Wat is de change management capaciteit binnen HR?"
        ],
        "output_fields": [
            "gebruikelijke_introductie_methode",
            "effectieve_communicatiemiddelen",
            "kritische_groepen",
            "potentiele_ambassadeurs",
            "training_behoeften",
            "change_management_capaciteit"
        ],
        "advies_haakje": "Ontwikkel change management roadmap en communicatieplan voor bredere HR-transformatie"
    },
    
    8: {
        "fase_number": 8,
        "fase_name": "Onboarding & Offboarding",
        "doel": "Identificeren van optimalisatiekansen in employee lifecycle",
        "kern_vragen": [
            "Hoe verloopt onboarding nu in de praktijk? (van contract tot eerste werkweek)",
            "Waar gaat het vaak mis of waar loopt het traag?",
            "Welke informatie heeft een nieuwe medewerker in de eerste 30 dagen het vaakst nodig?",
            "Zijn er standaard checklists of draaiboeken voor onboarding?",
            "Hoe verloopt offboarding en waar zitten daar pijnpunten?"
        ],
        "output_fields": [
            "onboarding_proces_beschrijving",
            "onboarding_knelpunten",
            "info_behoeften_eerste_30_dagen",
            "onboarding_checklists",
            "offboarding_proces_pijnpunten"
        ],
        "advies_haakje": "Automatische onboarding flows, checklists, LMS-integratie en employee journey mapping"
    },
    
    9: {
        "fase_number": 9,
        "fase_name": "Verzuim & Wellbeing",
        "doel": "Inzicht in verzuim en employee wellbeing",
        "kern_vragen": [
            "Hoe verloopt het verzuimproces nu? (administratief en begeleiding)",
            "Zijn er knelpunten in communicatie richting medewerkers bij verzuim?",
            "Waar zou je idealiter meer data of inzicht in willen hebben rond verzuim?",
            "Welke wellbeing-initiatieven hebben jullie en hoe effectief zijn die?",
            "Wat zijn de huidige verzuimcijfers en trends?"
        ],
        "output_fields": [
            "verzuimproces_beschrijving",
            "verzuim_communicatie_knelpunten",
            "gewenste_verzuim_inzichten",
            "wellbeing_initiatieven",
            "verzuimcijfers_trends"
        ],
        "advies_haakje": "AI/analytics op verzuim, sentiment-analyse, risicogroepen identificatie en preventie-programma's"
    },
    
    10: {
        "fase_number": 10,
        "fase_name": "Performance, Ontwikkeling & Learning",
        "doel": "Identificeren van talent management kansen",
        "kern_vragen": [
            "Hoe wordt performance nu besproken en vastgelegd?",
            "Hoe krijgen medewerkers inzicht in ontwikkelmogelijkheden en trainingen?",
            "Is er behoefte aan betere ondersteuning van managers in performance-gesprekken?",
            "Wat is de learning & development strategie?",
            "Hoe worden skills getrackt en hoe werken career paths?"
        ],
        "output_fields": [
            "performance_management_proces",
            "ontwikkelmogelijkheden_inzicht",
            "manager_support_behoefte",
            "learning_development_strategie",
            "skills_tracking_career_paths"
        ],
        "advies_haakje": "Future agents voor coaching, analytics rond performance en skills, interne mobiliteit-platform"
    },
    
    11: {
        "fase_number": 11,
        "fase_name": "HR-Analytics & Datavolwassenheid",
        "doel": "Begrijpen van data-maturity en analytics-kansen",
        "kern_vragen": [
            "Welke HR-rapportages en dashboards hebben jullie nu?",
            "Welke vragen kun je vandaag niet goed beantwoorden met de huidige data?",
            "Wie in de organisatie vraagt het vaakst om HR-inzichten?",
            "Zijn er ambities rond predictive analytics? (turnover, performance)",
            "Hoe is de data-kwaliteit en governance geregeld?"
        ],
        "output_fields": [
            "huidige_rapportages_dashboards",
            "onbeantwoorde_data_vragen",
            "stakeholders_hr_insights",
            "predictive_analytics_ambities",
            "data_kwaliteit_governance"
        ],
        "advies_haakje": "Bredere data- en analytics roadmap, HR-analytics maturity assessment, executive dashboards"
    }
}

def get_fase_definition(fase_number: int) -> dict:
    """Get fase definition by number"""
    return FASE_DEFINITIONS.get(fase_number, FASE_DEFINITIONS[1])

def get_all_fase_names() -> list:
    """Get list of all fase names"""
    return [fase["fase_name"] for fase in FASE_DEFINITIONS.values()]

def get_fase_output_fields(fase_number: int) -> list:
    """Get output fields for a specific fase"""
    fase = get_fase_definition(fase_number)
    return fase.get("output_fields", [])

def get_total_output_fields() -> list:
    """Get all output fields across all fases"""
    all_fields = []
    for fase in FASE_DEFINITIONS.values():
        all_fields.extend(fase.get("output_fields", []))
    return all_fields
