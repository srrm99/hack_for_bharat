# Bharat Context-Adaptive Engine

**Inference Engine for Day-0 Cold Start Problem - Tier-2/3/4 Indian Users**

This engine helps ChatGPT penetrate Tier-2/3/4 users in India by solving the Day-0 Cold Start problem using implicit context signals. It delivers hyper-relevant Day-0 UI + suggested actions for new ChatGPT users *without asking them anything*, using **implicit signals only**.

---

## 🎯 Problem Statement

Tier-2/3/4 Indian users often uninstall apps instantly because:
- They see generic, English-first screens
- They don't type prompts
- They have low-end devices & weak networks
- They rarely provide explicit preferences

**Solution**: A context inference engine that uses implicit signals to infer user needs and adapt the UI accordingly.

---

## 🏗️ Architecture

### Core Components

1. **Signals Collection** (`signals.md`)
   - Exhaustive taxonomy of implicit signals
   - Device, Network, Locale, Time, Commerce, Cultural signals
   - Privacy-first, coarse-grained, non-identifying

2. **Inference Rules** (`rules.yaml`)
   - YAML-based rule definitions
   - Weighted scoring system
   - Extensible rule engine

3. **Inference Engine** (`inference_engine.py`)
   - Signal extraction and validation
   - Rule scoring and matching
   - User need state inference
   - Recommendation generation

4. **API Layer** (`main.py`, `router_inference.py`)
   - FastAPI REST API
   - `/v1/infer` endpoint
   - Health checks and monitoring

5. **Data Models** (`models.py`)
   - Pydantic models for type safety
   - Request/Response schemas

---

## 📦 Installation

### Prerequisites

- Python 3.8+
- pip

### Setup

```bash
# Clone or navigate to project directory
cd Bharat

# Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Usage

### Start the Server

```bash
# Development mode (with auto-reload)
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Endpoints

#### 1. Infer User Need State

**POST** `/v1/infer`

Infer user need state from implicit signals.

**Request Body:**
```json
{
  "signals": {
    "time_of_day": "morning",
    "hour_of_day": 7,
    "system_language": "hi",
    "first_action": "voice",
    "device_class": "low_end",
    "network_type": "3g",
    "network_speed": "slow",
    "city_tier": "tier3"
  },
  "user_id": "optional_anonymous_id",
  "session_id": "optional_session_id"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user_need_state": "Morning Devotional User",
    "confidence": 7.5,
    "recommended_actions": [
      "Show devotional prompt suggestions (Bhajans, prayers, religious quotes)",
      "Enable voice input by default",
      "Display regional language interface",
      "Suggest morning routine prompts",
      "Show festival-specific content if applicable"
    ],
    "ui_mode": "voice-first",
    "language_preference": "hindi",
    "explanation": "Inferred 'Morning Devotional User' with confidence 7.5/10.0 based on 4 matching signals: time_of_day, hour_of_day, system_language, first_action. Key indicators: time_of_day=morning, hour_of_day=7, system_language=hi.",
    "matched_rule": "morning_devotional_user",
    "matched_signals": ["time_of_day", "hour_of_day", "system_language", "first_action"],
    "signal_count": 4
  },
  "processing_time_ms": 12.5
}
```

#### 2. Health Check

**GET** `/v1/health`

Check service health and configuration.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "rules_loaded": true,
  "rules_count": 11,
  "timestamp": "2024-01-15T10:30:00"
}
```

#### 3. List Rules

**GET** `/v1/rules`

List all available inference rules.

**Response:**
```json
{
  "total_rules": 11,
  "rules": [
    {
      "name": "morning_devotional_user",
      "description": "User likely engaging in morning devotional/religious activities",
      "confidence_threshold": 4.0,
      "condition_count": 5
    },
    ...
  ],
  "scoring_method": "weighted_sum",
  "default_rule": "First-time AI Explorer"
}
```

#### 4. Batch Inference

**POST** `/v1/infer/batch`

Process multiple inference requests in a single call.

---

## 📋 Example Use Cases

### Example 1: Morning Devotional User

```python
import requests

payload = {
    "signals": {
        "time_of_day": "morning",
        "hour_of_day": 7,
        "system_language": "hi",
        "first_action": "voice",
        "festival_day": "diwali"
    }
}

response = requests.post("http://localhost:8000/v1/infer", json=payload)
result = response.json()

print(f"User Need State: {result['data']['user_need_state']}")
print(f"Confidence: {result['data']['confidence']}")
print(f"UI Mode: {result['data']['ui_mode']}")
```

### Example 2: Evening Ledger User

```python
payload = {
    "signals": {
        "time_of_day": "evening",
        "hour_of_day": 19,
        "day_of_week": "monday",
        "payment_apps_installed": ["paytm", "phonepe"],
        "city_tier": "tier3",
        "text_input_length": "medium"
    }
}

response = requests.post("http://localhost:8000/v1/infer", json=payload)
result = response.json()
```

### Example 3: Low-network Slow Device User

```python
payload = {
    "signals": {
        "network_type": "3g",
        "network_speed": "slow",
        "device_class": "low_end",
        "ram_size": "2GB",
        "connection_stability": "unstable",
        "data_saver_mode": "enabled"
    }
}

response = requests.post("http://localhost:8000/v1/infer", json=payload)
result = response.json()
```

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest test_inference_engine.py
pytest test_api.py

# Run with coverage
pytest --cov=. --cov-report=html
```

### Test Coverage

- Unit tests for inference engine
- Rule condition evaluation tests
- API endpoint integration tests
- Edge cases and error handling

---

## 📊 User Need States

The engine can infer the following user need states (and more):

1. **Morning Devotional User** - Morning religious/devotional activities
2. **Evening Ledger / Khatabook Mode User** - Shop owner doing evening accounting
3. **Student Exam Time User** - Student preparing for exams
4. **Low-network Slow Device User** - User with poor network/device
5. **Hindi-first User** - User preferring Hindi interface
6. **Shop Owner / Kirana Workflow User** - Small business owner
7. **Festival-Day User** - User on a festival day
8. **Voice-first User** - User preferring voice input
9. **AI Beginner / First-time Prompt Explorer** - New AI user
10. **Regional Language User** - Non-Hindi regional language user
11. **Quick Task User** - User wanting quick, single-purpose tasks
12. **Power User / Tech-Savvy** - Advanced user with high-end device

---

## 🔧 Configuration

### Rules Configuration

Edit `rules.yaml` to:
- Add new inference rules
- Modify existing rule conditions
- Adjust confidence thresholds
- Update recommended actions

### Signal Collection

Refer to `signals.md` for:
- Complete signal taxonomy
- Signal collection guidelines
- Privacy principles
- Signal priority levels

---

## 🏗️ Extending the Engine

### Adding New Rules

1. Open `rules.yaml`
2. Add a new rule entry:

```yaml
- name: new_user_type
  description: Description of the user type
  conditions:
    - signal: signal_name
      operator: equals
      value: "value"
      weight: 2.0
  output:
    user_need_state: "New User Type"
    ui_mode: "standard"
    language_preference: "system_default"
    confidence_threshold: 5.0
    recommended_actions:
      - "Action 1"
      - "Action 2"
      - "Action 3"
```

3. Restart the server (rules are loaded at startup)

### Adding New Signals

1. Add signal to `signals.md` taxonomy
2. Add signal field to `RawSignals` model in `models.py`
3. Update rules in `rules.yaml` to use the new signal

### ML-Based Scoring (Future)

The architecture supports extending to ML-based scoring:
- Replace `score_rules()` with ML model inference
- Keep the same API interface
- Use signals as feature vectors
- Train models on historical inference data

---

## 🔒 Privacy & Security

### Privacy Principles

- **No PII Collection**: All signals are coarse-grained and non-identifying
- **Opt-Out Friendly**: No personal data collection
- **Coarse Signals Only**: Device class, network type, time patterns, etc.
- **No Tracking**: Signals are not linked to user identity

### Security Best Practices

- Use HTTPS in production
- Implement rate limiting
- Add authentication/authorization as needed
- Validate and sanitize all inputs
- Monitor for abuse

---

## 📈 Performance

- **Latency**: < 50ms per inference (typical)
- **Throughput**: 1000+ requests/second (depends on hardware)
- **Memory**: ~50MB base + rules
- **CPU**: Minimal (rule-based scoring)

---

## 🐛 Troubleshooting

### Rules Not Loading

- Check that `rules.yaml` exists in the project root
- Verify YAML syntax is valid
- Check file permissions

### Inference Returns Default Rule

- Verify signals are being sent correctly
- Check signal values match rule conditions
- Review confidence thresholds in rules

### API Errors

- Check FastAPI logs
- Verify request payload format
- Ensure all required fields are present

---

## 📝 License

[Add your license here]

---

## 🤝 Contributing

[Add contribution guidelines]

---

## 📧 Contact

[Add contact information]

---

## 🙏 Acknowledgments

Built for solving the Day-0 Cold Start problem for Tier-2/3/4 Indian users.

