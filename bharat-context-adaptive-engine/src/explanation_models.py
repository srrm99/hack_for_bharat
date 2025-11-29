"""
Explanation Event Models for Bharat Context-Adaptive Engine
Tracks reasoning steps and inference logic
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class ExplanationEventType(str, Enum):
    """Types of explanation events"""
    SIGNAL_EXTRACTION = "signal_extraction"
    WEB_INTELLIGENCE = "web_intelligence"
    APP_CONTEXT = "app_context"
    LLM_REASONING = "llm_reasoning"
    RULE_SCORING = "rule_scoring"
    SIGNAL_CORRELATION = "signal_correlation"
    CONTEXTUAL_INFERENCE = "contextual_inference"
    FINAL_DECISION = "final_decision"


class ExplanationEvent(BaseModel):
    """Single explanation event in the inference process"""
    
    event_type: ExplanationEventType = Field(..., description="Type of explanation event")
    timestamp: datetime = Field(default_factory=datetime.now)
    step: int = Field(..., description="Step number in inference process")
    description: str = Field(..., description="Human-readable description")
    input_signals: Optional[Dict[str, Any]] = Field(None, description="Input signals used")
    processing_details: Optional[Dict[str, Any]] = Field(None, description="Processing details")
    output: Optional[Dict[str, Any]] = Field(None, description="Output of this step")
    confidence_contribution: Optional[float] = Field(None, description="Confidence contribution from this step")
    reasoning: Optional[str] = Field(None, description="Reasoning explanation")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class InferenceExplanation(BaseModel):
    """Complete explanation of inference process"""
    
    inference_id: str = Field(..., description="Unique inference ID")
    timestamp: datetime = Field(default_factory=datetime.now)
    events: List[ExplanationEvent] = Field(default_factory=list, description="All explanation events")
    
    # Signal Analysis
    signal_summary: Dict[str, Any] = Field(default_factory=dict, description="Summary of signals analyzed")
    signal_count: int = Field(0, description="Total number of signals")
    signal_categories: List[str] = Field(default_factory=list, description="Signal categories present")
    
    # Web Intelligence
    web_intelligence_applied: bool = Field(False, description="Whether web intelligence was used")
    web_intelligence_insights: Optional[List[str]] = Field(None, description="Web intelligence insights")
    
    # App Context
    app_context_applied: bool = Field(False, description="Whether app context was used")
    app_context_insights: Optional[List[str]] = Field(None, description="App context insights")
    
    # LLM Reasoning
    llm_reasoning_applied: bool = Field(False, description="Whether LLM reasoning was used")
    llm_reasoning_insights: Optional[List[str]] = Field(None, description="LLM reasoning insights")
    
    # Rule Scoring
    top_rules: List[Dict[str, Any]] = Field(default_factory=list, description="Top scoring rules")
    rule_scores: Dict[str, float] = Field(default_factory=dict, description="All rule scores")
    
    # Final Decision
    final_user_need_state: Optional[str] = Field(None, description="Final inferred user need state")
    final_confidence: Optional[float] = Field(None, description="Final confidence score")
    decision_factors: List[str] = Field(default_factory=list, description="Key factors in decision")
    
    # Human-readable explanation
    human_readable_explanation: str = Field("", description="Complete human-readable explanation")
    
    def add_event(self, event: ExplanationEvent):
        """Add an explanation event"""
        self.events.append(event)
    
    def generate_human_readable(self) -> str:
        """Generate human-readable explanation"""
        parts = []
        
        # Introduction
        parts.append(f"Inference Process (ID: {self.inference_id})")
        parts.append(f"Analyzed {self.signal_count} signals across {len(self.signal_categories)} categories")
        parts.append("")
        
        # Signal Summary
        if self.signal_summary:
            parts.append("Signal Analysis:")
            for category, count in self.signal_summary.items():
                parts.append(f"  - {category}: {count} signals")
            parts.append("")
        
        # Web Intelligence
        if self.web_intelligence_applied and self.web_intelligence_insights:
            parts.append("Web Intelligence Insights:")
            for insight in self.web_intelligence_insights:
                parts.append(f"  - {insight}")
            parts.append("")
        
        # App Context
        if self.app_context_applied and self.app_context_insights:
            parts.append("App Context Insights:")
            for insight in self.app_context_insights:
                parts.append(f"  - {insight}")
            parts.append("")
        
        # LLM Reasoning
        if self.llm_reasoning_applied and self.llm_reasoning_insights:
            parts.append("LLM Reasoning Insights:")
            for insight in self.llm_reasoning_insights:
                parts.append(f"  - {insight}")
            parts.append("")
        
        # Rule Scoring
        if self.top_rules:
            parts.append("Rule Scoring:")
            for i, rule in enumerate(self.top_rules[:3], 1):
                parts.append(f"  {i}. {rule.get('name', 'Unknown')}: {rule.get('score', 0):.2f} points")
            parts.append("")
        
        # Decision Factors
        if self.decision_factors:
            parts.append("Key Decision Factors:")
            for factor in self.decision_factors:
                parts.append(f"  - {factor}")
            parts.append("")
        
        # Final Decision
        if self.final_user_need_state:
            parts.append(f"Final Inference: {self.final_user_need_state}")
            parts.append(f"Confidence: {self.final_confidence:.2f}/10.0")
        
        # Event Timeline
        if self.events:
            parts.append("")
            parts.append("Inference Timeline:")
            for event in self.events:
                parts.append(f"  [{event.step}] {event.event_type.value}: {event.description}")
                if event.reasoning:
                    parts.append(f"      Reasoning: {event.reasoning}")
        
        self.human_readable_explanation = "\n".join(parts)
        return self.human_readable_explanation

