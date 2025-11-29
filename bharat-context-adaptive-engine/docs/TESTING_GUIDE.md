# Testing Guide for Bharat Context-Adaptive Engine

## Quick Start Testing

### 1. Run Existing Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest test_inference_engine.py -v
pytest test_api.py -v

# Run with coverage
pytest --cov=. --cov-report=html
```

### 2. Start the Server for Manual Testing

```bash
# Start the server
python main.py

# Server will be available at http://localhost:8000
# API docs at http://localhost:8000/docs
```

---

## Testing Methods

### Method 1: Unit Tests (Automated)

#### Test Basic Inference Engine

```bash
pytest test_inference_engine.py -v
```

Tests cover:
- Morning devotional user
- Evening ledger user
- Low-network slow device user
- Hindi-first user
- Voice-first user
- AI beginner user
- Festival day user
- Default rule fallback

#### Test API Endpoints

```bash
pytest test_api.py -v
```

Tests cover:
- Root endpoint
- Health check
- Rules listing
- Inference endpoint (various scenarios)
- Batch inference

### Method 2: Manual API Testing

#### Using cURL

```bash
# Test basic inference
curl -X POST "http://localhost:8000/v1/infer" \
  -H "Content-Type: application/json" \
  -d '{
    "signals": {
      "time_of_day": "morning",
      "hour_of_day": 7,
      "system_language": "hi",
      "first_action": "voice",
      "device_class": "mid_range",
      "network_type": "4g"
    }
  }'

# Test enhanced inference (default)
curl -X POST "http://localhost:8000/v1/infer?enhanced=true" \
  -H "Content-Type: application/json" \
  -d '{
    "signals": {
      "business_apps": ["khatabook", "okcredit"],
      "whatsapp_business_usage": "yes",
      "payment_apps_installed": ["paytm", "phonepe"],
      "time_of_day": "evening",
      "hour_of_day": 19,
      "otp_message_frequency": "high"
    }
  }'

# Get explanation
curl -X GET "http://localhost:8000/v1/infer/explanation/{inference_id}"

# Health check
curl -X GET "http://localhost:8000/v1/health"
```

#### Using Python Requests

```python
import requests

# Test inference
response = requests.post(
    "http://localhost:8000/v1/infer",
    json={
        "signals": {
            "time_of_day": "morning",
            "hour_of_day": 7,
            "system_language": "hi",
            "first_action": "voice"
        }
    }
)

print(response.json())
```

#### Using FastAPI Interactive Docs

1. Start server: `python main.py`
2. Open browser: `http://localhost:8000/docs`
3. Click on `/v1/infer` endpoint
4. Click "Try it out"
5. Enter JSON payload
6. Click "Execute"

### Method 3: Python Test Script

Create a test script:

```python
# test_manual.py
from inference_engine_enhanced import get_enhanced_inference_engine
from models import RawSignals, DeviceClass, NetworkType, TimeOfDay

engine = get_enhanced_inference_engine()

# Test case 1: Business user
signals = RawSignals(
    business_apps=["khatabook", "okcredit"],
    whatsapp_business_usage="yes",
    payment_apps_installed=["paytm", "phonepe"],
    time_of_day=TimeOfDay.EVENING,
    hour_of_day=19,
    otp_message_frequency="high",
    system_language="hi"
)

result = engine.infer(signals)
print(f"User Need State: {result.user_need_state}")
print(f"Confidence: {result.confidence}")
print(f"Explanation:\n{result.explanation}")

# Get explanation
inference_id = list(engine.explanations.keys())[-1]
explanation = engine.get_explanation(inference_id)
print(f"\nDetailed Explanation:\n{explanation.generate_human_readable()}")
```

Run: `python test_manual.py`

---

## Test Scenarios

### Scenario 1: Morning Devotional User

```json
{
  "signals": {
    "time_of_day": "morning",
    "hour_of_day": 7,
    "system_language": "hi",
    "first_action": "voice",
    "festival_day": "diwali",
    "whatsapp_installed": "yes",
    "whatsapp_notification_frequency": "medium"
  }
}
```

**Expected**: Morning Devotional User, voice-first UI, Hindi language

### Scenario 2: Evening Ledger User (Enhanced)

```json
{
  "signals": {
    "time_of_day": "evening",
    "hour_of_day": 19,
    "business_apps": ["khatabook", "okcredit"],
    "whatsapp_business_usage": "yes",
    "payment_apps_installed": ["paytm", "phonepe", "gpay"],
    "otp_message_frequency": "high",
    "banking_sms_presence": "yes",
    "system_language": "hi",
    "city_tier": "tier3"
  }
}
```

**Expected**: Evening Ledger / Khatabook Mode User, high confidence (8.5+), business prompts

### Scenario 3: Student Exam User

```json
{
  "signals": {
    "education_apps": ["byjus", "unacademy"],
    "session_duration": "long",
    "text_input_length": "long",
    "total_notification_volume": "low",
    "time_of_day": "afternoon",
    "hour_of_day": 14,
    "return_user": "yes"
  }
}
```

**Expected**: Student Exam Time User, standard UI, mixed language

### Scenario 4: Low-network Slow Device User

```json
{
  "signals": {
    "device_class": "low_end",
    "network_type": "3g",
    "network_speed": "slow",
    "ram_size": "2GB",
    "connection_stability": "unstable",
    "data_saver_mode": "enabled",
    "app_launch_time": "slow"
  }
}
```

**Expected**: Low-network Slow Device User, lite UI mode

### Scenario 5: WhatsApp Business User

```json
{
  "signals": {
    "whatsapp_installed": "yes",
    "whatsapp_active": "yes",
    "whatsapp_business_usage": "yes",
    "whatsapp_group_activity": "high",
    "whatsapp_notification_frequency": "high",
    "business_apps": ["khatabook"],
    "payment_apps_installed": ["paytm"]
  }
}
```

**Expected**: Shop Owner / Kirana Workflow User

### Scenario 6: High OTP Frequency User

```json
{
  "signals": {
    "otp_message_frequency": "high",
    "banking_sms_presence": "yes",
    "ecommerce_sms_presence": "yes",
    "payment_apps_installed": ["paytm", "phonepe", "gpay"],
    "banking_apps": "yes",
    "sms_response_time": "immediate"
  }
}
```

**Expected**: Transaction-heavy user, high digital payment activity

---

## Testing Enhanced Engine Features

### Test Web Intelligence

```python
from web_intelligence import WebIntelligence
from models import RawSignals

web_intel = WebIntelligence()
signals = RawSignals(
    business_apps=["khatabook"],
    whatsapp_business_usage="yes",
    otp_message_frequency="high"
)

result = web_intel.analyze_signals(signals)
print("Detected Patterns:", result["detected_patterns"])
print("Insights:", result["insights"])
print("Confidence Adjustments:", result["confidence_adjustments"])
```

### Test App Context

```python
from app_context import AppContext
from models import RawSignals

app_context = AppContext()
signals = RawSignals(
    first_action="voice",
    education_apps=["byjus"],
    session_duration="long"
)

result = app_context.analyze_app_context(signals)
print("Detected Use Cases:", result["detected_use_cases"])
print("Prompt Suggestions:", result["prompt_suggestions"])
print("UI Recommendations:", result["ui_recommendations"])
```

### Test LLM Reasoning

```python
from llm_reasoning import LLMReasoning
from models import RawSignals

llm_reasoning = LLMReasoning()
signals = RawSignals(
    business_apps=["khatabook"],
    whatsapp_business_usage="yes",
    time_of_day=TimeOfDay.EVENING
)

web_intel = {}  # From web intelligence
app_context = {}  # From app context

result = llm_reasoning.reason(signals, web_intel, app_context)
print("Insights:", result["insights"])
print("Reasoning Steps:", result["reasoning_steps"])
```

### Test Explanation System

```python
from inference_engine_enhanced import get_enhanced_inference_engine
from models import RawSignals

engine = get_enhanced_inference_engine()
signals = RawSignals(
    business_apps=["khatabook"],
    whatsapp_business_usage="yes",
    time_of_day=TimeOfDay.EVENING
)

result = engine.infer(signals)

# Get explanation
inference_id = list(engine.explanations.keys())[-1]
explanation = engine.get_explanation(inference_id)

# Print human-readable explanation
print(explanation.generate_human_readable())

# Log to file
engine.log_explanation(inference_id)
```

---

## Testing Checklist

### Basic Functionality
- [ ] Inference engine loads rules correctly
- [ ] Signals are extracted properly
- [ ] Rules are scored correctly
- [ ] User need state is inferred
- [ ] Recommendations are generated
- [ ] Confidence scores are calculated

### Enhanced Features
- [ ] Web intelligence detects patterns
- [ ] App context identifies use cases
- [ ] LLM reasoning applies knowledge
- [ ] Confidence adjustments are applied
- [ ] Signal correlations are detected
- [ ] Multi-source agreement boosts confidence

### Explanation System
- [ ] Explanation events are created
- [ ] Human-readable explanation is generated
- [ ] Explanation can be retrieved by ID
- [ ] Explanation can be logged to file
- [ ] All reasoning steps are logged

### API Endpoints
- [ ] `/v1/infer` works with enhanced engine
- [ ] `/v1/infer/explanation/{id}` returns explanation
- [ ] `/v1/infer/log/{id}` logs explanation
- [ ] `/v1/health` returns correct status
- [ ] `/v1/rules` lists all rules

### Edge Cases
- [ ] Minimal signals (default rule)
- [ ] No matching rules
- [ ] Missing signal categories
- [ ] Invalid signal values
- [ ] Empty signals
- [ ] Very high confidence
- [ ] Very low confidence

---

## Performance Testing

### Load Testing

```python
import time
import requests
from concurrent.futures import ThreadPoolExecutor

def test_inference():
    response = requests.post(
        "http://localhost:8000/v1/infer",
        json={"signals": {"device_class": "mid_range"}}
    )
    return response.elapsed.total_seconds()

# Test with 100 requests
with ThreadPoolExecutor(max_workers=10) as executor:
    times = list(executor.map(lambda _: test_inference(), range(100)))

print(f"Average time: {sum(times)/len(times):.3f}s")
print(f"Min: {min(times):.3f}s, Max: {max(times):.3f}s")
```

### Memory Testing

```python
import tracemalloc
from inference_engine_enhanced import get_enhanced_inference_engine

tracemalloc.start()

engine = get_enhanced_inference_engine()
# Run multiple inferences
for i in range(100):
    # ... inference code ...

current, peak = tracemalloc.get_traced_memory()
print(f"Current: {current / 1024 / 1024:.2f} MB")
print(f"Peak: {peak / 1024 / 1024:.2f} MB")
```

---

## Debugging Tips

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Explanation Events

```python
explanation = engine.get_explanation(inference_id)
for event in explanation.events:
    print(f"[{event.step}] {event.event_type.value}")
    print(f"  Description: {event.description}")
    if event.reasoning:
        print(f"  Reasoning: {event.reasoning}")
```

### Validate Signals

```python
from models import RawSignals

try:
    signals = RawSignals(**payload["signals"])
    print("Signals valid")
except Exception as e:
    print(f"Signal validation error: {e}")
```

### Check Rule Scores

```python
rule_scores = engine.score_rules(signals)
for rule, score, conditions, top_signals in rule_scores[:5]:
    print(f"{rule.name}: {score:.2f} ({len(conditions)} conditions)")
```

---

## Continuous Testing

### Run Tests on File Change

```bash
# Install pytest-watch
pip install pytest-watch

# Watch for changes and run tests
ptw
```

### Pre-commit Testing

```bash
# Run tests before commit
pytest && git commit -m "Your message"
```

---

## Test Data

See `example_payloads.json` for comprehensive test payloads covering:
- Morning Devotional User
- Evening Ledger User
- Student Exam User
- Low-network User
- Hindi-first User
- Shop Owner User
- Festival-Day User
- Voice-first User
- AI Beginner User
- Regional Language User
- WhatsApp Business User (new)
- SMS Heavy User (new)
- High Notification User (new)

---

## Troubleshooting

### Tests Failing?

1. Check if rules.yaml exists and is valid
2. Verify all dependencies are installed
3. Check Python version (3.8+)
4. Review error messages for specific issues

### API Not Responding?

1. Check if server is running
2. Verify port 8000 is available
3. Check for import errors in logs
4. Verify rules.yaml is loaded

### Explanation Not Generated?

1. Ensure enhanced engine is used (`enhanced=true`)
2. Check if inference_id is captured
3. Verify explanation events are created
4. Check file permissions for logging

---

## Next Steps

1. Add more test scenarios
2. Create integration tests
3. Set up CI/CD testing
4. Add performance benchmarks
5. Create test data generator

