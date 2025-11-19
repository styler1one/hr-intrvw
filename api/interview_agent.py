import openai
import anthropic
import json
import re
from pathlib import Path
from templates import get_template, get_fase_count, EXTENDED_FASE_INSTRUCTIONS

class InterviewAgent:
    def __init__(self, provider: str = "openai", api_key: str = None, model: str = "gpt-4-turbo", api_base: str = None, template_id: str = "standard"):
        self.provider = provider.lower()
        self.model = model
        self.template_id = template_id
        self.template = get_template(template_id)
        self.total_fases = self.template["total_fases"]
        
        # Initialize the appropriate client
        if self.provider == "openai":
            self.client = openai.OpenAI(api_key=api_key)
        elif self.provider == "anthropic":
            self.client = anthropic.Anthropic(api_key=api_key)
        elif self.provider == "windsurf":
            # Windsurf uses OpenAI-compatible API
            self.client = openai.OpenAI(
                api_key=api_key,
                base_url=api_base or "https://api.windsurf.ai/v1"
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")
        
        self.system_prompt = self.load_system_prompt()
        self.fase_instructions = self.load_fase_instructions()
    
    def load_system_prompt(self):
        """Load system prompt from config file"""
        # For now, embedded. In production, load from file
        return """Je bent de Volentis HR Implementation Interview Agent.

=== JE ROL ===
- Je helpt organisaties om de Volentis HR Agent snel en slim te implementeren.
- Je verzamelt gestructureerde informatie over organisatie, HR-processen, systemen en documenten.

=== CONVERSATIE STIJL ===
- Zakelijk, vriendelijk en helder
- Stel ALTIJD maar ÉÉN vraag tegelijk - wacht op antwoord voordat je de volgende vraag stelt
- NOOIT meerdere vragen in één bericht
- Vraag om kwantificering waar mogelijk
- Leg kort uit WAAROM je een vraag stelt als dat helpt
- Herformuleer vage antwoorden tot specifieke informatie
- Blijf strikt binnen HR & Volentis HR Agent domein

=== OPERATIONAL GUIDELINES ===
1. CONTEXT MANAGEMENT:
   - Extraheer en sla gestructureerde data op NA ELKE FASE
   - Begin elke nieuwe fase met korte samenvatting

2. DATA QUALITY:
   - NEVER invent data - mark as "unknown" if unclear
   - ASK follow-up questions max 2x per topic, then move on

3. OUTPUT STRUCTURE:
   - Generate PARTIAL JSON after each fase
   - Each fase outputs only its own fields

4. QUESTION CLUSTERING:
   - Group questions in clusters of max 3-4 per interaction
   - Wait for answers before next cluster

=== OUTPUT FORMAT ===
After each fase, output JSON in this format:
```json
{
  "fase": number,
  "fase_name": "string",
  "confidence": "high | medium | low",
  "fields": {
    // only fields relevant to this fase
  }
}
```"""
    
    def load_fase_instructions(self):
        """Load fase-specific instructions based on template"""
        # Base instructions for fases 1-11
        base_instructions = {
            1: {
                "name": "Intro & context",
                "duration": "5 min" if self.template_id != "quick" else "3 min",
                "instructions": """FASE 1 – INTRO & CONTEXT

BELANGRIJK: Stel vragen ÉÉN VOOR ÉÉN. Wacht op antwoord voordat je de volgende vraag stelt.

VRAGEN (stel ze één voor één):
1. In wat voor organisatie werk je? (sector, grootte, aantal medewerkers, locaties)
2. Wat is jouw rol binnen HR?
3. Waarom kijken jullie nu naar een HR Agent zoals Volentis?
4. Wat hoop je over 6-12 maanden verbeterd te hebben?
5. Wat is de HR-strategie voor de komende 2-3 jaar?
6. Hoe zou je de organisatiecultuur beschrijven?
7. Hoe is de werkdruk binnen HR?
8. Zijn er recente reorganisaties of grote veranderingen geweest?

FASE AFSLUITING:
Na alle vragen: geef korte samenvatting (max 5 bullets) en vraag: "Klopt dit?"

Als bevestigd, output JSON met:
- org_profile
- hr_team_profile  
- strategic_focus
- organizational_culture"""
            },
            2: {
                "name": "Stakeholders",
                "duration": "5 min" if self.template_id != "quick" else "3 min",
                "instructions": """FASE 2 – STAKEHOLDERS

BELANGRIJK: Stel vragen ÉÉN VOOR ÉÉN. Wacht op antwoord voordat je de volgende vraag stelt.

VRAGEN (stel ze één voor één):
1. Wie zijn de belangrijkste stakeholders voor deze implementatie? (bijv. MT, OR, IT, lijnmanagers)
2. Wie moet uiteindelijk akkoord geven op de implementatie?
3. Zijn er groepen waar je weerstand verwacht? Waarom?
4. Hoe staat jullie organisatie over het algemeen tegenover nieuwe technologie?
5. Wat was de laatste grote HR-verandering en hoe verliep die?

FASE AFSLUITING:
Na alle vragen: geef korte samenvatting (max 5 bullets) en vraag: "Klopt dit?"

Als bevestigd, output JSON met:
- stakeholders
- change_history
- change_readiness_preliminary"""
            },
            # Add more fases as needed
        }
        
        # Add extended fases for extensive template
        if self.template_id == "extensive":
            base_instructions.update(EXTENDED_FASE_INSTRUCTIONS)
        
        return base_instructions
    
    async def process_message(self, messages: list, current_fase: int):
        """Process user message and generate response"""
        
        # Get fase instructions
        fase_info = self.fase_instructions.get(current_fase, {})
        fase_instructions = fase_info.get("instructions", "")
        
        # Build prompt
        full_prompt = f"{self.system_prompt}\n\n{fase_instructions}"
        
        # Prepare messages for API
        api_messages = [
            {"role": "system", "content": full_prompt}
        ]
        
        # Add conversation history (last 10 messages to manage context)
        for msg in messages[-10:]:
            api_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        try:
            # Call LLM API based on provider
            if self.provider in ["openai", "windsurf"]:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=api_messages,
                    temperature=0.7,
                    max_tokens=2000
                )
                agent_message = response.choices[0].message.content
                
            elif self.provider == "anthropic":
                # Anthropic uses different API format
                # Extract system message
                system_msg = api_messages[0]["content"] if api_messages[0]["role"] == "system" else ""
                user_messages = [msg for msg in api_messages if msg["role"] != "system"]
                
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=2000,
                    temperature=0.7,
                    system=system_msg,
                    messages=user_messages
                )
                agent_message = response.content[0].text
            
            # Check for JSON output (fase complete)
            partial_json = self.extract_json(agent_message)
            
            return {
                "content": agent_message,
                "fase_complete": partial_json is not None,
                "partial_json": partial_json,
                "fase_name": fase_info.get("name", "")
            }
            
        except Exception as e:
            print(f"Error calling {self.provider} API: {e}")
            return {
                "content": f"Sorry, er ging iets mis: {str(e)}",
                "fase_complete": False,
                "partial_json": None,
                "fase_name": fase_info.get("name", "")
            }
    
    def extract_json(self, text: str):
        """Extract JSON from agent response"""
        # Look for JSON code blocks
        json_pattern = r'```json\s*(.*?)\s*```'
        matches = re.findall(json_pattern, text, re.DOTALL)
        
        if matches:
            try:
                return json.loads(matches[0])
            except json.JSONDecodeError:
                pass
        
        # Try to find JSON without code blocks
        try:
            # Find anything that looks like JSON
            json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
            matches = re.findall(json_pattern, text, re.DOTALL)
            if matches:
                return json.loads(matches[-1])  # Take last match
        except:
            pass
        
        return None
    
    async def generate_suggestions(self, messages: list, current_question: str) -> list:
        """Generate AI-powered suggestions based on conversation context and current question"""
        
        # Build context from recent messages (last 6 messages for efficiency)
        recent_context = messages[-6:] if len(messages) > 6 else messages
        context_summary = "\n".join([
            f"{msg['role'].upper()}: {msg['content'][:200]}" 
            for msg in recent_context
        ])
        
        suggestion_prompt = f"""Je bent een slimme assistent die helpt bij het beantwoorden van interview vragen.

CONVERSATIE CONTEXT:
{context_summary}

HUIDIGE VRAAG VAN DE AGENT:
{current_question}

TAAK:
Genereer 3-4 concrete, relevante antwoord-suggesties die de gebruiker kan gebruiken om deze vraag te beantwoorden.

REGELS:
- Suggesties moeten SPECIFIEK en RELEVANT zijn voor deze vraag
- Gebruik context uit eerdere antwoorden om suggesties te personaliseren
- Houd suggesties kort (max 8 woorden)
- Maak suggesties actionable en concreet
- Varieer in specificiteit (van algemeen tot specifiek)
- Gebruik Nederlandse taal

FORMAAT:
Geef ALLEEN een JSON array met suggesties terug, bijvoorbeeld:
["Suggestie 1", "Suggestie 2", "Suggestie 3", "Suggestie 4"]

GEEN uitleg, ALLEEN de JSON array."""

        try:
            if self.provider == "anthropic":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=500,
                    messages=[{"role": "user", "content": suggestion_prompt}]
                )
                content = response.content[0].text
            else:  # OpenAI or Windsurf
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": suggestion_prompt}],
                    max_tokens=500,
                    temperature=0.7
                )
                content = response.choices[0].message.content
            
            # Extract JSON array from response
            content = content.strip()
            
            # Try to parse as JSON
            try:
                suggestions = json.loads(content)
                if isinstance(suggestions, list) and len(suggestions) > 0:
                    return suggestions[:4]  # Max 4 suggestions
            except json.JSONDecodeError:
                # Try to find JSON array in text
                json_pattern = r'\[(.*?)\]'
                matches = re.findall(json_pattern, content, re.DOTALL)
                if matches:
                    suggestions = json.loads(f"[{matches[0]}]")
                    if isinstance(suggestions, list) and len(suggestions) > 0:
                        return suggestions[:4]
            
            # Fallback
            return [
                "Ja, dat klopt",
                "Nee, nog niet",
                "Deels, laat me toelichten"
            ]
            
        except Exception as e:
            print(f"Error in generate_suggestions: {e}")
            import traceback
            traceback.print_exc()
            # Return generic fallback
            return [
                "Ja, dat klopt",
                "Nee, nog niet",
                "Deels, laat me toelichten"
            ]
