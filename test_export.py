"""Test export API endpoint"""
import requests
import json

# Test data
test_session = {
    "template_id": "standard",
    "created_at": "2025-11-20T15:00:00",
    "updated_at": "2025-11-20T15:30:00",
    "current_fase": 1,
    "total_fases": 11,
    "messages": [
        {"role": "assistant", "content": "Hallo!", "timestamp": "2025-11-20T15:00:00"},
        {"role": "user", "content": "We zijn een tech startup", "timestamp": "2025-11-20T15:01:00"}
    ],
    "structured_data": {
        "fase_1": {
            "fase_name": "Organisatie Context",
            "data": {
                "organisatie_naam": "Test BV",
                "sector": "IT",
                "aantal_medewerkers": 85
            }
        }
    },
    "followup_stats": {
        "total_questions": 5,
        "followup_questions": 2
    }
}

# Test JSON export
print("Testing JSON export...")
response = requests.post(
    "https://hr.agentboss.nl/api/export",
    json={"format": "json", "session": test_session}
)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    with open("test_export.json", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("✅ JSON export saved to test_export.json")
else:
    print(f"❌ Error: {response.text}")

# Test CSV export
print("\nTesting CSV export...")
response = requests.post(
    "https://hr.agentboss.nl/api/export",
    json={"format": "csv", "session": test_session}
)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    with open("test_export.csv", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("✅ CSV export saved to test_export.csv")
else:
    print(f"❌ Error: {response.text}")

# Test Markdown export
print("\nTesting Markdown export...")
response = requests.post(
    "https://hr.agentboss.nl/api/export",
    json={"format": "md", "session": test_session}
)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    with open("test_export.md", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("✅ Markdown export saved to test_export.md")
    print("\nMarkdown preview:")
    print(response.text[:500])
else:
    print(f"❌ Error: {response.text}")
