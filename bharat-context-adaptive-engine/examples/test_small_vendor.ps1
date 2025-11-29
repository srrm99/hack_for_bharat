# Test script for Small Vendor Persona using PowerShell
# Runs inference and generates recommendations for Day-0, Day-1, Day-7

$baseUrl = "http://localhost:8000"
$signalsFile = Join-Path $PSScriptRoot "small_vendor_signals.json"

Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "SMALL VENDOR PERSONA - INFERENCE & RECOMMENDATIONS TEST" -ForegroundColor Green
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""

# Load signals
Write-Host "📊 Loading 50 signals for Small Vendor persona..." -ForegroundColor Yellow
$signalsData = Get-Content $signalsFile -Raw | ConvertFrom-Json
$signals = $signalsData.signals
$signalCount = ($signals.PSObject.Properties | Where-Object { $_.Value -ne $null }).Count
Write-Host "✅ Loaded $signalCount signals" -ForegroundColor Green
Write-Host ""

# Step 1: Run inference
Write-Host "🔍 Step 1: Running Enhanced Inference Engine..." -ForegroundColor Yellow
Write-Host ("-" * 80) -ForegroundColor Gray
try {
    $inferenceBody = @{
        signals = $signals
    } | ConvertTo-Json -Depth 10
    
    $inferenceResponse = Invoke-RestMethod -Uri "$baseUrl/v1/infer?enhanced=true" -Method POST -Body $inferenceBody -ContentType "application/json"
    
    if ($inferenceResponse.success) {
        $inference = $inferenceResponse.data
        Write-Host "✅ User Need State: $($inference.user_need_state)" -ForegroundColor Green
        Write-Host "📈 Confidence: $($inference.confidence)/10.0" -ForegroundColor Cyan
        Write-Host "🎨 UI Mode: $($inference.ui_mode)" -ForegroundColor Magenta
        Write-Host "🌐 Language: $($inference.language_preference)" -ForegroundColor Yellow
        Write-Host "📋 Matched Signals: $($inference.matched_signals.Count)" -ForegroundColor White
        Write-Host ""
        Write-Host "📝 Recommended Actions:" -ForegroundColor Cyan
        $i = 1
        foreach ($action in $inference.recommended_actions) {
            Write-Host "  $i. $action" -ForegroundColor White
            $i++
        }
        Write-Host ""
    } else {
        Write-Host "❌ Error: $($inferenceResponse.error)" -ForegroundColor Red
        exit
    }
} catch {
    Write-Host "❌ API Error: $_" -ForegroundColor Red
    Write-Host "Make sure the server is running: python main.py" -ForegroundColor Yellow
    exit
}

# Step 2: Generate recommendations for all days
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "🎯 Step 2: GENERATING RECOMMENDATIONS" -ForegroundColor Green
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""

try {
    $recBody = @{
        signals = $signals
    } | ConvertTo-Json -Depth 10
    
    $recResponse = Invoke-RestMethod -Uri "$baseUrl/v1/recommendations/all-days?enhanced=true" -Method POST -Body $recBody -ContentType "application/json"
    
    if ($recResponse.success) {
        $recommendations = $recResponse.recommendations
        
        # Day-0 Recommendations
        Write-Host "📅 DAY-0: Home Page Personalization" -ForegroundColor Yellow
        Write-Host ("-" * 80) -ForegroundColor Gray
        $day0 = $recommendations.day_0
        Write-Host "Outcome: $($day0.outcome)" -ForegroundColor White
        Write-Host "Delivery: $($day0.delivery_medium)" -ForegroundColor White
        Write-Host "Timing: $($day0.timing.when)" -ForegroundColor White
        Write-Host ""
        Write-Host "Content:" -ForegroundColor Cyan
        $content = $day0.content
        Write-Host "  Hero Prompt: $($content.hero_section.prompt)" -ForegroundColor White
        Write-Host "  Language: $($content.hero_section.language)" -ForegroundColor White
        Write-Host "  Quick Actions: $($content.quick_actions -join ', ')" -ForegroundColor White
        Write-Host "  Example Prompts:" -ForegroundColor White
        foreach ($prompt in $content.example_prompts) {
            Write-Host "    • $prompt" -ForegroundColor Gray
        }
        Write-Host ""
        
        # Day-1 Recommendations
        Write-Host "📅 DAY-1: Engagement (Push Notifications, Reminders, Daily Summaries)" -ForegroundColor Yellow
        Write-Host ("-" * 80) -ForegroundColor Gray
        $day1 = $recommendations.day_1
        Write-Host "Outcome: $($day1.outcome)" -ForegroundColor White
        Write-Host "Delivery: $($day1.delivery_medium -join ', ')" -ForegroundColor White
        Write-Host ""
        Write-Host "Push Notifications:" -ForegroundColor Cyan
        foreach ($notif in $day1.content.push_notifications) {
            Write-Host "  • $($notif.title)" -ForegroundColor White
            Write-Host "    $($notif.body)" -ForegroundColor Gray
            Write-Host "    Time: $($notif.time)" -ForegroundColor Gray
        }
        Write-Host ""
        Write-Host "Reminders:" -ForegroundColor Cyan
        foreach ($reminder in $day1.content.reminders) {
            Write-Host "  • $($reminder.message) (Time: $($reminder.time))" -ForegroundColor White
        }
        Write-Host ""
        Write-Host "Daily Summaries:" -ForegroundColor Cyan
        foreach ($summary in $day1.content.daily_summaries) {
            Write-Host "  • $($summary.title)" -ForegroundColor White
            Write-Host "    $($summary.content)" -ForegroundColor Gray
        }
        Write-Host ""
        
        # Day-7 Recommendations
        Write-Host "📅 DAY-7: Retention & Growth (Weekly Insights, Feature Suggestions)" -ForegroundColor Yellow
        Write-Host ("-" * 80) -ForegroundColor Gray
        $day7 = $recommendations.day_7
        Write-Host "Outcome: $($day7.outcome)" -ForegroundColor White
        Write-Host "Delivery: $($day7.delivery_medium -join ', ')" -ForegroundColor White
        Write-Host ""
        Write-Host "Weekly Insights:" -ForegroundColor Cyan
        foreach ($insight in $day7.content.weekly_insights) {
            Write-Host "  • $($insight.title)" -ForegroundColor White
            Write-Host "    $($insight.content)" -ForegroundColor Gray
        }
        Write-Host ""
        Write-Host "Feature Suggestions:" -ForegroundColor Cyan
        foreach ($feature in $day7.content.feature_suggestions) {
            Write-Host "  • $feature" -ForegroundColor White
        }
        Write-Host ""
        
        # Save results
        $results = @{
            inference = $inference
            recommendations = $recommendations
        }
        
        $outputFile = Join-Path $PSScriptRoot "small_vendor_results.json"
        $results | ConvertTo-Json -Depth 10 | Set-Content $outputFile -Encoding UTF8
        
        Write-Host "=" * 80 -ForegroundColor Cyan
        Write-Host "✅ Results saved to: $outputFile" -ForegroundColor Green
        Write-Host "=" * 80 -ForegroundColor Cyan
    } else {
        Write-Host "❌ Error: $($recResponse.error)" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ API Error: $_" -ForegroundColor Red
    Write-Host "Make sure the server is running: python main.py" -ForegroundColor Yellow
}

