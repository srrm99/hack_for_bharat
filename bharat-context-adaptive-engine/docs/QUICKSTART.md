# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Start the Server

```bash
python main.py
```

The server will start at `http://localhost:8000`

### Step 3: Test the API

Open your browser and go to:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/v1/health

### Step 4: Make Your First Inference Request

Using curl:

```bash
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
```

Using Python:

```python
import requests

payload = {
    "signals": {
        "time_of_day": "morning",
        "hour_of_day": 7,
        "system_language": "hi",
        "first_action": "voice"
    }
}

response = requests.post("http://localhost:8000/v1/infer", json=payload)
print(response.json())
```

### Step 5: Run Tests

```bash
pytest
```

## 📝 Example Payloads

See `example_payloads.json` for complete examples of different user scenarios.

## 🔧 Configuration

- **Rules**: Edit `rules.yaml` to modify inference rules
- **Signals**: See `signals.md` for available signals
- **API**: See `README.md` for full documentation

## 🎯 Common Use Cases

### Morning Devotional User
```json
{
  "signals": {
    "time_of_day": "morning",
    "hour_of_day": 7,
    "system_language": "hi",
    "first_action": "voice"
  }
}
```

### Low-network User
```json
{
  "signals": {
    "network_type": "3g",
    "network_speed": "slow",
    "device_class": "low_end"
  }
}
```

### Hindi-first User
```json
{
  "signals": {
    "system_language": "hi",
    "keyboard_language": "hindi",
    "state": "UP"
  }
}
```

## 🐛 Troubleshooting

**Server won't start?**
- Check Python version: `python --version` (needs 3.8+)
- Install dependencies: `pip install -r requirements.txt`

**Rules not loading?**
- Ensure `rules.yaml` exists in project root
- Check YAML syntax is valid

**API returns errors?**
- Check request payload format
- Verify all signal values are valid (see `signals.md`)

## 📚 Next Steps

1. Read `README.md` for full documentation
2. Review `signals.md` for available signals
3. Customize `rules.yaml` for your use case
4. Run tests to verify everything works

