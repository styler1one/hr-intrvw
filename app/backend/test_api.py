"""Test script to verify API configuration"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=== API Configuration Test ===")
print()

provider = os.getenv("LLM_PROVIDER", "not set")
print(f"Provider: {provider}")

if provider == "anthropic":
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if api_key and api_key != "YOUR_ANTHROPIC_KEY_HERE":
        print(f"✅ Anthropic API Key: {api_key[:15]}...")
        print(f"Model: {os.getenv('LLM_MODEL')}")
        
        # Test Anthropic connection
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            print("\n✅ Anthropic client initialized successfully!")
            print("\nTesting API connection...")
            
            # Simple test
            message = client.messages.create(
                model=os.getenv("LLM_MODEL", "claude-3-opus-20240229"),
                max_tokens=100,
                messages=[
                    {"role": "user", "content": "Say 'Hello, I am working!' in Dutch"}
                ]
            )
            
            print(f"✅ API Response: {message.content[0].text}")
            print("\n🎉 Everything is working! You can start the backend now.")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("\nCheck:")
            print("1. Is your API key correct?")
            print("2. Do you have credits on your Anthropic account?")
    else:
        print("❌ API Key not configured!")
        print("\nPlease edit .env and set:")
        print("ANTHROPIC_API_KEY=sk-ant-your-actual-key")
        
elif provider == "openai":
    api_key = os.getenv("OPENAI_API_KEY", "")
    if api_key and api_key != "sk-your-api-key-here":
        print(f"✅ OpenAI API Key: {api_key[:15]}...")
    else:
        print("❌ API Key not configured!")
else:
    print(f"❌ Unknown provider: {provider}")

print("\n" + "="*40)
