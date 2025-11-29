"""
Pydantic models for Bharat Context-Adaptive Engine
Defines data structures for signals and inference output
"""

from typing import Optional, List, Dict, Any, Literal, Union
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


# Enums for signal values
class DeviceClass(str, Enum):
    LOW_END = "low_end"
    MID_RANGE = "mid_range"
    HIGH_END = "high_end"


class NetworkType(str, Enum):
    WIFI = "wifi"
    FOUR_G = "4g"
    THREE_G = "3g"
    TWO_G = "2g"
    OFFLINE = "offline"


class TimeOfDay(str, Enum):
    EARLY_MORNING = "early_morning"
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    NIGHT = "night"
    LATE_NIGHT = "late_night"


class UIMode(str, Enum):
    STANDARD = "standard"
    LITE = "lite"
    VOICE_FIRST = "voice-first"


class LanguagePreference(str, Enum):
    HINDI = "hindi"
    ENGLISH = "english"
    REGIONAL = "regional"
    MIXED = "mixed"
    SYSTEM_DEFAULT = "system_default"


# Raw Signal Input Model
class RawSignals(BaseModel):
    """Raw signals collected from the client app"""
    
    # Device Signals
    device_class: Optional[DeviceClass] = None
    ram_size: Optional[str] = None  # "1GB", "2GB", etc.
    storage_available: Optional[str] = None  # "low", "medium", "high"
    screen_size: Optional[str] = None
    screen_resolution: Optional[str] = None
    battery_level: Optional[str] = None  # "critical", "low", "medium", "high"
    battery_health: Optional[str] = None
    device_age: Optional[str] = None  # "new", "medium", "old"
    manufacturer: Optional[str] = None
    os_version: Optional[str] = None
    device_model: Optional[str] = None
    app_launch_time: Optional[str] = None  # "fast", "medium", "slow"
    frame_rate: Optional[str] = None
    memory_pressure: Optional[str] = None
    cpu_usage: Optional[str] = None
    thermal_state: Optional[str] = None
    
    # Network Signals
    network_type: Optional[NetworkType] = None
    network_speed: Optional[str] = None  # "fast", "medium", "slow"
    latency: Optional[str] = None  # "low", "medium", "high"
    connection_stability: Optional[str] = None
    data_saver_mode: Optional[str] = None  # "enabled", "disabled"
    roaming_status: Optional[str] = None
    carrier: Optional[str] = None
    network_quality_score: Optional[str] = None
    
    # Locale & Geographic Signals
    state: Optional[str] = None  # State code
    district: Optional[str] = None
    city_tier: Optional[str] = None  # "tier1", "tier2", "tier3", "tier4", "rural"
    timezone: Optional[str] = None
    language_region: Optional[str] = None
    urban_rural: Optional[str] = None
    
    # Cultural Context
    festival_day: Optional[str] = None  # "diwali", "holi", "eid", "none", etc.
    regional_holiday: Optional[str] = None  # "yes", "no"
    weekend: Optional[str] = None  # "yes", "no"
    time_of_day: Optional[TimeOfDay] = None
    
    # Temporal Signals
    hour_of_day: Optional[int] = Field(None, ge=0, le=23)
    day_of_week: Optional[str] = None
    day_of_month: Optional[int] = Field(None, ge=1, le=31)
    month: Optional[int] = Field(None, ge=1, le=12)
    season: Optional[str] = None
    first_launch_time: Optional[datetime] = None
    session_duration: Optional[str] = None  # "short", "medium", "long"
    time_since_install: Optional[str] = None
    
    # App Usage Signals
    installation_source: Optional[str] = None
    referral_code: Optional[str] = None
    campaign_tag: Optional[str] = None
    app_version: Optional[str] = None
    installation_day: Optional[str] = None
    first_action: Optional[str] = None
    time_to_first_interaction: Optional[str] = None
    screen_views: Optional[List[str]] = None
    scroll_behavior: Optional[str] = None
    tap_patterns: Optional[str] = None
    back_button_usage: Optional[str] = None
    app_minimization: Optional[str] = None
    session_count: Optional[int] = None
    
    # Feature Discovery
    keyboard_opened: Optional[str] = None  # "yes", "no"
    voice_button_tapped: Optional[str] = None
    settings_accessed: Optional[str] = None
    help_faq_opened: Optional[str] = None
    example_prompts_viewed: Optional[str] = None
    tutorial_started: Optional[str] = None
    tutorial_completed: Optional[str] = None
    
    # System & Environment Signals
    system_language: Optional[str] = None  # Language code
    keyboard_language: Optional[str] = None
    font_size: Optional[str] = None
    dark_mode: Optional[str] = None
    accessibility_features: Optional[str] = None
    developer_options: Optional[str] = None
    root_status: Optional[str] = None
    
    # App Permissions
    location_permission: Optional[str] = None
    microphone_permission: Optional[str] = None
    storage_permission: Optional[str] = None
    notification_permission: Optional[str] = None
    
    # Installed Apps & App Ecosystem Signals
    total_apps_installed: Optional[str] = None  # "few", "medium", "many"
    communication_apps: Optional[Union[str, List[str]]] = None
    social_media_apps: Optional[Union[str, List[str]]] = None
    video_apps: Optional[Union[str, List[str]]] = None
    music_apps: Optional[Union[str, List[str]]] = None
    news_apps: Optional[Union[str, List[str]]] = None
    gaming_apps: Optional[str] = None  # "yes", "no", "many"
    productivity_apps: Optional[Union[str, List[str]]] = None
    education_apps: Optional[Union[str, List[str]]] = None
    health_fitness_apps: Optional[str] = None
    food_delivery_apps: Optional[Union[str, List[str]]] = None
    travel_apps: Optional[Union[str, List[str]]] = None
    entertainment_apps: Optional[Union[str, List[str]]] = None
    investment_apps: Optional[Union[str, List[str]]] = None
    lending_apps: Optional[str] = None
    financial_app_count: Optional[str] = None
    grocery_apps: Optional[Union[str, List[str]]] = None
    fashion_apps: Optional[Union[str, List[str]]] = None
    shopping_app_count: Optional[str] = None
    business_apps: Optional[Union[str, List[str]]] = None
    accounting_apps: Optional[str] = None
    crm_lead_apps: Optional[str] = None
    work_communication_apps: Optional[Union[str, List[str]]] = None
    email_apps: Optional[Union[str, List[str]]] = None
    regional_news_apps: Optional[str] = None
    regional_entertainment_apps: Optional[str] = None
    government_apps: Optional[Union[str, List[str]]] = None
    local_services_apps: Optional[str] = None
    most_used_app_category: Optional[str] = None
    app_diversity_score: Optional[str] = None
    premium_app_presence: Optional[str] = None
    app_update_frequency: Optional[str] = None
    app_installation_recency: Optional[str] = None
    
    # SMS & Text Message Signals (Metadata Only - No Content)
    sms_permission: Optional[str] = None
    sms_volume: Optional[str] = None  # "low", "medium", "high"
    sms_frequency_pattern: Optional[str] = None
    sms_time_distribution: Optional[str] = None
    sms_sender_types: Optional[str] = None
    otp_message_frequency: Optional[str] = None
    promotional_sms_volume: Optional[str] = None
    banking_sms_presence: Optional[str] = None
    ecommerce_sms_presence: Optional[str] = None
    government_sms_presence: Optional[str] = None
    sms_language_mix: Optional[str] = None
    sms_script_detection: Optional[str] = None
    sms_length_pattern: Optional[str] = None
    sms_emoji_usage: Optional[str] = None
    business_hours_sms: Optional[str] = None
    weekend_sms_pattern: Optional[str] = None
    sms_response_time: Optional[str] = None
    sms_thread_activity: Optional[str] = None
    
    # WhatsApp & Messaging App Signals
    whatsapp_installed: Optional[str] = None
    whatsapp_active: Optional[str] = None
    whatsapp_notification_permission: Optional[str] = None
    whatsapp_notification_frequency: Optional[str] = None
    whatsapp_notification_pattern: Optional[str] = None
    whatsapp_notification_time_distribution: Optional[str] = None
    whatsapp_group_activity: Optional[str] = None
    whatsapp_business_usage: Optional[str] = None
    whatsapp_notification_sender_types: Optional[str] = None
    whatsapp_notification_urgency_pattern: Optional[str] = None
    whatsapp_notification_response_pattern: Optional[str] = None
    whatsapp_call_frequency: Optional[str] = None
    whatsapp_video_call_frequency: Optional[str] = None
    whatsapp_status_updates: Optional[str] = None
    telegram_installed: Optional[str] = None
    telegram_active: Optional[str] = None
    signal_installed: Optional[str] = None
    facebook_messenger_installed: Optional[str] = None
    messaging_app_count: Optional[str] = None
    primary_messaging_app: Optional[str] = None
    
    # Notification Patterns (All Apps)
    total_notification_volume: Optional[str] = None
    notification_permission_status: Optional[str] = None
    notification_dismissal_rate: Optional[str] = None
    notification_response_rate: Optional[str] = None
    do_not_disturb_usage: Optional[str] = None
    notification_sound_enabled: Optional[str] = None
    notification_vibration_enabled: Optional[str] = None
    social_notifications: Optional[str] = None
    communication_notifications: Optional[str] = None
    ecommerce_notifications: Optional[str] = None
    banking_finance_notifications: Optional[str] = None
    news_notifications: Optional[str] = None
    entertainment_notifications: Optional[str] = None
    gaming_notifications: Optional[str] = None
    productivity_notifications: Optional[str] = None
    peak_notification_hours: Optional[str] = None
    weekend_vs_weekday_notification_pattern: Optional[str] = None
    notification_burst_pattern: Optional[str] = None
    silent_hours: Optional[str] = None
    immediate_open_rate: Optional[str] = None
    delayed_open_rate: Optional[str] = None
    notification_to_app_launch: Optional[str] = None
    notification_ignore_rate: Optional[str] = None
    
    # Commerce & Intent Signals
    device_price_tier: Optional[str] = None
    payment_apps_installed: Optional[Union[str, List[str]]] = None
    ecommerce_apps: Optional[Union[str, List[str]]] = None
    banking_apps: Optional[str] = None
    upi_apps: Optional[str] = None
    business_hours_activity: Optional[str] = None
    weekend_activity: Optional[str] = None
    financial_sophistication_score: Optional[str] = None
    work_app_presence: Optional[str] = None
    business_communication_pattern: Optional[str] = None
    
    # Behavioral Heuristics
    return_user: Optional[str] = None  # "yes", "no"
    session_frequency: Optional[str] = None
    time_between_sessions: Optional[str] = None
    abandonment_indicators: Optional[str] = None
    voice_usage: Optional[str] = None
    text_input_length: Optional[str] = None  # "none", "short", "medium", "long"
    copy_paste_behavior: Optional[str] = None
    
    # Cultural & Social Signals (Additional)
    app_language_mix: Optional[str] = None
    messaging_language: Optional[str] = None
    social_engagement_level: Optional[str] = None
    family_communication_pattern: Optional[str] = None
    professional_network: Optional[str] = None
    
    # User Journey Stage
    onboarding_completion: Optional[str] = None
    first_prompt_attempted: Optional[str] = None
    first_response_received: Optional[str] = None
    first_successful_interaction: Optional[str] = None
    
    # Additional metadata
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)
    signal_version: Optional[str] = "1.0"


class FeedItem(BaseModel):
    id: str
    type: str  # 'news', 'insight', 'tip'
    title: str
    summary: str
    source: Optional[str] = "BharatAI"
    time: Optional[str] = "Just now"
    image: Optional[str] = None
    tags: Optional[List[str]] = None

# Inference Output Model
class InferenceOutput(BaseModel):
    """Output from the inference engine"""
    
    user_need_state: str = Field(..., description="Inferred user need state")
    confidence: float = Field(..., ge=0.0, le=10.0, description="Confidence score (0-10)")
    recommended_actions: List[str] = Field(..., min_items=3, max_items=5, description="3-5 recommended actions")
    ui_mode: UIMode = Field(..., description="Recommended UI mode")
    language_preference: LanguagePreference = Field(..., description="Language preference")
    explanation: str = Field(..., description="Explanation of why this inference was made")
    feed: Optional[List[FeedItem]] = Field(default=[], description="Dynamic personalized feed")
    
    # Optional metadata
    matched_rule: Optional[str] = Field(None, description="Name of the matched rule")
    matched_signals: Optional[List[str]] = Field(None, description="Signals that contributed to inference")
    signal_count: Optional[int] = Field(None, description="Number of signals used")
    inference_timestamp: datetime = Field(default_factory=datetime.now)


# API Request Model
class InferenceRequest(BaseModel):
    """Request model for /v1/infer endpoint"""
    
    signals: RawSignals = Field(..., description="Raw signals from client")
    user_id: Optional[str] = Field(None, description="Optional anonymous user ID")
    session_id: Optional[str] = Field(None, description="Optional session ID")


# API Response Model
class InferenceResponse(BaseModel):
    """Response model for /v1/infer endpoint"""
    
    success: bool = Field(..., description="Whether inference was successful")
    data: Optional[InferenceOutput] = Field(None, description="Inference output")
    error: Optional[str] = Field(None, description="Error message if inference failed")
    processing_time_ms: Optional[float] = Field(None, description="Processing time in milliseconds")


# Health Check Model
class HealthCheck(BaseModel):
    """Health check response"""
    
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    rules_loaded: bool = Field(..., description="Whether rules are loaded")
    rules_count: Optional[int] = Field(None, description="Number of rules loaded")
    timestamp: datetime = Field(default_factory=datetime.now)

