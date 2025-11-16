"""Direct API test"""
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('ANTHROPIC_API_KEY')

print(f"Testing API key: {api_key[:20]}...")
print()

try:
    import anthropic
    client = anthropic.Anthropic(api_key=api_key)
    
    print("Sending test message to Claude...")
    message = client.messages.create(
        model=os.getenv('LLM_MODEL', 'claude-3-5-sonnet-20241022'),
        max_tokens=100,
        messages=[
            {"role": "user", "content": "Say 'Hello, I am working!' in Dutch"}
        ]
    )
    
    print(f"✅ SUCCESS! Response: {message.content[0].text}")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
