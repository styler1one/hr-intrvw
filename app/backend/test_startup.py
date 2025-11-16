"""Test backend startup"""
import os
from dotenv import load_dotenv

load_dotenv()

print("=== Testing Backend Startup ===\n")

# Test 1: Environment variables
print("1. Environment Variables:")
print(f"   LLM_PROVIDER: {os.getenv('LLM_PROVIDER')}")
print(f"   ANTHROPIC_API_KEY: {os.getenv('ANTHROPIC_API_KEY')[:20]}..." if os.getenv('ANTHROPIC_API_KEY') else "   ANTHROPIC_API_KEY: NOT SET")
print(f"   LLM_MODEL: {os.getenv('LLM_MODEL')}")
print()

# Test 2: Import anthropic
print("2. Testing Anthropic import...")
try:
    import anthropic
    print("   ✅ Anthropic imported successfully")
except Exception as e:
    print(f"   ❌ Error: {e}")
print()

# Test 3: Create Anthropic client
print("3. Testing Anthropic client creation...")
try:
    client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    print("   ✅ Client created successfully")
except Exception as e:
    print(f"   ❌ Error: {e}")
print()

# Test 4: Import InterviewAgent
print("4. Testing InterviewAgent import...")
try:
    from interview_agent import InterviewAgent
    print("   ✅ InterviewAgent imported successfully")
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()
print()

# Test 5: Create InterviewAgent
print("5. Testing InterviewAgent creation...")
try:
    agent = InterviewAgent(
        provider="anthropic",
        api_key=os.getenv('ANTHROPIC_API_KEY'),
        model=os.getenv('LLM_MODEL', 'claude-3-opus-20240229')
    )
    print("   ✅ Agent created successfully")
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()
print()

print("=== Test Complete ===")
