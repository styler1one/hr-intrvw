# Interview Agent - Flow Diagram

## Hoofdflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    START: Nieuw Project                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  FASE 1: PLANNING & REQUIREMENTS                                │
│  Agent: Requirements Analyst                                     │
│                                                                  │
│  Input: User beschrijving                                       │
│  Proces:                                                        │
│    1. Stel klarificerende vragen                               │
│    2. Identificeer scope en doelen                             │
│    3. Definieer succescriteria                                 │
│  Output: Product Requirements Document (PRD)                    │
│                                                                  │
│  Guardrails:                                                    │
│    - Gestructureerd format                                      │
│    - Alle requirements gedocumenteerd                           │
│    - User stories compleet                                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  FASE 2: INTERVIEW UITVOERING                                   │
│  Agent: Interview Agent (Domein-Specifiek)                      │
│                                                                  │
│  Input: PRD + Domein configuratie                               │
│  Proces:                                                        │
│    1. Selecteer domein (HR/Sales/Operations/etc)               │
│    2. Laad domein-specifieke templates                         │
│    3. Voer gestructureerde interviews uit                      │
│    4. Verzamel stakeholder input                               │
│    5. Documenteer bevindingen                                  │
│  Output: Interview Report                                       │
│                                                                  │
│  Guardrails:                                                    │
│    - Blijf binnen domein                                        │
│    - Gebruik domein terminologie                                │
│    - Focus op implementeerbare oplossingen                      │
│    - Gestructureerde documentatie                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  FASE 3: ANALYSE & DESIGN                                       │
│  Agent: Solution Designer                                        │
│                                                                  │
│  Input: PRD + Interview Report                                  │
│  Proces:                                                        │
│    1. Analyseer interview data                                 │
│    2. Identificeer oplossingsrichtingen                        │
│    3. Ontwerp technische architectuur                          │
│    4. Specificeer componenten                                  │
│    5. Definieer integraties                                    │
│  Output: Technical Design Document                              │
│                                                                  │
│  Guardrails:                                                    │
│    - Gestandaardiseerd format                                   │
│    - Gebaseerd op interview data                                │
│    - Praktisch en implementeerbaar                              │
│    - Geen aannames zonder onderbouwing                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  FASE 4: IMPLEMENTATIE PLANNING                                 │
│  Agent: Implementation Planner (Builder)                         │
│                                                                  │
│  Input: Technical Design Document                               │
│  Proces:                                                        │
│    1. Breek design op in taken                                 │
│    2. Definieer subtaken                                       │
│    3. Stel dependencies vast                                   │
│    4. Prioriteer taken                                         │
│  Output: Task List met subtaken                                │
│                                                                  │
│  ┌──────────────────────────────────────────────┐              │
│  │  Per Taak:                                   │              │
│  │  - Eigen scope                               │              │
│  │  - Eigen chat context                        │              │
│  │  - Acceptatiecriteria                        │              │
│  │  - 1 taak = 1 git commit                     │              │
│  └──────────────────────────────────────────────┘              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  FASE 5: BUILD & QA LOOP                                        │
│  Agents: Builder + QA Reviewer                                   │
│                                                                  │
│  ┌────────────────────────────────────────────────────┐        │
│  │  Voor elke taak:                                   │        │
│  │                                                     │        │
│  │  1. Builder werkt aan taak                         │        │
│  │     └─> Commit changes                             │        │
│  │                                                     │        │
│  │  2. QA Reviewer controleert automatisch            │        │
│  │     ├─> Check tegen standaarden                    │        │
│  │     ├─> Valideer requirements                      │        │
│  │     └─> Beoordeel kwaliteit                        │        │
│  │                                                     │        │
│  │  3. Beslissing:                                    │        │
│  │     ┌─────────────┬─────────────┐                 │        │
│  │     │ GOEDGEKEURD │  AFGEKEURD  │                 │        │
│  │     └──────┬──────┴──────┬──────┘                 │        │
│  │            │             │                         │        │
│  │            │             ├─> Maak herbouw taak    │        │
│  │            │             └─> Maak nieuwe QA taak  │        │
│  │            │                  └─> Loop terug      │        │
│  │            │                                       │        │
│  │            └─> Volgende taak                       │        │
│  │                                                     │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                  │
│  Output: Geïmplementeerde en gecontroleerde code                │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  FASE 6: REVIEW & DEPLOYMENT                                    │
│  Agent: Deployment Manager                                       │
│                                                                  │
│  Input: Alle voltooide taken                                    │
│  Proces:                                                        │
│    1. Toon alle code changes                                   │
│    2. User review met inline comments                          │
│    3. Verzamel feedback                                        │
│    4. Maak herbouw taken indien nodig                          │
│    5. Check merge conflicts                                    │
│    6. Deploy naar productie                                    │
│  Output: Deployed applicatie                                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PROJECT COMPLEET                              │
└─────────────────────────────────────────────────────────────────┘
```

## Domein-Specifieke Interview Flow (Voorbeeld: HR)

```
┌─────────────────────────────────────────────────────────────────┐
│  HR INTERVIEW AGENT                                             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  STAP 1: Introductie & Context                                  │
│                                                                  │
│  - Begroet stakeholder                                          │
│  - Leg doel van interview uit                                   │
│  - Vraag naar rol en verantwoordelijkheden                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  STAP 2: Huidige Situatie Analyse                              │
│                                                                  │
│  Focus Gebied 1: RECRUITMENT                                    │
│  ├─ Hoe verloopt het huidige proces?                           │
│  ├─ Hoeveel tijd kost CV screening?                            │
│  ├─ Wat zijn de grootste uitdagingen?                          │
│  └─ Welke tools gebruiken jullie?                              │
│                                                                  │
│  Focus Gebied 2: ONBOARDING                                     │
│  ├─ Hoe ziet het onboarding proces eruit?                      │
│  ├─ Hoeveel tijd kost het per nieuwe medewerker?               │
│  ├─ Wat zijn repetitieve taken?                                │
│  └─ Waar gaat het vaak mis?                                    │
│                                                                  │
│  Focus Gebied 3: PERFORMANCE MANAGEMENT                         │
│  ├─ Hoe meten jullie performance?                              │
│  ├─ Hoe vaak zijn er evaluaties?                               │
│  ├─ Wat is tijdrovend?                                          │
│  └─ Hoe verzamelen jullie feedback?                            │
│                                                                  │
│  Focus Gebied 4: ADMINISTRATIE                                  │
│  ├─ Welke administratieve taken kosten veel tijd?              │
│  ├─ Wat is repetitief werk?                                    │
│  ├─ Welke data moet je vaak opzoeken?                          │
│  └─ Waar maken jullie fouten?                                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  STAP 3: Gewenste Situatie                                      │
│                                                                  │
│  ├─ Wat zou je willen verbeteren?                              │
│  ├─ Wat zijn de prioriteiten?                                  │
│  ├─ Wat is het verwachte resultaat?                            │
│  ├─ Hoe meet je succes?                                        │
│  └─ Wat is de tijdlijn?                                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  STAP 4: Constraints & Requirements                             │
│                                                                  │
│  ├─ Welke systemen zijn er al (ATS, HRIS, etc)?               │
│  ├─ Wat zijn integratie-eisen?                                 │
│  ├─ Wat is het budget?                                         │
│  ├─ Wat zijn privacy/compliance eisen?                         │
│  └─ Wie zijn de eindgebruikers?                                │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  STAP 5: Validatie & Samenvatting                              │
│                                                                  │
│  ├─ Samenvatting van bevindingen                               │
│  ├─ Valideer begrip                                            │
│  ├─ Prioriteer verbeterpunten                                  │
│  └─ Bevestig volgende stappen                                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  OUTPUT: HR Interview Report                                    │
│                                                                  │
│  Bevat:                                                         │
│  - Stakeholder informatie                                       │
│  - Huidige situatie per focus gebied                           │
│  - Pain points en uitdagingen                                   │
│  - Gewenste verbeteringen                                       │
│  - Prioriteiten                                                 │
│  - Constraints en requirements                                  │
│  - Aanbevelingen voor oplossing                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Self-Improvement Loop Detail

```
┌─────────────────────────────────────────────────────────────────┐
│  TAAK EXECUTIE MET QA LOOP                                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │  Taak Start    │
                    └────────┬───────┘
                             │
                             ▼
                    ┌────────────────┐
                    │ Builder Agent  │
                    │ werkt aan taak │
                    └────────┬───────┘
                             │
                             ▼
                    ┌────────────────┐
                    │ Taak Voltooid  │
                    │ (Git Commit)   │
                    └────────┬───────┘
                             │
                             ▼
                    ┌────────────────┐
                    │  QA Reviewer   │
                    │  Start Auto    │
                    └────────┬───────┘
                             │
                             ▼
                ┌────────────────────────┐
                │  Check Standaarden:    │
                │  - Code kwaliteit      │
                │  - Naming conventions  │
                │  - Tests aanwezig      │
                │  - Documentatie        │
                │  - Requirements match  │
                └────────┬───────────────┘
                         │
                         ▼
            ┌────────────┴────────────┐
            │                         │
            ▼                         ▼
    ┌───────────────┐        ┌───────────────┐
    │  GOEDGEKEURD  │        │   AFGEKEURD   │
    └───────┬───────┘        └───────┬───────┘
            │                        │
            │                        ▼
            │               ┌─────────────────┐
            │               │ Maak 2 Taken:   │
            │               │ 1. Herbouw taak │
            │               │ 2. QA taak      │
            │               └────────┬────────┘
            │                        │
            │                        ▼
            │               ┌─────────────────┐
            │               │ Insert taken in │
            │               │ task list       │
            │               └────────┬────────┘
            │                        │
            │                        ▼
            │               ┌─────────────────┐
            │               │ Builder werkt   │
            │               │ aan herbouw     │
            │               └────────┬────────┘
            │                        │
            │                        └────┐
            │                             │
            ▼                             ▼
    ┌───────────────┐            ┌───────────────┐
    │ Volgende Taak │◄───────────┤  QA opnieuw   │
    └───────────────┘            └───────────────┘
```

## Agent Context Management

```
┌─────────────────────────────────────────────────────────────────┐
│  AGENT PROMPT STRUCTUUR                                         │
└─────────────────────────────────────────────────────────────────┘

Voor elke agent call:

┌─────────────────────────────────────────────────────────────────┐
│  [SYSTEM PROMPT]                                                │
│  - Agent rol en verantwoordelijkheden                           │
│  - Algemene capabilities                                        │
│  - Output format requirements                                   │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  [CONTEXT]                                                      │
│  - Huidige fase                                                 │
│  - Status (eerste keer / follow-up)                            │
│  - Beschikbare documenten                                       │
│  - Eerdere conversatie history                                  │
│  - Relevante data                                               │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  [SITUATIE-SPECIFIEKE INSTRUCTIES]                             │
│                                                                  │
│  Als eerste keer:                                               │
│  - Begroet gebruiker                                            │
│  - Leg uit wat je gaat doen                                     │
│  - Start met eerste vraag/actie                                 │
│                                                                  │
│  Als follow-up:                                                 │
│  - Refereer naar eerdere conversatie                            │
│  - Beantwoord gebruiker input                                   │
│  - Blijf bij het script                                         │
│  - Ga door naar volgende stap                                   │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  [GUARDRAILS]                                                   │
│  - Blijf binnen scope                                           │
│  - Gebruik gestandaardiseerd format                             │
│  - Geen algemene gesprekken                                     │
│  - Focus op taak-relevante zaken                                │
│  - Domein-specifieke constraints                                │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  [OUTPUT TEMPLATE]                                              │
│  - Specifiek format voor deze fase                             │
│  - Verplichte secties                                           │
│  - Structuur requirements                                       │
└─────────────────────────────────────────────────────────────────┘
```

## Multi-Agent Coördinatie

```
┌─────────────────────────────────────────────────────────────────┐
│  WORKSPACE MASTER (Orchestrator)                                │
│                                                                  │
│  Verantwoordelijk voor:                                         │
│  - Agent selectie per fase                                      │
│  - Context management                                           │
│  - Document routing                                             │
│  - Workflow state tracking                                      │
│  - User interaction routing                                     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                ┌────────────┼────────────┐
                │            │            │
                ▼            ▼            ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │ Agent 1  │  │ Agent 2  │  │ Agent 3  │
        │ Planning │  │Interview │  │ Design   │
        └──────────┘  └──────────┘  └──────────┘
                │            │            │
                └────────────┼────────────┘
                             │
                             ▼
                ┌────────────────────────┐
                │  Shared Context Store  │
                │  - Documents           │
                │  - Chat history        │
                │  - Task state          │
                │  - User preferences    │
                └────────────────────────┘
```
