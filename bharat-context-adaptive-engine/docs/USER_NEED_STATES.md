# User Need States - Complete Reference

This document lists all possible user need states that the inference engine can output based on the signals captured.

---

## 📊 Output Format

For each inference, the engine returns:

```json
{
  "user_need_state": "State Name",
  "confidence": 8.5,
  "recommended_actions": ["action1", "action2", ...],
  "ui_mode": "standard|lite|voice-first",
  "language_preference": "hindi|english|regional|mixed|system_default",
  "explanation": "Detailed explanation...",
  "matched_rule": "rule_name",
  "matched_signals": ["signal1", "signal2", ...],
  "signal_count": 4
}
```

---

## 🎯 All Possible User Need States

### 1. **Morning Devotional User**

**Description**: User likely engaging in morning devotional/religious activities

**Key Signals**:
- `time_of_day`: "early_morning" or "morning"
- `hour_of_day`: 5-9
- `system_language`: Hindi or regional (hi, mr, gu, te, ta)
- `first_action`: "voice"
- `festival_day`: Not "none" (optional)

**Output**:
- **UI Mode**: `voice-first`
- **Language**: `hindi`
- **Confidence Threshold**: 4.0
- **Recommended Actions**:
  - Show devotional prompt suggestions (Bhajans, prayers, religious quotes)
  - Enable voice input by default
  - Display regional language interface
  - Suggest morning routine prompts
  - Show festival-specific content if applicable

---

### 2. **Evening Ledger / Khatabook Mode User**

**Description**: Shop owner or small business person doing evening accounting

**Key Signals**:
- `time_of_day`: "evening" or "night"
- `hour_of_day`: 18-22
- `day_of_week`: Weekday (Mon-Fri)
- `payment_apps_installed`: ["paytm", "phonepe", "gpay", "multiple"]
- `city_tier`: "tier2", "tier3", "tier4", or "rural"
- `text_input_length`: "medium"

**Output**:
- **UI Mode**: `standard`
- **Language**: `hindi`
- **Confidence Threshold**: 5.0
- **Recommended Actions**:
  - Show accounting and calculation prompts
  - Suggest ledger entry templates
  - Display number-to-words converter
  - Show GST calculation helpers
  - Suggest invoice generation prompts

---

### 3. **Student Exam Time User**

**Description**: Student preparing for exams or studying

**Key Signals**:
- `time_of_day`: "morning", "afternoon", or "evening"
- `hour_of_day`: 6-22
- `device_class`: "low_end" or "mid_range"
- `session_duration`: "medium" or "long"
- `text_input_length`: "medium" or "long"
- `return_user`: "yes"

**Output**:
- **UI Mode**: `standard`
- **Language**: `mixed`
- **Confidence Threshold**: 6.0
- **Recommended Actions**:
  - Show study and exam preparation prompts
  - Suggest subject-specific help (Math, Science, English)
  - Display quick Q&A format suggestions
  - Show essay writing helpers
  - Suggest revision and summary prompts

---

### 4. **Low-network Slow Device User**

**Description**: User with poor network and/or low-end device

**Key Signals**:
- `network_type`: "2g" or "3g"
- `network_speed`: "slow"
- `device_class`: "low_end"
- `ram_size`: "1GB" or "2GB"
- `connection_stability`: "unstable" or "intermittent"
- `data_saver_mode`: "enabled"
- `app_launch_time`: "medium" or "slow"

**Output**:
- **UI Mode**: `lite`
- **Language**: `system_default`
- **Confidence Threshold**: 6.0
- **Recommended Actions**:
  - Enable lite mode with minimal UI
  - Reduce image/asset loading
  - Suggest offline-capable features
  - Show text-only interface options
  - Enable aggressive caching

---

### 5. **Hindi-first User**

**Description**: User prefers Hindi language interface

**Key Signals**:
- `system_language`: "hi"
- `keyboard_language`: Contains "hindi"
- `state`: Hindi-speaking states (UP, MP, BH, RJ, HR, DL)
- `language_region`: "hindi"
- `text_input_length`: Not "none"

**Output**:
- **UI Mode**: `standard`
- **Language**: `hindi`
- **Confidence Threshold**: 5.0
- **Recommended Actions**:
  - Display Hindi interface by default
  - Show Hindi prompt examples
  - Enable Hindi voice input
  - Suggest Hindi content prompts
  - Show Devanagari keyboard hints

---

### 6. **Shop Owner / Kirana Workflow User**

**Description**: Small shop or kirana store owner

**Key Signals**:
- `payment_apps_installed`: ["paytm", "phonepe", "gpay", "multiple"]
- `ecommerce_apps`: ["flipkart", "amazon", "meesho", "multiple"]
- `business_hours_activity`: "yes"
- `city_tier`: "tier2", "tier3", or "tier4"
- `time_of_day`: "morning", "afternoon", or "evening"
- `session_frequency`: "multiple"

**Output**:
- **UI Mode**: `standard`
- **Language**: `hindi`
- **Confidence Threshold**: 5.0
- **Recommended Actions**:
  - Show business calculation prompts
  - Suggest inventory management helpers
  - Display price comparison tools
  - Show customer communication templates
  - Suggest GST and tax calculation prompts

---

### 7. **Festival-Day User**

**Description**: User on a festival day

**Key Signals**:
- `festival_day`: Not "none" (diwali, holi, eid, dussehra, pongal, etc.)
- `regional_holiday`: "yes"
- `system_language`: Hindi or regional (hi, mr, gu, te, ta, bn)

**Output**:
- **UI Mode**: `standard`
- **Language**: `regional`
- **Confidence Threshold**: 5.0
- **Recommended Actions**:
  - Show festival-specific greetings and messages
  - Suggest festival-related prompts (recipes, wishes, quotes)
  - Display regional language interface
  - Show sharing templates for festival messages
  - Suggest creative content for festival posts

---

### 8. **Voice-first User**

**Description**: User prefers voice input over typing

**Key Signals**:
- `first_action`: "voice"
- `voice_button_tapped`: "yes"
- `microphone_permission`: "granted"
- `text_input_length`: "none"
- `keyboard_opened`: "no"
- `system_language`: Hindi or regional (optional)

**Output**:
- **UI Mode**: `voice-first`
- **Language**: `system_default`
- **Confidence Threshold**: 6.0
- **Recommended Actions**:
  - Enable voice input by default
  - Show voice command examples
  - Display large voice button
  - Suggest voice-friendly prompts
  - Show voice-to-text conversion hints

---

### 9. **AI Beginner / First-time Prompt Explorer**

**Description**: First-time user exploring AI capabilities

**Key Signals**:
- `time_since_install`: "immediate"
- `first_prompt_attempted`: "no"
- `example_prompts_viewed`: "yes"
- `tutorial_started`: "yes"
- `help_faq_opened`: "yes"
- `time_to_first_interaction`: "delayed" or "quick"
- `text_input_length`: "none"

**Output**:
- **UI Mode**: `standard`
- **Language**: `system_default`
- **Confidence Threshold**: 6.0
- **Recommended Actions**:
  - Show interactive tutorial
  - Display example prompts prominently
  - Suggest beginner-friendly prompts
  - Show 'What can I ask?' examples
  - Enable guided onboarding

---

### 10. **Regional Language User**

**Description**: User from non-Hindi speaking region

**Key Signals**:
- `system_language`: Regional (ta, te, mr, gu, bn, kn, ml, or, pa)
- `keyboard_language`: Contains regional language
- `state`: Regional states (TN, AP, TS, KA, KL, WB, GJ, MH, OR, PB)
- `language_region`: Not "hindi"

**Output**:
- **UI Mode**: `standard`
- **Language**: `regional`
- **Confidence Threshold**: 5.0
- **Recommended Actions**:
  - Display interface in regional language
  - Show regional language prompt examples
  - Enable regional language voice input
  - Suggest culturally relevant prompts
  - Show regional keyboard hints

---

### 11. **Quick Task User**

**Description**: User wants quick, single-purpose tasks

**Key Signals**:
- `session_duration`: "short"
- `time_to_first_interaction`: "immediate"
- `text_input_length`: "short"
- `session_count`: 1
- `scroll_behavior`: "minimal"

**Output**:
- **UI Mode**: `lite`
- **Language**: `system_default`
- **Confidence Threshold**: 5.0
- **Recommended Actions**:
  - Show quick action buttons
  - Display one-tap common tasks
  - Suggest short, direct prompts
  - Minimize UI clutter
  - Show search-first interface

---

### 12. **Power User / Tech-Savvy**

**Description**: Tech-savvy user with high-end device and good network

**Key Signals**:
- `device_class`: "high_end"
- `network_type`: "wifi" or "4g"
- `network_speed`: "fast"
- `ram_size`: "4GB+", "6GB+", or "8GB+"
- `session_duration`: "long"
- `text_input_length`: "long"

**Output**:
- **UI Mode**: `standard`
- **Language**: `english`
- **Confidence Threshold**: 6.0
- **Recommended Actions**:
  - Show advanced features
  - Enable rich formatting options
  - Suggest complex, multi-step prompts
  - Display developer-friendly tools
  - Show API and integration options

---

### 13. **First-time AI Explorer** (Default Fallback)

**Description**: Default state when no rules match or insufficient signals

**Key Signals**: Minimal or no matching signals

**Output**:
- **UI Mode**: `standard`
- **Language**: `system_default`
- **Confidence**: 0.0 (low confidence)
- **Recommended Actions**:
  - Show welcome message
  - Display example prompts
  - Enable basic tutorial
  - Show language selection
  - Suggest getting started prompts

---

## 📈 Confidence Scores

- **Confidence Range**: 0.0 to 10.0
- **High Confidence**: 7.0+ (strong signal match)
- **Medium Confidence**: 4.0-6.9 (moderate signal match)
- **Low Confidence**: 0.0-3.9 (weak or default match)

---

## 🎨 UI Modes

1. **standard**: Full-featured UI with all capabilities
2. **lite**: Minimal UI optimized for low-end devices/slow networks
3. **voice-first**: Voice input prioritized, large voice button, voice examples

---

## 🌐 Language Preferences

1. **hindi**: Hindi interface and prompts
2. **english**: English interface
3. **regional**: Regional language (Tamil, Telugu, Bengali, etc.)
4. **mixed**: Mix of languages
5. **system_default**: Use system language setting

---

## 🔄 Signal-to-State Mapping Examples

### Example 1: Business User
```
Signals:
- business_apps: ["khatabook"]
- whatsapp_business_usage: "yes"
- payment_apps_installed: ["paytm"]
- time_of_day: "evening"
- hour_of_day: 19

→ Output: "Evening Ledger / Khatabook Mode User"
```

### Example 2: Student
```
Signals:
- education_apps: ["byjus"]
- session_duration: "long"
- text_input_length: "long"
- time_of_day: "afternoon"

→ Output: "Student Exam Time User"
```

### Example 3: Low-end Device User
```
Signals:
- device_class: "low_end"
- network_type: "3g"
- network_speed: "slow"
- ram_size: "2GB"

→ Output: "Low-network Slow Device User"
```

---

## 📝 Notes

- Multiple rules can match; the highest scoring rule wins
- Confidence adjustments from web intelligence and LLM reasoning can boost scores
- If no rule meets threshold, default rule is used
- All outputs include detailed explanations of the inference process

