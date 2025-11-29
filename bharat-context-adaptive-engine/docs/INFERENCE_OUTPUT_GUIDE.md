# Inference Engine Output Guide

## Overview

Based on the signals you capture, the inference engine outputs **13 possible user need states** with associated UI modes, language preferences, and recommended actions.

---

## 📤 Complete Output Structure

For every inference request, you receive:

```json
{
  "success": true,
  "data": {
    "user_need_state": "State Name",
    "confidence": 8.5,
    "recommended_actions": [
      "Action 1",
      "Action 2",
      "Action 3",
      "Action 4",
      "Action 5"
    ],
    "ui_mode": "standard|lite|voice-first",
    "language_preference": "hindi|english|regional|mixed|system_default",
    "explanation": "Detailed explanation...",
    "matched_rule": "rule_name",
    "matched_signals": ["signal1", "signal2", ...],
    "signal_count": 4,
    "inference_timestamp": "2024-01-15T10:30:00"
  },
  "processing_time_ms": 25.5
}
```

---

## 🎯 All 13 User Need States

### 1. **Morning Devotional User**
- **When**: Morning time + Hindi/regional language + Voice input
- **UI**: Voice-first
- **Language**: Hindi

### 2. **Evening Ledger / Khatabook Mode User**
- **When**: Evening + Payment apps + Business apps + Tier-2/3/4 city
- **UI**: Standard
- **Language**: Hindi

### 3. **Student Exam Time User**
- **When**: Education apps + Long sessions + Long text input
- **UI**: Standard
- **Language**: Mixed

### 4. **Low-network Slow Device User**
- **When**: 2G/3G network + Low-end device + Slow network
- **UI**: Lite
- **Language**: System default

### 5. **Hindi-first User**
- **When**: Hindi system language + Hindi keyboard + Hindi region
- **UI**: Standard
- **Language**: Hindi

### 6. **Shop Owner / Kirana Workflow User**
- **When**: Payment apps + E-commerce apps + Business hours activity
- **UI**: Standard
- **Language**: Hindi

### 7. **Festival-Day User**
- **When**: Festival day detected + Regional holiday
- **UI**: Standard
- **Language**: Regional

### 8. **Voice-first User**
- **When**: Voice action + Microphone permission + No text input
- **UI**: Voice-first
- **Language**: System default

### 9. **AI Beginner / First-time Prompt Explorer**
- **When**: First install + No prompt attempted + Tutorial started
- **UI**: Standard
- **Language**: System default

### 10. **Regional Language User**
- **When**: Regional language (Tamil, Telugu, etc.) + Regional state
- **UI**: Standard
- **Language**: Regional

### 11. **Quick Task User**
- **When**: Short session + Immediate interaction + Short text
- **UI**: Lite
- **Language**: System default

### 12. **Power User / Tech-Savvy**
- **When**: High-end device + Fast network + Long sessions
- **UI**: Standard
- **Language**: English

### 13. **First-time AI Explorer** (Default)
- **When**: No rules match or insufficient signals
- **UI**: Standard
- **Language**: System default

---

## 🔄 Signal → Need State Mapping

### Example Mappings:

| Signals Captured | → | User Need State |
|-----------------|---|----------------|
| `time_of_day: "morning"` + `system_language: "hi"` + `first_action: "voice"` | → | **Morning Devotional User** |
| `business_apps: ["khatabook"]` + `time_of_day: "evening"` + `payment_apps: ["paytm"]` | → | **Evening Ledger User** |
| `education_apps: ["byjus"]` + `session_duration: "long"` | → | **Student Exam User** |
| `device_class: "low_end"` + `network_type: "3g"` + `network_speed: "slow"` | → | **Low-network Slow Device User** |
| `system_language: "hi"` + `keyboard_language: "hindi"` | → | **Hindi-first User** |
| `whatsapp_business_usage: "yes"` + `business_apps: ["khatabook"]` | → | **Shop Owner User** |
| `festival_day: "diwali"` | → | **Festival-Day User** |
| `first_action: "voice"` + `microphone_permission: "granted"` | → | **Voice-first User** |
| `first_prompt_attempted: "no"` + `tutorial_started: "yes"` | → | **AI Beginner User** |
| `system_language: "ta"` + `state: "TN"` | → | **Regional Language User** |
| `session_duration: "short"` + `text_input_length: "short"` | → | **Quick Task User** |
| `device_class: "high_end"` + `network_type: "wifi"` + `network_speed: "fast"` | → | **Power User** |

---

## 📊 Confidence Levels

- **0.0-3.9**: Low confidence (default/fallback)
- **4.0-6.9**: Medium confidence (some signals match)
- **7.0-10.0**: High confidence (strong signal match)

---

## 🎨 UI Modes Explained

1. **standard**: Full-featured UI
   - All features enabled
   - Rich formatting
   - Advanced prompts
   - Best for: Most users

2. **lite**: Minimal UI
   - Reduced assets
   - Text-only options
   - Offline-capable
   - Best for: Low-end devices, slow networks

3. **voice-first**: Voice-optimized UI
   - Large voice button
   - Voice examples
   - Voice-to-text hints
   - Best for: Voice preference users

---

## 🌐 Language Preferences Explained

1. **hindi**: Hindi interface and prompts
2. **english**: English interface
3. **regional**: Regional language (Tamil, Telugu, Bengali, etc.)
4. **mixed**: Mix of languages
5. **system_default**: Use device system language

---

## 📋 Recommended Actions

Each need state includes **3-5 recommended actions** that tell your app:
- What prompts to show
- What features to enable
- What UI elements to display
- What content to suggest

---

## 🔍 How Inference Works

1. **Signal Collection**: You send signals to `/v1/infer`
2. **Rule Scoring**: Engine scores all 12 rules against signals
3. **Web Intelligence**: Applies contextual knowledge
4. **App Context**: Analyzes ChatGPT-specific behaviors
5. **LLM Reasoning**: Applies worldly knowledge
6. **Final Decision**: Highest scoring rule wins
7. **Output Generation**: Creates recommendations and explanation

---

## 💡 Key Insights

- **Multiple signals** → Higher confidence
- **Signal correlation** → Better inference
- **Web intelligence** → Contextual understanding
- **App context** → ChatGPT-specific insights
- **LLM reasoning** → Worldly knowledge application

---

For detailed information about each need state, see `USER_NEED_STATES.md`.

