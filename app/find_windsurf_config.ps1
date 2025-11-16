# Windsurf API Configuration Finder
Write-Host "🔍 Zoeken naar Windsurf API configuratie..." -ForegroundColor Cyan
Write-Host ""

# Check 1: Windsurf AppData folder
$windsurfPath = "$env:APPDATA\Windsurf"
if (Test-Path $windsurfPath) {
    Write-Host "✅ Windsurf gevonden in: $windsurfPath" -ForegroundColor Green
    
    # Look for settings files
    Write-Host "`n📁 Zoeken naar configuratie bestanden..." -ForegroundColor Yellow
    
    $settingsFiles = Get-ChildItem $windsurfPath -Recurse -File -ErrorAction SilentlyContinue | 
        Where-Object { $_.Name -match "settings|config|storage" -and $_.Extension -eq ".json" } |
        Select-Object -First 10
    
    foreach ($file in $settingsFiles) {
        Write-Host "   📄 $($file.FullName)" -ForegroundColor Gray
        
        # Try to read and search for API keys
        try {
            $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
            if ($content -match "api.*key|openai|anthropic|claude|gpt") {
                Write-Host "      ⭐ Dit bestand bevat mogelijk API configuratie!" -ForegroundColor Green
                
                # Show relevant lines (without exposing full keys)
                $lines = $content -split "`n" | Where-Object { $_ -match "api|key|openai|anthropic" }
                foreach ($line in $lines | Select-Object -First 5) {
                    $safeLine = $line -replace '(sk-[a-zA-Z0-9]{20})[a-zA-Z0-9]+', '$1...'
                    Write-Host "      $safeLine" -ForegroundColor DarkGray
                }
            }
        } catch {
            # Silently continue
        }
    }
} else {
    Write-Host "❌ Windsurf folder niet gevonden" -ForegroundColor Red
}

# Check 2: Environment Variables
Write-Host "`n🔐 Checken environment variables..." -ForegroundColor Yellow
$apiVars = Get-ChildItem Env: | Where-Object { 
    $_.Name -like "*API*" -or 
    $_.Name -like "*KEY*" -or 
    $_.Name -like "*OPENAI*" -or 
    $_.Name -like "*ANTHROPIC*" -or 
    $_.Name -like "*WINDSURF*" 
}

if ($apiVars) {
    foreach ($var in $apiVars) {
        $safeValue = if ($var.Value -match "^sk-") {
            $var.Value.Substring(0, [Math]::Min(15, $var.Value.Length)) + "..."
        } else {
            $var.Value
        }
        Write-Host "   $($var.Name) = $safeValue" -ForegroundColor Gray
    }
} else {
    Write-Host "   Geen API-gerelateerde environment variables gevonden" -ForegroundColor Gray
}

# Check 3: Windsurf Extension Storage
Write-Host "`n🔌 Checken Windsurf extensions..." -ForegroundColor Yellow
$extensionsPath = "$windsurfPath\User\globalStorage"
if (Test-Path $extensionsPath) {
    $storageFiles = Get-ChildItem $extensionsPath -Recurse -Filter "*.json" -ErrorAction SilentlyContinue |
        Select-Object -First 5
    
    foreach ($file in $storageFiles) {
        try {
            $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
            if ($content -match "apiKey|api_key") {
                Write-Host "   📄 $($file.Name) bevat mogelijk API keys" -ForegroundColor Green
            }
        } catch {
            # Silently continue
        }
    }
}

# Recommendations
Write-Host "`n💡 Aanbevelingen:" -ForegroundColor Cyan
Write-Host ""
Write-Host "Optie 1: Gebruik OpenAI direct" -ForegroundColor White
Write-Host "   1. Ga naar https://platform.openai.com/api-keys" -ForegroundColor Gray
Write-Host "   2. Maak een nieuwe API key" -ForegroundColor Gray
Write-Host "   3. Kopieer naar .env: OPENAI_API_KEY=sk-..." -ForegroundColor Gray
Write-Host ""
Write-Host "Optie 2: Gebruik Anthropic (Claude)" -ForegroundColor White
Write-Host "   1. Ga naar https://console.anthropic.com/" -ForegroundColor Gray
Write-Host "   2. Maak een API key" -ForegroundColor Gray
Write-Host "   3. Kopieer naar .env: ANTHROPIC_API_KEY=sk-ant-..." -ForegroundColor Gray
Write-Host ""
Write-Host "Optie 3: Check Windsurf Settings" -ForegroundColor White
Write-Host "   1. Open Windsurf" -ForegroundColor Gray
Write-Host "   2. Ga naar Settings (Ctrl+,)" -ForegroundColor Gray
Write-Host "   3. Zoek naar 'API' of 'LLM'" -ForegroundColor Gray
Write-Host "   4. Kopieer de key als je die vindt" -ForegroundColor Gray
Write-Host ""

Write-Host "✅ Scan compleet!" -ForegroundColor Green
Write-Host ""
Write-Host "Volgende stap: Configureer .env in app/backend/" -ForegroundColor Cyan
