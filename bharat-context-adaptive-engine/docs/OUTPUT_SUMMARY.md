# Inference Engine Output Summary

## Quick Reference: What You Get

Based on the **signals you capture**, the inference engine outputs:

### ✅ **13 Possible User Need States**

1. **Morning Devotional User** - Voice-first, Hindi
2. **Evening Ledger / Khatabook Mode User** - Standard, Hindi
3. **Student Exam Time User** - Standard, Mixed
4. **Low-network Slow Device User** - Lite, System default
5. **Hindi-first User** - Standard, Hindi
6. **Shop Owner / Kirana Workflow User** - Standard, Hindi
7. **Festival-Day User** - Standard, Regional
8. **Voice-first User** - Voice-first, System default
9. **AI Beginner / First-time Prompt Explorer** - Standard, System default
10. **Regional Language User** - Standard, Regional
11. **Quick Task User** - Lite, System default
12. **Power User / Tech-Savvy** - Standard, English
13. **First-time AI Explorer** (Default) - Standard, System default

---

## 📤 Output Format

```json
{
  "user_need_state": "Evening Ledger / Khatabook Mode User",
  "confidence": 10.0,
  "recommended_actions": [
    "Show accounting and calculation prompts",
    "Suggest ledger entry templates",
    "Display number-to-words converter",
    "Show GST calculation helpers",
    "Suggest invoice generation prompts"
  ],
  "ui_mode": "standard",
  "language_preference": "hindi",
  "explanation": "Detailed explanation...",
  "matched_rule": "evening_ledger_user",
  "matched_signals": ["time_of_day", "hour_of_day", "payment_apps_installed", ...],
  "signal_count": 6
}
```

---

## 🎯 Real Example Output

**Input Signals:**
```json
{
  "business_apps": ["khatabook", "okcredit"],
  "whatsapp_business_usage": "yes",
  "payment_apps_installed": ["paytm", "phonepe", "gpay"],
  "time_of_day": "evening",
  "hour_of_day": 19,
  "otp_message_frequency": "high"
}
```

**Output:**
- **User Need State**: "Evening Ledger / Khatabook Mode User"
- **Confidence**: 10.0/10.0
- **UI Mode**: "standard"
- **Language**: "hindi"
- **Actions**: Accounting prompts, ledger templates, GST helpers

---

## 📊 Output Components

### 1. **user_need_state** (String)
The inferred user type/need state (one of 13 states)

### 2. **confidence** (Float: 0.0-10.0)
How confident the inference is:
- **High (7.0+)**: Strong signal match
- **Medium (4.0-6.9)**: Moderate match
- **Low (0.0-3.9)**: Weak match or default

### 3. **recommended_actions** (Array: 3-5 items)
Specific actions your app should take:
- What prompts to show
- What features to enable
- What UI elements to display

### 4. **ui_mode** (Enum)
- `"standard"` - Full-featured UI
- `"lite"` - Minimal UI (for low-end devices)
- `"voice-first"` - Voice-optimized UI

### 5. **language_preference** (Enum)
- `"hindi"` - Hindi interface
- `"english"` - English interface
- `"regional"` - Regional language
- `"mixed"` - Mix of languages
- `"system_default"` - Use system language

### 6. **explanation** (String)
Human-readable explanation of the inference process

### 7. **matched_rule** (String)
Name of the rule that matched

### 8. **matched_signals** (Array)
List of signals that contributed to the inference

### 9. **signal_count** (Integer)
Number of signals used in inference

---

## 🔄 Signal → Output Flow

```
Your Signals (200+ possible)
    ↓
Inference Engine Processing
    ├─ Rule Scoring
    ├─ Web Intelligence
    ├─ App Context
    └─ LLM Reasoning
    ↓
User Need State (1 of 13)
    ↓
Output with:
- UI Mode
- Language Preference
- Recommended Actions
- Confidence Score
- Explanation
```

---

## 📝 See Also

- **USER_NEED_STATES.md** - Detailed description of all 13 states
- **INFERENCE_OUTPUT_GUIDE.md** - Complete output guide
- **signals.md** - All possible signals you can capture

