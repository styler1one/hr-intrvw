"""Test full interview flow"""
import os
from dotenv import load_dotenv
from interview_agent import InterviewAgent

load_dotenv()

print("=== Testing Full Interview Flow ===\n")

# Create agent
agent = InterviewAgent(
    provider="anthropic",
    api_key=os.getenv('ANTHROPIC_API_KEY'),
    model=os.getenv('LLM_MODEL')
)

print("✅ Agent created\n")

# Simulate first message
messages = [
    {
        "role": "user",
        "content": "We zijn TechParts Manufacturing, een Nederlands productiebedrijf gespecialiseerd in precisie-onderdelen voor de automotive en aerospace industrie. We hebben 1000 medewerkers verdeeld over 3 locaties."
    }
]

print("Sending first message to agent...")
try:
    response = agent.process_message(messages=messages, current_fase=1)
    print(f"\n✅ Response received!")
    print(f"Content length: {len(response['content'])} chars")
    print(f"Fase complete: {response['fase_complete']}")
    print(f"\nFirst 200 chars of response:")
    print(response['content'][:200])
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n=== Test Complete ===")
