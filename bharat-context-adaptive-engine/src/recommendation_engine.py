"""
Recommendation Engine for Bharat Context-Adaptive Engine
Generates personalized content, delivery medium, and timing recommendations
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from .models import InferenceOutput, UIMode, LanguagePreference


class RecommendationEngine:
    """Generates personalized content recommendations based on inference output"""
    
    # Content templates by user need state
    CONTENT_TEMPLATES = {
        "Hindi-first User": {
            "day_0": {
                "home_page": {
                    "hero_prompt": "मेरी दुकान का हिसाब-किताब करने में मदद करो",
                    "quick_actions": [
                        "GST Calculation",
                        "Invoice Generator",
                        "Number to Words",
                        "Profit Calculator"
                    ],
                    "example_prompts": [
                        "₹5000 का 18% GST कितना होगा?",
                        "Invoice बनाने में मदद करो",
                        "₹12500 को शब्दों में लिखो"
                    ],
                    "feature_highlights": [
                        "Hindi Interface",
                        "Business Calculations",
                        "GST Helper"
                    ]
                }
            },
            "day_1": {
                "push_notifications": [
                    {
                        "title": "आज का हिसाब-किताब करें",
                        "body": "ChatGPT से GST calculation और invoice बनाने में मदद लें",
                        "time": "18:00",
                        "priority": "high"
                    }
                ],
                "reminders": [
                    {
                        "type": "daily_accounting",
                        "message": "शाम को हिसाब-किताब करने का समय",
                        "time": "19:00"
                    }
                ],
                "daily_summaries": [
                    {
                        "type": "business_tips",
                        "title": "आज का Business Tip",
                        "content": "GST filing के लिए ChatGPT से मदद लें"
                    }
                ]
            },
            "day_7": {
                "weekly_insights": [
                    {
                        "type": "usage_summary",
                        "title": "इस हफ्ते आपने क्या सीखा",
                        "content": "Hindi interface, Business calculations, GST helpers"
                    }
                ],
                "feature_suggestions": [
                    "Advanced GST Calculator",
                    "Monthly Report Generator",
                    "Customer Communication Templates"
                ]
            }
        },
        "Evening Ledger / Khatabook Mode User": {
            "day_0": {
                "home_page": {
                    "hero_prompt": "मेरी दुकान का हिसाब-किताब करने में मदद करो",
                    "quick_actions": [
                        "GST Calculation",
                        "Invoice Generator",
                        "Number to Words",
                        "Profit Calculator"
                    ],
                    "example_prompts": [
                        "₹5000 का 18% GST कितना होगा?",
                        "Invoice बनाने में मदद करो",
                        "₹12500 को शब्दों में लिखो"
                    ],
                    "feature_highlights": [
                        "Quick Calculations",
                        "Invoice Templates",
                        "GST Helper"
                    ]
                }
            },
            "day_1": {
                "push_notifications": [
                    {
                        "title": "आज का हिसाब-किताब करें",
                        "body": "ChatGPT से GST calculation और invoice बनाने में मदद लें",
                        "time": "18:00",
                        "priority": "high"
                    }
                ],
                "reminders": [
                    {
                        "type": "daily_accounting",
                        "message": "शाम को हिसाब-किताब करने का समय",
                        "time": "19:00"
                    }
                ],
                "daily_summaries": [
                    {
                        "type": "business_tips",
                        "title": "आज का Business Tip",
                        "content": "GST filing के लिए ChatGPT से मदद लें"
                    }
                ]
            },
            "day_7": {
                "weekly_insights": [
                    {
                        "type": "usage_summary",
                        "title": "इस हफ्ते आपने क्या सीखा",
                        "content": "Accounting prompts, GST calculations, Invoice generation"
                    }
                ],
                "feature_suggestions": [
                    "Advanced GST Calculator",
                    "Monthly Report Generator",
                    "Customer Communication Templates"
                ]
            }
        },
        "Shop Owner / Kirana Workflow User": {
            "day_0": {
                "home_page": {
                    "hero_prompt": "मेरी दुकान के लिए मदद चाहिए",
                    "quick_actions": [
                        "Price Comparison",
                        "Inventory Helper",
                        "Customer Messages",
                        "Business Calculations"
                    ],
                    "example_prompts": [
                        "Customer को WhatsApp message कैसे भेजूं?",
                        "Inventory management tips दो",
                        "Profit margin कैसे calculate करें?"
                    ]
                }
            },
            "day_1": {
                "push_notifications": [
                    {
                        "title": "Business Tips",
                        "body": "आज के लिए useful business prompts देखें",
                        "time": "10:00",
                        "priority": "medium"
                    }
                ]
            },
            "day_7": {
                "weekly_insights": [
                    {
                        "type": "business_growth",
                        "title": "Business Growth Tips",
                        "content": "Customer engagement और inventory management के लिए ChatGPT का उपयोग करें"
                    }
                ]
            }
        }
    }
    
    def generate_recommendations(
        self,
        inference_output: InferenceOutput,
        day: int = 0,
        available_content: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Generate personalized recommendations based on inference output
        
        Args:
            inference_output: Output from inference engine
            day: Day number (0 = Day-0, 1 = Day-1, 7 = Day-7)
            available_content: List of content that app can show
            
        Returns:
            Dictionary with content, delivery medium, and timing recommendations
        """
        user_need_state = inference_output.user_need_state
        ui_mode = inference_output.ui_mode
        language_preference = inference_output.language_preference
        confidence = inference_output.confidence
        
        # Get content templates for this user need state
        templates = self.CONTENT_TEMPLATES.get(user_need_state, {})
        
        # Generate recommendations based on day
        if day == 0:
            return self._generate_day_0_recommendations(
                inference_output, templates, available_content
            )
        elif day == 1:
            return self._generate_day_1_recommendations(
                inference_output, templates, available_content
            )
        elif day == 7:
            return self._generate_day_7_recommendations(
                inference_output, templates, available_content
            )
        else:
            return self._generate_generic_recommendations(
                inference_output, templates, available_content
            )
    
    def _generate_day_0_recommendations(
        self,
        inference_output: InferenceOutput,
        templates: Dict[str, Any],
        available_content: Optional[List[str]]
    ) -> Dict[str, Any]:
        """Generate Day-0 recommendations (Home page adaptation)"""
        user_need_state = inference_output.user_need_state
        language_preference = inference_output.language_preference
        
        # Get template or create default
        day_0_template = templates.get("day_0", {})
        home_page = day_0_template.get("home_page", {})
        
        # Generate content
        content = {
            "hero_section": {
                "prompt": home_page.get("hero_prompt", self._get_default_prompt(user_need_state, language_preference)),
                "language": language_preference.value,
                "ui_mode": inference_output.ui_mode.value
            },
            "quick_actions": home_page.get("quick_actions", inference_output.recommended_actions[:4]),
            "example_prompts": home_page.get("example_prompts", inference_output.recommended_actions[:3]),
            "feature_highlights": home_page.get("feature_highlights", []),
            "personalization_level": "high" if inference_output.confidence >= 7.0 else "medium"
        }
        
        return {
            "outcome": "Day-0 Home Page Personalization",
            "content": content,
            "delivery_medium": "in_app_home_page",
            "timing": {
                "when": "immediate",
                "trigger": "app_launch",
                "priority": "high"
            },
            "expected_outcome": f"User sees personalized {user_need_state} interface on first launch",
            "confidence": inference_output.confidence
        }
    
    def _generate_day_1_recommendations(
        self,
        inference_output: InferenceOutput,
        templates: Dict[str, Any],
        available_content: Optional[List[str]]
    ) -> Dict[str, Any]:
        """Generate Day-1 recommendations (Push notifications, reminders, daily summaries)"""
        user_need_state = inference_output.user_need_state
        day_1_template = templates.get("day_1", {})
        
        # Push notifications
        push_notifications = day_1_template.get("push_notifications", [])
        if not push_notifications:
            push_notifications = self._generate_default_push_notifications(user_need_state)
        
        # Reminders
        reminders = day_1_template.get("reminders", [])
        if not reminders:
            reminders = self._generate_default_reminders(user_need_state)
        
        # Daily summaries
        daily_summaries = day_1_template.get("daily_summaries", [])
        if not daily_summaries:
            daily_summaries = self._generate_default_daily_summaries(user_need_state)
        
        return {
            "outcome": "Day-1 Engagement",
            "content": {
                "push_notifications": push_notifications,
                "reminders": reminders,
                "daily_summaries": daily_summaries
            },
            "delivery_medium": ["push_notification", "in_app_notification", "daily_digest"],
            "timing": {
                "when": "day_1",
                "schedule": {
                    "push_notifications": [{"time": "18:00", "timezone": "IST"}],
                    "reminders": [{"time": "19:00", "timezone": "IST"}],
                    "daily_summaries": [{"time": "20:00", "timezone": "IST"}]
                }
            },
            "expected_outcome": "User re-engages with app through notifications and reminders",
            "confidence": inference_output.confidence
        }
    
    def _generate_day_7_recommendations(
        self,
        inference_output: InferenceOutput,
        templates: Dict[str, Any],
        available_content: Optional[List[str]]
    ) -> Dict[str, Any]:
        """Generate Day-7 recommendations (Weekly insights, feature suggestions)"""
        user_need_state = inference_output.user_need_state
        day_7_template = templates.get("day_7", {})
        
        weekly_insights = day_7_template.get("weekly_insights", [])
        if not weekly_insights:
            weekly_insights = self._generate_default_weekly_insights(user_need_state)
        
        feature_suggestions = day_7_template.get("feature_suggestions", [])
        if not feature_suggestions:
            feature_suggestions = inference_output.recommended_actions
        
        return {
            "outcome": "Day-7 Retention & Growth",
            "content": {
                "weekly_insights": weekly_insights,
                "feature_suggestions": feature_suggestions,
                "advanced_features": self._get_advanced_features(user_need_state)
            },
            "delivery_medium": ["in_app_insights", "email_digest", "push_notification"],
            "timing": {
                "when": "day_7",
                "schedule": {
                    "weekly_insights": [{"time": "10:00", "day": "monday", "timezone": "IST"}]
                }
            },
            "expected_outcome": "User discovers advanced features and continues engagement",
            "confidence": inference_output.confidence
        }
    
    def _generate_generic_recommendations(
        self,
        inference_output: InferenceOutput,
        templates: Dict[str, Any],
        available_content: Optional[List[str]]
    ) -> Dict[str, Any]:
        """Generate generic recommendations for other days"""
        return {
            "outcome": "Ongoing Personalization",
            "content": {
                "recommended_actions": inference_output.recommended_actions,
                "ui_mode": inference_output.ui_mode.value,
                "language": inference_output.language_preference.value
            },
            "delivery_medium": "in_app",
            "timing": {"when": "ongoing"},
            "expected_outcome": "Continuous personalized experience",
            "confidence": inference_output.confidence
        }
    
    def _get_default_prompt(self, user_need_state: str, language_preference: LanguagePreference) -> str:
        """Get default prompt based on user need state and language"""
        prompts = {
            "Evening Ledger / Khatabook Mode User": {
                "hindi": "मेरी दुकान का हिसाब-किताब करने में मदद करो",
                "english": "Help me with my shop's accounting"
            },
            "Shop Owner / Kirana Workflow User": {
                "hindi": "मेरी दुकान के लिए मदद चाहिए",
                "english": "I need help for my shop"
            }
        }
        
        state_prompts = prompts.get(user_need_state, {})
        lang_key = language_preference.value if language_preference.value in ["hindi", "english"] else "hindi"
        return state_prompts.get(lang_key, "How can I help you?")
    
    def _generate_default_push_notifications(self, user_need_state: str) -> List[Dict[str, Any]]:
        """Generate default push notifications"""
        notifications = {
            "Evening Ledger / Khatabook Mode User": [
                {
                    "title": "आज का हिसाब-किताब करें",
                    "body": "ChatGPT से GST calculation और invoice बनाने में मदद लें",
                    "time": "18:00",
                    "priority": "high"
                }
            ]
        }
        return notifications.get(user_need_state, [])
    
    def _generate_default_reminders(self, user_need_state: str) -> List[Dict[str, Any]]:
        """Generate default reminders"""
        reminders = {
            "Evening Ledger / Khatabook Mode User": [
                {
                    "type": "daily_accounting",
                    "message": "शाम को हिसाब-किताब करने का समय",
                    "time": "19:00"
                }
            ]
        }
        return reminders.get(user_need_state, [])
    
    def _generate_default_daily_summaries(self, user_need_state: str) -> List[Dict[str, Any]]:
        """Generate default daily summaries"""
        summaries = {
            "Evening Ledger / Khatabook Mode User": [
                {
                    "type": "business_tips",
                    "title": "आज का Business Tip",
                    "content": "GST filing के लिए ChatGPT से मदद लें"
                }
            ]
        }
        return summaries.get(user_need_state, [])
    
    def _generate_default_weekly_insights(self, user_need_state: str) -> List[Dict[str, Any]]:
        """Generate default weekly insights"""
        insights = {
            "Evening Ledger / Khatabook Mode User": [
                {
                    "type": "usage_summary",
                    "title": "इस हफ्ते आपने क्या सीखा",
                    "content": "Accounting prompts, GST calculations, Invoice generation"
                }
            ]
        }
        return insights.get(user_need_state, [])
    
    def _get_advanced_features(self, user_need_state: str) -> List[str]:
        """Get advanced features for user need state"""
        features = {
            "Evening Ledger / Khatabook Mode User": [
                "Advanced GST Calculator",
                "Monthly Report Generator",
                "Customer Communication Templates",
                "Inventory Management Helper"
            ]
        }
        return features.get(user_need_state, [])

