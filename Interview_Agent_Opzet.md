# Interview Agent - Opzet en Architectuur

## Analyse van het Gesprek

### Kernpunten uit de Discussie

**Speaker 1 (Dennis - Platform Expert)** en **Speaker 2** bespreken hoe een interview agent het beste vorm te geven. De belangrijkste inzichten:

1. **AI heeft specifieke instructies nodig** - Je kunt niet vertrouwen op default LLM behavior
2. **Domeinkennis is cruciaal** - Een interview agent moet specifiek zijn voor een domein (bijv. HR)
3. **Gestructureerde workflow is essentieel** - Plan → Design → Implementatie → QA → Deploy
4. **Guardrails en templates** - Elke agent heeft specifieke instructies per fase
5. **Self-improvement loop** - Automatische QA en herbouw-cycli

---

## Interview Agent Architectuur

### 1. Doel en Scope

**Primaire Functie:**
Een interview agent die bedrijven helpt bij het implementeren van AI-oplossingen door:
- Gestructureerde interviews af te nemen met stakeholders
- Input te verzamelen van verschillende afdelingen
- Automatisch een implementatieplan te genereren
- Specifiek te zijn voor een domein (bijv. HR, Sales, Operations)

**Belangrijke Constraint:**
> "Want dan ga je af op het default behavior van een LLM... als je hem echt behulpzaam wil laten zijn, dan moet je duidelijk in je instructies zeggen waar hij op moet letten en waar hij naar moet zoeken."

---

## 2. Workflow Structuur

### Fase 1: Planning & Requirements
**Agent:** Requirements Analyst

**Taken:**
- Start met een plan (altijd!)
- Stel klarificerende vragen
- Maak een Product Requirements Document (PRD)
- Definieer:
  - User stories
  - Requirements
  - Succescriteria
  - Scope en beperkingen

**Template Onderdelen:**
```
- Wat is het doel van de AI-implementatie?
- Welke processen moeten verbeterd worden?
- Wie zijn de eindgebruikers?
- Wat zijn de succescriteria?
- Welke constraints zijn er (budget, tijd, technisch)?
```

**Guardrails:**
- Blijf binnen het gedefinieerde domein (bijv. HR)
- Stel alleen relevante vragen voor de implementatie
- Geen algemene gesprekken over het weer etc.
- Gestructureerd format voor output

---

### Fase 2: Interview Uitvoering
**Agent:** Interview Agent (domein-specifiek)

**Taken:**
- Voer gestructureerde interviews uit
- Verzamel input van verschillende stakeholders
- Identificeer pain points en verbeterpunten
- Documenteer bevindingen

**Domein-Specifieke Instructies (voorbeeld HR):**

**Toon:**
- Professioneel maar toegankelijk
- Empathisch voor HR-uitdagingen
- Gericht op praktische oplossingen

**Focus Gebieden:**
- Recruitment processen
- Onboarding workflows
- Performance management
- Employee engagement
- Administratieve lasten

**Vragen Structuur:**
```
1. Huidige Situatie
   - Hoe werkt het proces nu?
   - Wat zijn de grootste uitdagingen?
   - Hoeveel tijd kost het?

2. Gewenste Situatie
   - Wat zou je willen verbeteren?
   - Wat zijn de prioriteiten?
   - Wat is het verwachte resultaat?

3. Constraints
   - Welke systemen zijn er al?
   - Wat zijn de technische beperkingen?
   - Wat is het budget/tijdframe?
```

**Guardrails:**
- Blijf bij HR-gerelateerde onderwerpen
- Stel geen vragen over andere domeinen
- Focus op implementeerbare oplossingen
- Documenteer alle antwoorden gestructureerd

---

### Fase 3: Analyse & Design
**Agent:** Solution Designer

**Taken:**
- Analyseer interview resultaten
- Maak een technisch design
- Definieer componenten en integraties
- Stel implementatie-strategie op

**Output Format:**
```
1. Executive Summary
2. Probleemanalyse
3. Voorgestelde Oplossing
   - Componenten
   - Integraties
   - Data flows
4. Technische Specificaties
5. Implementatie Roadmap
6. Risico's en Mitigaties
```

**Guardrails:**
- Gestandaardiseerd format (geen bullet points overal of juist te beknopt)
- Praktisch en implementeerbaar
- Gebaseerd op interview data
- Geen aannames zonder onderbouwing

---

### Fase 4: Implementatie Planning
**Agent:** Implementation Planner (Builder)

**Taken:**
- Breek design op in taken
- Maak subtaken per component
- Definieer dependencies
- Stel prioriteiten

**Taak Structuur:**
- Elke taak heeft een duidelijke scope
- Elke taak heeft eigen chat context
- Taken kunnen groot zijn (agent is lang bezig)
- Elke taak = 1 git commit

**Guardrails:**
- Blijf bij het technisch design
- Maak realistische taken
- Documenteer dependencies
- Duidelijke acceptatiecriteria per taak

---

### Fase 5: Quality Assurance (Self-Improvement Loop)
**Agent:** QA Reviewer

**Taken:**
- Review elke voltooide taak
- Check tegen standaarden
- Identificeer issues
- Maak herbouw-taken indien nodig

**QA Proces:**
```
1. Taak voltooid door Builder
2. QA Agent review automatisch
3. Twee opties:
   a. Goedkeuren → volgende taak
   b. Afkeuren → maak 2 nieuwe taken:
      - Herbouw taak voor Builder
      - Nieuwe QA taak voor check
```

**Standaarden Checklist:**
- Code kwaliteit
- Variabele naming conventions
- Tests aanwezig
- Documentatie compleet
- Voldoet aan requirements

**Guardrails:**
- Kritisch maar constructief
- Specifieke feedback
- Blijf bij de scope
- Geen feature creep

---

### Fase 6: Review & Deployment
**Agent:** Deployment Manager

**Taken:**
- Toon alle wijzigingen
- Faciliteer review door gebruiker
- Handle merge conflicts
- Deploy naar productie

**Review Interface:**
- Toon alle code changes
- Mogelijkheid voor comments per regel/sectie
- Verzamel alle comments
- Maak herbouw taken op basis van feedback

**Deployment Opties:**
- Merge naar main branch
- Deploy naar Vercel/hosting
- Genereer deployment bericht
- Markeer taak als compleet

---

## 3. Agent Configuratie Structuur

### Template Systeem

**Per Agent:**
```
agents/
├── requirements_analyst/
│   ├── system_prompt.txt
│   ├── initial_prompt.txt
│   ├── follow_up_prompt.txt
│   └── output_template.txt
├── interview_agent/
│   ├── hr_domain/
│   │   ├── system_prompt.txt
│   │   ├── question_templates.txt
│   │   ├── tone_guidelines.txt
│   │   └── focus_areas.txt
│   ├── sales_domain/
│   └── operations_domain/
├── solution_designer/
├── implementation_planner/
├── qa_reviewer/
└── deployment_manager/
```

### Context Management

**Per Fase:**
- Agent krijgt specifieke instructies voor de situatie
- "Je bent voor het eerst aangeroepen" vs "Je bent in een follow-up"
- Context van vorige fases beschikbaar
- Referenties naar relevante documenten

**Voorbeeld Prompt Structuur:**
```
[SYSTEM]
Je bent de Interview Agent voor het HR domein.

[CONTEXT]
- Fase: Interview Uitvoering
- Status: Eerste contact
- Beschikbare documenten: PRD-2024-001

[INSTRUCTIES]
1. Begroet de gebruiker professioneel
2. Leg uit wat je gaat doen
3. Begin met de eerste vragenset over recruitment
4. Blijf binnen HR domein
5. Documenteer alle antwoorden gestructureerd

[GUARDRAILS]
- Geen vragen over andere domeinen
- Geen algemene gesprekken
- Focus op implementeerbare oplossingen
- Gebruik gestandaardiseerd format

[OUTPUT FORMAT]
<gestructureerd template>
```

---

## 4. Domein-Specifieke Configuratie

### HR Domain Voorbeeld

**Focus Gebieden:**
1. Recruitment & Onboarding
2. Performance Management
3. Learning & Development
4. Employee Engagement
5. HR Analytics & Reporting

**Toon & Stijl:**
- Empathisch
- Praktisch
- Focus op mensen én processen
- Begrip voor HR-uitdagingen

**Typische Vragen:**
- "Hoeveel tijd besteden jullie aan screening van CV's?"
- "Hoe verloopt het onboarding proces?"
- "Welke repetitieve taken kosten de meeste tijd?"
- "Hoe meten jullie employee satisfaction?"

**Oplossings-Focus:**
- Automatisering van administratie
- Verbetering candidate experience
- Data-driven beslissingen
- Efficiëntere workflows

---

## 5. Technische Implementatie

### Platform Componenten

**Frontend:**
- Chat interface per agent/fase
- Document viewer
- Task management board
- Review interface met inline comments
- Progress tracking

**Backend:**
- Agent orchestration
- Context management
- Document storage
- Version control integratie
- Real-time updates

**Agent System:**
- Template engine voor prompts
- Context injection
- Multi-agent coordination
- Self-improvement loops
- Quality gates

---

## 6. Workflow Voorbeeld: HR Agent Implementatie

### Stap 1: Start Project
```
User: "Ik wil een AI-agent voor HR recruitment"

Requirements Analyst:
- Stelt klarificerende vragen
- Maakt PRD met user stories
- Definieert scope en succescriteria
→ Output: PRD document
```

### Stap 2: Interview Fase
```
Interview Agent (HR Domain):
- "Laten we beginnen met jullie huidige recruitment proces"
- Stelt gestructureerde vragen
- Verzamelt input van HR team
- Documenteert pain points
→ Output: Interview Report met bevindingen
```

### Stap 3: Solution Design
```
Solution Designer:
- Analyseert interview data
- Ontwerpt AI-oplossing voor recruitment
- Specificeert componenten (CV parser, matching engine, etc.)
- Maakt technisch design
→ Output: Technical Design Document
```

### Stap 4: Implementatie
```
Implementation Planner:
- Breekt design op in taken
- Taak 1: CV Parser component
- Taak 2: Matching Algorithm
- Taak 3: Integration met ATS
- etc.

Builder Agent:
- Werkt taken af één voor één
- Elke taak heeft eigen chat
- Commit per voltooide taak

QA Agent (automatisch):
- Review elke taak
- Check tegen standaarden
- Maak herbouw-taken indien nodig
→ Loop tot alles goedgekeurd
```

### Stap 5: Review & Deploy
```
Deployment Manager:
- Toont alle changes
- Gebruiker reviewt
- Inline comments mogelijk
- Merge naar productie
→ Output: Deployed HR Recruitment Agent
```

---

## 7. Kritische Succesfactoren

### 1. Specifieke Instructies
❌ **Niet:** "Je bent een interview agent, stel goede vragen"
✅ **Wel:** "Je bent een HR interview agent. Focus op recruitment, onboarding, en performance management. Stel vragen volgens template X. Documenteer volgens format Y."

### 2. Domein Expertise
- Elke domein heeft eigen agent configuratie
- Specifieke focus gebieden per domein
- Aangepaste toon en stijl
- Domein-specifieke templates

### 3. Gestructureerde Output
- Gestandaardiseerde formats
- Geen willekeurige bullet points
- Consistente documentatie
- Herbruikbare templates

### 4. Guardrails
- Blijf binnen scope
- Geen feature creep
- Focus op implementeerbaar
- Geen algemene gesprekken

### 5. Self-Improvement
- Automatische QA loops
- Herbouw bij issues
- Kwaliteitscontrole per taak
- Iteratieve verbetering

---

## 8. Uitbreidingsmogelijkheden

### Andere Domeinen

**Sales Domain:**
- Lead qualification
- Sales process optimization
- CRM integratie
- Pipeline management

**Operations Domain:**
- Process automation
- Supply chain optimization
- Quality control
- Resource planning

**Customer Service Domain:**
- Ticket routing
- Response automation
- Knowledge base
- Sentiment analysis

### Multi-Domain Projecten
- Start met breed interview
- Identificeer meerdere domeinen
- Maak per domein specifieke agents
- Coördineer tussen domeinen

---

## 9. Implementatie Roadmap

### Fase 1: Core Platform (Basis zoals Dennis heeft)
- [ ] Agent orchestration systeem
- [ ] Template engine
- [ ] Context management
- [ ] Chat interfaces
- [ ] Document storage
- [ ] Task management

### Fase 2: Interview Agent Specifiek
- [ ] Interview agent templates
- [ ] Domein-specifieke configuraties
- [ ] Vraag-bibliotheek per domein
- [ ] Interview rapport generator
- [ ] Stakeholder management

### Fase 3: Integration & Automation
- [ ] Self-improvement loops
- [ ] Automatische QA
- [ ] Git integratie
- [ ] Deployment automation
- [ ] Real-time collaboration

### Fase 4: Domein Uitbreiding
- [ ] HR domein volledig
- [ ] Sales domein
- [ ] Operations domein
- [ ] Custom domain configurator

---

## 10. Best Practices

### Voor Interview Agent

1. **Start Breed, Ga Diep**
   - Begin met open vragen
   - Zoom in op specifieke problemen
   - Valideer begrip met samenvatting

2. **Documenteer Alles**
   - Alle antwoorden gestructureerd
   - Citaten van stakeholders
   - Context en nuances
   - Prioriteiten en constraints

3. **Blijf Praktisch**
   - Focus op implementeerbare oplossingen
   - Geen theoretische discussies
   - Concrete voorbeelden
   - Meetbare doelen

4. **Domein Expertise**
   - Gebruik domein-specifieke terminologie
   - Toon begrip van domein-uitdagingen
   - Stel relevante follow-up vragen
   - Herken patterns in het domein

5. **Iteratief Proces**
   - Valideer begrip regelmatig
   - Pas aan op basis van feedback
   - Bouw voort op eerdere antwoorden
   - Sluit af met samenvatting

---

## Conclusie

De interview agent moet **niet** vertrouwen op default LLM behavior, maar **wel** op:
- Specifieke, domein-gerichte instructies
- Gestructureerde templates en formats
- Duidelijke guardrails en scope
- Geautomatiseerde kwaliteitscontrole
- Iteratieve verbetering

De kracht zit in de **combinatie** van:
1. Goed doordachte workflow (Plan → Design → Build → QA → Deploy)
2. Domein-specifieke configuratie per agent
3. Context-aware prompting per fase
4. Self-improvement loops voor kwaliteit
5. Gestructureerde output formats

**Volgende Stap:** Maak eerst het schema/flow op papier voordat je gaat bouwen. Definieer exact:
- Welke vragen per domein
- Welke output formats
- Welke guardrails
- Welke kwaliteitscriteria

Dan kan de AI de mooie interface maken, maar de strategie moet eerst helder zijn.
