# Implicit Signals Taxonomy for Bharat Context-Adaptive Engine

This document enumerates all implicit signals that can be collected on Day-0 without requiring explicit user input. These signals help infer user context and needs for Tier-2/3/4 Indian users.

---

## 1. Device Signals

### 1.1 Hardware Characteristics
- **Device Class**: `low_end`, `mid_range`, `high_end` (based on RAM, CPU cores, storage)
- **RAM Size**: `1GB`, `2GB`, `3GB`, `4GB+`
- **Storage Available**: `low` (< 2GB), `medium` (2-10GB), `high` (> 10GB)
- **Screen Size**: `small` (< 5"), `medium` (5-6"), `large` (> 6")
- **Screen Resolution**: `hd`, `fhd`, `qhd`, `4k`
- **Battery Level**: `critical` (< 20%), `low` (20-50%), `medium` (50-80%), `high` (> 80%)
- **Battery Health**: `poor`, `good`, `excellent`
- **Device Age**: `new` (< 6 months), `medium` (6-24 months), `old` (> 24 months)
- **Manufacturer**: `samsung`, `xiaomi`, `realme`, `oppo`, `vivo`, `oneplus`, `other`
- **OS Version**: Android/iOS version number
- **Device Model**: Specific model identifier

### 1.2 Performance Indicators
- **App Launch Time**: `fast` (< 2s), `medium` (2-5s), `slow` (> 5s)
- **Frame Rate**: `smooth` (> 55fps), `medium` (30-55fps), `laggy` (< 30fps)
- **Memory Pressure**: `low`, `medium`, `high`
- **CPU Usage**: `low`, `medium`, `high`
- **Thermal State**: `cool`, `warm`, `hot`

---

## 2. Network Signals

### 2.1 Connection Characteristics
- **Network Type**: `wifi`, `4g`, `3g`, `2g`, `offline`
- **Network Speed**: `fast` (> 5 Mbps), `medium` (1-5 Mbps), `slow` (< 1 Mbps)
- **Latency**: `low` (< 100ms), `medium` (100-300ms), `high` (> 300ms)
- **Connection Stability**: `stable`, `unstable`, `intermittent`
- **Data Saver Mode**: `enabled`, `disabled`
- **Roaming Status**: `home`, `roaming`
- **Carrier**: `jio`, `airtel`, `vi`, `bsnl`, `other`
- **Network Quality Score**: `excellent`, `good`, `poor`, `very_poor`

### 2.2 Usage Patterns
- **Peak Hours Usage**: `yes`, `no` (based on network congestion)
- **Offline Duration**: Time since last successful connection
- **Retry Count**: Number of failed requests before success

---

## 3. Locale & Geographic Signals

### 3.1 Location Context
- **State**: Indian state code (e.g., `UP`, `MH`, `WB`, `TN`, `GJ`)
- **District**: District name (if available)
- **City Tier**: `tier1` (metro), `tier2`, `tier3`, `tier4`, `rural`
- **Timezone**: IST offset
- **Language Region**: Dominant language in region (e.g., `hindi`, `tamil`, `bengali`, `gujarati`, `marathi`)
- **Urban/Rural**: `urban`, `rural`, `semi_urban`

### 3.2 Cultural Context
- **Festival Day**: `diwali`, `holi`, `eid`, `dussehra`, `pongal`, `none`
- **Regional Holiday**: `yes`, `no`
- **Weekend**: `yes`, `no`
- **Time of Day**: `early_morning` (5-8 AM), `morning` (8-12 PM), `afternoon` (12-5 PM), `evening` (5-9 PM), `night` (9 PM-12 AM), `late_night` (12-5 AM)

---

## 4. Temporal Signals

### 4.1 Time-Based Patterns
- **Hour of Day**: 0-23
- **Day of Week**: `monday`, `tuesday`, `wednesday`, `thursday`, `friday`, `saturday`, `sunday`
- **Day of Month**: 1-31
- **Month**: 1-12
- **Season**: `summer`, `monsoon`, `winter`
- **First Launch Time**: Time of first app open
- **Session Duration**: `short` (< 2 min), `medium` (2-10 min), `long` (> 10 min)
- **Time Since Install**: `immediate` (< 1 hour), `same_day`, `next_day`, `later`

### 4.2 Activity Timing
- **Morning Routine**: `yes`, `no` (5-9 AM usage)
- **Evening Routine**: `yes`, `no` (6-10 PM usage)
- **Night Owl**: `yes`, `no` (10 PM-2 AM usage)
- **Work Hours**: `yes`, `no` (9 AM-6 PM on weekdays)

---

## 5. App Usage Signals

### 5.1 Installation Context
- **Installation Source**: `play_store`, `apk`, `referral`, `ad_campaign`
- **Referral Code**: If present, indicates user segment
- **Campaign Tag**: Marketing campaign identifier
- **App Version**: First installed version
- **Installation Day**: Day of week when installed

### 5.2 Interaction Patterns
- **First Action**: `none`, `tap_icon`, `swipe`, `voice`, `search`
- **Time to First Interaction**: `immediate` (< 5s), `quick` (5-30s), `delayed` (> 30s)
- **Screen Views**: Which screens were viewed first
- **Scroll Behavior**: `none`, `minimal`, `extensive`
- **Tap Patterns**: `sparse`, `moderate`, `frequent`
- **Back Button Usage**: `frequent`, `rare`, `none`
- **App Minimization**: `frequent`, `rare`, `none`
- **Session Count**: Number of sessions in first day

### 5.3 Feature Discovery
- **Keyboard Opened**: `yes`, `no`
- **Voice Button Tapped**: `yes`, `no`
- **Settings Accessed**: `yes`, `no`
- **Help/FAQ Opened**: `yes`, `no`
- **Example Prompts Viewed**: `yes`, `no`
- **Tutorial Started**: `yes`, `no`
- **Tutorial Completed**: `yes`, `no`

---

## 6. System & Environment Signals

### 6.1 System Settings
- **System Language**: Primary system language (e.g., `hi`, `en`, `ta`, `te`, `mr`, `gu`, `bn`)
- **Keyboard Language**: Active keyboard language
- **Font Size**: `small`, `medium`, `large`, `extra_large`
- **Dark Mode**: `enabled`, `disabled`
- **Accessibility Features**: `enabled`, `disabled`
- **Developer Options**: `enabled`, `disabled`
- **Root Status**: `rooted`, `not_rooted`

### 6.2 App Permissions
- **Location Permission**: `granted`, `denied`, `not_asked`
- **Microphone Permission**: `granted`, `denied`, `not_asked`
- **Storage Permission**: `granted`, `denied`, `not_asked`
- **Notification Permission**: `granted`, `denied`, `not_asked`

---

## 7. Installed Apps & App Ecosystem Signals

### 7.1 App Categories Present
- **Total Apps Installed**: Count (bucketed: `few` < 20, `medium` 20-50, `many` > 50)
- **Communication Apps**: `whatsapp`, `telegram`, `signal`, `messenger`, `none`, `multiple`
- **Social Media Apps**: `facebook`, `instagram`, `twitter`, `linkedin`, `none`, `multiple`
- **Video Apps**: `youtube`, `tiktok`, `instagram_reels`, `jio_cinema`, `none`, `multiple`
- **Music Apps**: `spotify`, `wynk`, `gaana`, `jio_saavn`, `none`, `multiple`
- **News Apps**: `news18`, `aaj_tak`, `times_of_india`, `none`, `multiple`
- **Gaming Apps**: `yes`, `no`, `many` (> 5 games)
- **Productivity Apps**: `wps_office`, `adobe_reader`, `none`, `multiple`
- **Education Apps**: `byjus`, `unacademy`, `vedantu`, `none`, `multiple`
- **Health & Fitness Apps**: `yes`, `no`
- **Food Delivery Apps**: `zomato`, `swiggy`, `none`, `multiple`
- **Travel Apps**: `ola`, `uber`, `irctc`, `none`, `multiple`
- **Entertainment Apps**: `hotstar`, `netflix`, `prime_video`, `none`, `multiple`

### 7.2 Payment & Financial Apps
- **Payment Apps Installed**: `paytm`, `phonepe`, `gpay`, `bhim`, `none`, `multiple`
- **Banking Apps**: `sbi`, `hdfc`, `icici`, `axis`, `none`, `multiple`
- **UPI Apps**: `yes`, `no`, `multiple`
- **Investment Apps**: `zerodha`, `groww`, `upstox`, `none`, `multiple`
- **Lending Apps**: `yes`, `no` (presence of loan/credit apps)
- **Financial App Count**: `none`, `few` (1-2), `many` (3+)

### 7.3 E-commerce & Shopping Apps
- **E-commerce Apps**: `flipkart`, `amazon`, `meesho`, `myntra`, `snapdeal`, `none`, `multiple`
- **Grocery Apps**: `bigbasket`, `grofers`, `jiomart`, `none`, `multiple`
- **Fashion Apps**: `myntra`, `ajio`, `nykaa`, `none`, `multiple`
- **Shopping App Count**: `none`, `few` (1-2), `many` (3+)

### 7.4 Business & Work Apps
- **Business Apps**: `khatabook`, `okcredit`, `bharatpe`, `none`, `multiple`
- **Accounting Apps**: `yes`, `no`
- **CRM/Lead Apps**: `yes`, `no`
- **Work Communication**: `slack`, `teams`, `zoom`, `none`, `multiple`
- **Email Apps**: `gmail`, `outlook`, `yahoo`, `none`, `multiple`

### 7.5 Regional & Local Apps
- **Regional News Apps**: `yes`, `no` (state/regional language news apps)
- **Regional Entertainment**: `yes`, `no` (regional OTT/content apps)
- **Government Apps**: `aadhaar`, `digilocker`, `umang`, `none`, `multiple`
- **Local Services**: `yes`, `no` (hyperlocal service apps)

### 7.6 App Usage Patterns (Aggregated)
- **Most Used App Category**: `communication`, `social`, `entertainment`, `shopping`, `finance`, `other`
- **App Diversity Score**: `low` (few categories), `medium`, `high` (many categories)
- **Premium App Presence**: `yes`, `no` (presence of paid/premium apps)
- **App Update Frequency**: `frequent`, `occasional`, `rare` (inferred from app versions)
- **App Installation Recency**: `recent` (many new apps), `stable` (few new apps), `old` (no new apps)

---

## 8. SMS & Text Message Signals

### 8.1 SMS Patterns (Metadata Only - No Content)
- **SMS Permission**: `granted`, `denied`, `not_asked`
- **SMS Volume**: `low` (< 10/day), `medium` (10-50/day), `high` (> 50/day)
- **SMS Frequency Pattern**: `sparse`, `regular`, `frequent`
- **SMS Time Distribution**: `morning_heavy`, `afternoon_heavy`, `evening_heavy`, `uniform`
- **SMS Sender Types**: `personal`, `business`, `otp`, `promotional`, `mixed`
- **OTP Message Frequency**: `low`, `medium`, `high` (count only, no content)
- **Promotional SMS Volume**: `low`, `medium`, `high` (count only)
- **Banking SMS Presence**: `yes`, `no` (detected from sender patterns, not content)
- **E-commerce SMS Presence**: `yes`, `no` (detected from sender patterns)
- **Government SMS Presence**: `yes`, `no` (Aadhaar, government services)

### 8.2 SMS Language Patterns
- **SMS Language Mix**: `hindi_only`, `english_only`, `regional_only`, `mixed`, `unknown`
- **SMS Script Detection**: `devanagari`, `latin`, `tamil`, `telugu`, `bengali`, `mixed`, `unknown`
- **SMS Length Pattern**: `short` (avg < 50 chars), `medium` (50-100), `long` (> 100)
- **SMS Emoji Usage**: `frequent`, `occasional`, `rare`, `none`

### 8.3 SMS Context Signals
- **Business Hours SMS**: `yes`, `no` (SMS activity during 9 AM-6 PM)
- **Weekend SMS Pattern**: `similar`, `different` (compared to weekday)
- **SMS Response Time**: `immediate` (< 5 min), `quick` (5-30 min), `delayed` (> 30 min)
- **SMS Thread Activity**: `active` (many conversations), `moderate`, `low`

---

## 9. WhatsApp & Messaging App Signals

### 9.1 WhatsApp Presence & Usage
- **WhatsApp Installed**: `yes`, `no`
- **WhatsApp Active**: `yes`, `no` (recent activity detected)
- **WhatsApp Notification Permission**: `granted`, `denied`, `not_asked`
- **WhatsApp Notification Frequency**: `low` (< 10/day), `medium` (10-50/day), `high` (> 50/day)
- **WhatsApp Notification Pattern**: `sparse`, `regular`, `frequent`, `bursty`
- **WhatsApp Notification Time Distribution**: `morning_heavy`, `afternoon_heavy`, `evening_heavy`, `night_heavy`, `uniform`
- **WhatsApp Group Activity**: `high` (many group notifications), `medium`, `low`, `none`
- **WhatsApp Business Usage**: `yes`, `no` (detected from notification patterns)

### 9.2 WhatsApp Notification Metadata (No Content)
- **Notification Sender Types**: `personal`, `business`, `group`, `broadcast`, `mixed`
- **Notification Urgency Pattern**: `high` (many immediate notifications), `medium`, `low`
- **Notification Response Pattern**: `immediate` (quick opens), `delayed`, `ignored`
- **WhatsApp Call Frequency**: `frequent`, `occasional`, `rare`, `none` (from notification patterns)
- **WhatsApp Video Call Frequency**: `frequent`, `occasional`, `rare`, `none`
- **WhatsApp Status Updates**: `frequent`, `occasional`, `rare`, `none`

### 9.3 Other Messaging Apps
- **Telegram Installed**: `yes`, `no`
- **Telegram Active**: `yes`, `no`
- **Signal Installed**: `yes`, `no`
- **Facebook Messenger Installed**: `yes`, `no`
- **Messaging App Count**: `single` (1 app), `multiple` (2+ apps)
- **Primary Messaging App**: `whatsapp`, `telegram`, `signal`, `messenger`, `sms`, `unknown`

---

## 10. Notification Patterns (All Apps)

### 10.1 Overall Notification Behavior
- **Total Notification Volume**: `low` (< 20/day), `medium` (20-100/day), `high` (> 100/day)
- **Notification Permission Status**: `granted`, `denied`, `partial`
- **Notification Dismissal Rate**: `high` (many dismissed), `medium`, `low`
- **Notification Response Rate**: `high` (many opened), `medium`, `low`
- **Do Not Disturb Usage**: `frequent`, `occasional`, `rare`, `never`
- **Notification Sound Enabled**: `yes`, `no`
- **Notification Vibration Enabled**: `yes`, `no`

### 10.2 Notification Categories
- **Social Notifications**: `high`, `medium`, `low`, `none`
- **Communication Notifications**: `high`, `medium`, `low`, `none`
- **E-commerce Notifications**: `high`, `medium`, `low`, `none`
- **Banking/Finance Notifications**: `high`, `medium`, `low`, `none`
- **News Notifications**: `high`, `medium`, `low`, `none`
- **Entertainment Notifications**: `high`, `medium`, `low`, `none`
- **Gaming Notifications**: `high`, `medium`, `low`, `none`
- **Productivity Notifications**: `high`, `medium`, `low`, `none`

### 10.3 Notification Timing Patterns
- **Peak Notification Hours**: `morning` (6-10 AM), `afternoon` (12-4 PM), `evening` (6-10 PM), `night` (10 PM-12 AM)
- **Weekend vs Weekday Pattern**: `similar`, `different`
- **Notification Burst Pattern**: `frequent_bursts`, `occasional_bursts`, `steady`, `sparse`
- **Silent Hours**: `yes`, `no` (periods with no notifications)

### 10.4 Notification Engagement
- **Immediate Open Rate**: `high` (> 50%), `medium` (20-50%), `low` (< 20%)
- **Delayed Open Rate**: `high`, `medium`, `low`
- **Notification-to-App Launch**: `frequent`, `occasional`, `rare`
- **Notification Ignore Rate**: `high`, `medium`, `low`

---

## 11. Commerce & Intent Signals

### 11.1 Economic Indicators
- **Device Price Tier**: Inferred from device model
- **App Store Category**: Other apps installed (if detectable)
- **Payment Apps Installed**: `paytm`, `phonepe`, `gpay`, `none`, `multiple`
- **E-commerce Apps**: `flipkart`, `amazon`, `meesho`, `none`, `multiple`
- **Banking Apps**: `yes`, `no`
- **UPI Apps**: `yes`, `no`
- **Financial Sophistication Score**: `low`, `medium`, `high` (based on financial apps)

### 11.2 Work Patterns
- **Business Hours Activity**: `yes`, `no`
- **Weekend Activity**: `yes`, `no`
- **Multiple Device Usage**: `yes`, `no` (if detectable)
- **Work App Presence**: `yes`, `no` (business/productivity apps)
- **Business Communication Pattern**: `high`, `medium`, `low` (from messaging patterns)

---

## 12. Cultural & Social Signals

### 12.1 Language Preferences
- **System Language**: Primary language code
- **Keyboard Languages**: List of installed keyboards
- **Input Method**: `qwerty`, `phonetic`, `gesture`, `voice`
- **Language Switching Frequency**: `none`, `low`, `high`
- **App Language Mix**: `hindi_dominant`, `english_dominant`, `regional_dominant`, `mixed`
- **Messaging Language**: `hindi`, `english`, `regional`, `mixed` (from SMS/WhatsApp patterns)

### 12.2 Social Context
- **Contact Sync**: `enabled`, `disabled`
- **Calendar Access**: `granted`, `denied`
- **Social Media Apps**: Presence of WhatsApp, Facebook, Instagram, etc.
- **Social Engagement Level**: `high` (many social apps, frequent notifications), `medium`, `low`
- **Family Communication Pattern**: `high`, `medium`, `low` (inferred from messaging patterns)
- **Professional Network**: `yes`, `no` (LinkedIn, professional messaging)

---

## 13. Behavioral Heuristics

### 9.1 Engagement Patterns
- **Return User**: `yes`, `no` (within first 24 hours)
- **Session Frequency**: `single`, `multiple`
- **Time Between Sessions**: `short` (< 1 hour), `medium` (1-6 hours), `long` (> 6 hours)
- **Abandonment Indicators**: `quick_exit` (< 10s), `no_interaction`, `error_encountered`

### 9.2 Intent Signals
- **Search Query Patterns**: If any search was performed
- **Voice Usage**: `attempted`, `successful`, `not_attempted`
- **Text Input Length**: `none`, `short` (< 10 chars), `medium` (10-50 chars), `long` (> 50 chars)
- **Copy-Paste Behavior**: `yes`, `no`

---

## 14. Accessibility & Usability Signals

### 10.1 Accessibility Needs
- **Screen Reader**: `enabled`, `disabled`
- **High Contrast**: `enabled`, `disabled`
- **Large Text**: `enabled`, `disabled`
- **Touch Sensitivity**: `normal`, `high`

### 10.2 Usability Indicators
- **Error Rate**: `low`, `medium`, `high`
- **Crash Frequency**: `none`, `low`, `high`
- **Loading Timeouts**: `none`, `few`, `many`
- **User Frustration Indicators**: Multiple back presses, rapid taps, app closure

---

## 15. Contextual Metadata

### 11.1 App State
- **Installation Method**: `organic`, `paid`, `referral`
- **First Launch Context**: `cold_start`, `warm_start`
- **Background Apps**: Number of apps running
- **Memory Available**: `low`, `medium`, `high`

### 11.2 User Journey Stage
- **Onboarding Completion**: `not_started`, `in_progress`, `completed`, `skipped`
- **First Prompt Attempted**: `yes`, `no`
- **First Response Received**: `yes`, `no`
- **First Successful Interaction**: `yes`, `no`

---

## 16. Aggregated Composite Signals

### 12.1 Derived Metrics
- **Device Performance Score**: Composite of RAM, CPU, storage, age
- **Network Reliability Score**: Composite of speed, latency, stability
- **User Sophistication Score**: Based on device, apps, interaction patterns
- **Engagement Likelihood**: Based on session patterns, return behavior
- **Language Comfort Score**: Based on system language, keyboard, input patterns
- **Economic Tier Estimate**: Based on device, apps, location

### 12.2 Risk Indicators
- **Churn Risk**: `low`, `medium`, `high`
- **Adoption Risk**: `low`, `medium`, `high`
- **Performance Risk**: `low`, `medium`, `high`
- **Network Risk**: `low`, `medium`, `high`

---

## Signal Collection Principles

1. **Privacy-First**: All signals are coarse-grained and non-identifying
2. **Opt-Out Friendly**: No PII collection
3. **Battery Efficient**: Minimal background processing
4. **Network Efficient**: Batch collection, offline-first
5. **Extensible**: Easy to add new signal categories
6. **Debuggable**: All signals timestamped and versioned

---

## Signal Priority Levels

- **P0 (Critical)**: Device class, network type, system language, time of day, first interaction, WhatsApp presence
- **P1 (Important)**: Location tier, battery level, session duration, app permissions, installed app categories, SMS patterns
- **P2 (Useful)**: Device age, network speed, keyboard language, accessibility features, notification patterns, messaging app usage
- **P3 (Optional)**: Detailed performance metrics, advanced behavioral patterns, specific app names, notification content analysis

---

## Privacy & Collection Notes

### Critical Privacy Principles
- **NO CONTENT COLLECTION**: Never collect SMS content, WhatsApp message content, or notification content
- **METADATA ONLY**: Only collect patterns, frequencies, timing, and aggregated statistics
- **ANONYMIZED APP DETECTION**: Use app package name hashing or category detection, not direct app names
- **COARSE-GRAINED SIGNALS**: All signals are aggregated and non-identifying
- **OPT-IN REQUIRED**: SMS and notification access require explicit user permission

### Collection Guidelines
- Signals marked as "if available" should be collected only when accessible without special permissions
- All signals should have default/unknown values for graceful degradation
- Signal collection should be non-blocking and not impact app performance
- Signals should be versioned to support schema evolution
- SMS/Notification signals require explicit user consent and should be clearly explained

### Permissions Required
- **SMS Read Permission**: Required for SMS pattern detection (metadata only)
- **Notification Access**: Required for notification pattern analysis (Android Notification Listener)
- **App List Permission**: Required for installed app detection (coarse-grained categories only)
- **Usage Stats Permission**: Optional, for app usage patterns (Android UsageStats)

### Data Minimization
- Store only aggregated patterns, not raw data
- Use bucketing and categorization instead of exact counts
- Hash or anonymize any identifiers
- Implement data retention policies
- Allow users to opt-out of specific signal collection

