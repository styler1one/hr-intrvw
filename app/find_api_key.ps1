Write-Host "=== Windsurf API Key Finder ===" -ForegroundColor Cyan
Write-Host ""

# Check Windsurf folder
$windsurfPath = "$env:APPDATA\Windsurf"
Write-Host "Windsurf locatie: $windsurfPath"

if (Test-Path $windsurfPath) {
    Write-Host "Status: Gevonden!" -ForegroundColor Green
} else {
    Write-Host "Status: Niet gevonden" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Aanbeveling ===" -ForegroundColor Yellow
Write-Host ""
Write-Host "Windsurf heeft waarschijnlijk geen eigen API endpoint."
Write-Host "Gebruik in plaats daarvan OpenAI of Anthropic direct:"
Write-Host ""
Write-Host "OPTIE 1: OpenAI (Aanbevolen)" -ForegroundColor Green
Write-Host "  1. Ga naar: https://platform.openai.com/api-keys"
Write-Host "  2. Maak een nieuwe API key"
Write-Host "  3. Kopieer de key (begint met sk-)"
Write-Host "  4. Plak in .env: OPENAI_API_KEY=sk-your-key"
Write-Host ""
Write-Host "OPTIE 2: Anthropic Claude" -ForegroundColor Green
Write-Host "  1. Ga naar: https://console.anthropic.com/"
Write-Host "  2. Maak een API key"
Write-Host "  3. Kopieer de key (begint met sk-ant-)"
Write-Host "  4. Plak in .env: ANTHROPIC_API_KEY=sk-ant-your-key"
Write-Host ""
Write-Host "Druk op een toets om door te gaan..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
