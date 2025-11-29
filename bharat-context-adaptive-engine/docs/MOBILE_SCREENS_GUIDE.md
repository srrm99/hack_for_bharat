# Mobile App Screens - Small Vendor Persona

## 📱 Overview

This document describes the mobile app screens created based on the inference engine recommendations for the **Small Vendor Persona**. The screens are designed to resemble ChatGPT's mobile interface while incorporating personalized content and actions.

---

## 🎯 Design Philosophy

- **ChatGPT-style UI**: Dark theme, modern design, familiar interface
- **Hindi-first**: All content in Hindi for Tier-2/3 India users
- **Business-focused**: Accounting, GST, invoice generation prompts
- **Personalized**: Based on inference engine recommendations
- **Engagement-driven**: Clear CTAs and interactive elements

---

## 📅 Screen Breakdown

### Day-0: Home Page (`day0_home.html`)

**Purpose**: First impression and immediate personalization

**Key Features**:
- **Hero Section**: Large, prominent prompt in Hindi
  - "मेरी दुकान का हिसाब-किताब करने में मदद करो"
  - Tap to start conversation
  
- **Quick Actions Grid**: 4 business-focused actions
  - 🧮 GST Calculation
  - 📄 Invoice Generator
  - 🔢 Number to Words
  - 💰 Profit Calculator

- **Example Prompts**: 3 suggested prompts in Hindi
  - "₹5000 का 18% GST कितना होगा?"
  - "Invoice बनाने में मदद करो"
  - "₹12500 को शब्दों में लिखो"

- **Feature Highlights**: Badges showing key features
  - Hindi Interface
  - Business Calculations
  - GST Helper

- **Chat Input**: Bottom input bar matching ChatGPT style

**Design Elements**:
- Dark gradient background (#343541 to #1a1b26)
- Green accent color (#10b981) for CTAs
- Rounded corners and modern card design
- Smooth hover effects

---

### Day-1: Notifications (`day1_notifications.html`)

**Purpose**: Re-engagement through notifications and reminders

**Key Features**:

#### Push Notifications
- **Title**: "आज का हिसाब-किताब करें"
- **Body**: "ChatGPT से GST calculation और invoice बनाने में मदद लें"
- **Time**: 18:00
- **Actions**: Open App, Dismiss

#### Reminders
- **Type**: Daily Accounting Reminder
- **Message**: "शाम को हिसाब-किताब करने का समय"
- **Time**: 19:00
- **Actions**: Set Reminder, Skip

#### Daily Summaries
- **Title**: "आज का Business Tip"
- **Content**: "GST filing के लिए ChatGPT से मदद लें"
- **Time**: 20:00
- **Actions**: Learn More, View Tips

**Design Elements**:
- Color-coded cards (green for notifications, blue for reminders, purple for summaries)
- Icon-based visual hierarchy
- Action buttons for quick engagement
- Time stamps for context

---

### Day-7: Weekly Insights (`day7_insights.html`)

**Purpose**: Retention through insights and feature discovery

**Key Features**:

#### Weekly Insights Card
- **Title**: "इस हफ्ते आपने क्या सीखा"
- **Content**: Summary of learnings
  - Hindi interface usage
  - Business calculations
  - GST helpers
  - Invoice generation

#### Usage Statistics
- **Days Active**: 7 days
- **Prompts Used**: 24 prompts
- Visual grid layout

#### Feature Suggestions
- **Advanced GST Calculator**: Complex GST scenarios
- **Monthly Report Generator**: Auto-generate reports
- **Customer Communication Templates**: Pre-written messages
- **Inventory Management Helper**: Track inventory with AI

**Design Elements**:
- Gradient header for visual appeal
- Large icon-based cards
- Statistics grid for quick insights
- Feature cards with hover effects
- Arrow indicators for discoverability

---

## 🎨 Design System

### Colors
- **Background**: Dark theme (#1a1b26, #343541)
- **Primary Accent**: Green (#10b981) - for CTAs and highlights
- **Secondary**: Blue (#3b82f6) - for reminders
- **Tertiary**: Purple (#a855f7) - for summaries
- **Text**: Light gray (#ececf1) for primary, #8e8ea0 for secondary

### Typography
- **Font**: System fonts (-apple-system, BlinkMacSystemFont, Segoe UI)
- **Hindi Font**: Noto Sans Devanagari, Mangal, Arial Unicode MS
- **Sizes**: 
  - Headers: 24px
  - Body: 15-16px
  - Secondary: 12-14px

### Components
- **Cards**: Rounded corners (12-16px), subtle borders, hover effects
- **Buttons**: Rounded (8-24px), colored backgrounds, clear CTAs
- **Icons**: Emoji-based for universal recognition
- **Spacing**: Consistent 12px, 16px, 20px grid

---

## 📂 File Structure

```
examples/mobile_screens/
├── index.html              # Main navigation page
├── day0_home.html         # Day-0 home screen
├── day1_notifications.html # Day-1 notifications
└── day7_insights.html      # Day-7 weekly insights
```

---

## 🚀 How to View

### Option 1: Direct HTML Files
1. Open `examples/mobile_screens/index.html` in a browser
2. Click "View Full Screen" on any screen
3. Or open individual HTML files directly

### Option 2: Local Server
```bash
# Navigate to examples/mobile_screens
cd examples/mobile_screens

# Start a simple HTTP server
python -m http.server 8001

# Open in browser
# http://localhost:8001
```

### Option 3: Mobile Preview
- Use browser developer tools (F12)
- Enable device emulation
- Select iPhone or Android device
- View screens in mobile viewport

---

## 🔄 Integration with ChatGPT App

### Implementation Steps

1. **Extract Recommendations**
   ```json
   POST /v1/recommendations/all-days
   {
     "signals": { ... }
   }
   ```

2. **Render Day-0 Home Page**
   - Use `day_0.content.hero_section.prompt` for hero
   - Use `day_0.content.quick_actions` for action cards
   - Use `day_0.content.example_prompts` for suggestions

3. **Schedule Day-1 Notifications**
   - Use `day_1.content.push_notifications` for push notifications
   - Use `day_1.content.reminders` for reminders
   - Use `day_1.content.daily_summaries` for summaries

4. **Show Day-7 Insights**
   - Use `day_7.content.weekly_insights` for insights
   - Use `day_7.content.feature_suggestions` for features

---

## 📊 Screen Flow

```
App Launch (Day-0)
    ↓
Home Page (Personalized)
    ↓
User Interaction
    ↓
Day-1 Notifications (Re-engagement)
    ↓
Day-7 Insights (Retention)
    ↓
Ongoing Personalization
```

---

## ✅ Key Features Implemented

- ✅ ChatGPT-style dark theme
- ✅ Hindi-first interface
- ✅ Business-focused content
- ✅ Personalized recommendations
- ✅ Interactive elements
- ✅ Responsive design
- ✅ Clear visual hierarchy
- ✅ Engagement CTAs

---

## 🎯 Expected User Experience

### Day-0
- User opens app → Sees personalized Hindi interface
- Immediate relevance → Business prompts visible
- Quick actions → One-tap access to common tasks
- **Result**: User understands app value immediately

### Day-1
- Push notification → Reminds user to engage
- Reminder → Sets daily accounting habit
- Daily summary → Provides value and tips
- **Result**: User re-engages with app

### Day-7
- Weekly insights → Shows progress and value
- Feature suggestions → Encourages exploration
- Statistics → Gamification and motivation
- **Result**: User continues using app long-term

---

## 🔧 Customization

### For Different Personas

1. **Student Persona**:
   - Change hero prompt to study-related
   - Update quick actions to exam prep, homework help
   - Modify example prompts to academic queries

2. **Professional Persona**:
   - Change to work-related prompts
   - Update actions to productivity tools
   - Modify examples to professional queries

3. **Regional Language**:
   - Change Hindi to Tamil, Telugu, Bengali, etc.
   - Update fonts for regional scripts
   - Maintain same structure and design

---

## 📝 Notes

- All screens are responsive and work on mobile devices
- Hindi text uses proper Unicode fonts
- Design matches ChatGPT's aesthetic
- Content is dynamically generated from inference engine
- Screens can be integrated into actual ChatGPT mobile app

---

**These screens demonstrate how the inference engine recommendations translate into a personalized, engaging mobile experience for small vendors in Tier-2/3 India.**

