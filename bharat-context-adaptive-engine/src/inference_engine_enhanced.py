"""
Enhanced Inference Engine for Bharat Context-Adaptive Engine
Uses signals + web intelligence + app context + LLM reasoning
"""

import yaml
import os
import uuid
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime

from .models import RawSignals, InferenceOutput, UIMode, LanguagePreference, FeedItem
from .explanation_models import InferenceExplanation, ExplanationEvent, ExplanationEventType
from .web_intelligence import WebIntelligence
from .app_context import AppContext
from .llm_reasoning import LLMReasoning
from .llm_service import get_llm_service

# Import original rule-based engine
from .inference_engine import InferenceEngine, InferenceRule, RuleCondition


class EnhancedInferenceEngine(InferenceEngine):
    """Enhanced inference engine with web intelligence, app context, and LLM reasoning"""
    
    def __init__(self, rules_path: Optional[str] = None):
        """Initialize enhanced inference engine"""
        super().__init__(rules_path)
        self.web_intelligence = WebIntelligence()
        self.app_context = AppContext()
        self.llm_reasoning = LLMReasoning()
        self.llm_service = get_llm_service()
        self.explanations: Dict[str, InferenceExplanation] = {}
    
    def infer(self, signals: RawSignals) -> InferenceOutput:
        """
        Complete enhanced inference pipeline with explanation logging
        """
        inference_id = str(uuid.uuid4())
        explanation = InferenceExplanation(inference_id=inference_id)
        
        step = 0
        
        # Step 1: Signal Extraction and Summary
        step += 1
        signal_summary = self._extract_signal_summary(signals)
        explanation.signal_summary = signal_summary
        explanation.signal_count = sum(signal_summary.values())
        explanation.signal_categories = list(signal_summary.keys())
        
        explanation.add_event(ExplanationEvent(
            event_type=ExplanationEventType.SIGNAL_EXTRACTION,
            step=step,
            description=f"Extracted and analyzed {explanation.signal_count} signals across {len(explanation.signal_categories)} categories",
            input_signals={"signal_count": explanation.signal_count, "categories": explanation.signal_categories},
            output={"signal_summary": signal_summary}
        ))
        
        # Step 2: Web Intelligence Analysis
        step += 1
        web_intel_result = self.web_intelligence.analyze_signals(signals)
        explanation.web_intelligence_applied = web_intel_result.get("web_intelligence_applied", False)
        explanation.web_intelligence_insights = web_intel_result.get("insights", [])
        
        explanation.add_event(ExplanationEvent(
            event_type=ExplanationEventType.WEB_INTELLIGENCE,
            step=step,
            description=f"Applied web intelligence: {len(web_intel_result.get('insights', []))} insights, {len(web_intel_result.get('detected_patterns', []))} patterns detected",
            input_signals={"signals_analyzed": explanation.signal_count},
            processing_details={"patterns_detected": web_intel_result.get("detected_patterns", [])},
            output={"insights": web_intel_result.get("insights", [])},
            reasoning="Web intelligence provides contextual knowledge about signal patterns and their meanings in Indian context"
        ))
        
        # Step 3: App Context Analysis
        step += 1
        app_context_result = self.app_context.analyze_app_context(signals)
        explanation.app_context_applied = app_context_result.get("app_context_applied", False)
        explanation.app_context_insights = app_context_result.get("insights", [])
        
        explanation.add_event(ExplanationEvent(
            event_type=ExplanationEventType.APP_CONTEXT,
            step=step,
            description=f"Applied app context: {len(app_context_result.get('detected_use_cases', []))} use cases detected",
            input_signals={"signals_analyzed": explanation.signal_count},
            processing_details={"use_cases": app_context_result.get("detected_use_cases", [])},
            output={"insights": app_context_result.get("insights", [])},
            reasoning="App context provides ChatGPT-specific understanding of user behaviors and Indian use cases"
        ))
        
        # Step 4: LLM Reasoning
        step += 1
        llm_result = self.llm_reasoning.reason(signals, web_intel_result, app_context_result)
        explanation.llm_reasoning_applied = llm_result.get("llm_reasoning_applied", False)
        explanation.llm_reasoning_insights = llm_result.get("insights", [])
        
        explanation.add_event(ExplanationEvent(
            event_type=ExplanationEventType.LLM_REASONING,
            step=step,
            description=f"Applied LLM reasoning: {len(llm_result.get('insights', []))} insights, {len(llm_result.get('reasoning_steps', []))} reasoning steps",
            input_signals={"web_intelligence": web_intel_result, "app_context": app_context_result},
            processing_details={"reasoning_steps": llm_result.get("reasoning_steps", [])},
            output={"insights": llm_result.get("insights", [])},
            reasoning="LLM reasoning applies worldly knowledge and cross-signal correlation for deeper understanding"
        ))
        
        # Step 5: Enhanced Rule Scoring with Adjustments
        step += 1
        rule_scores = self.score_rules(signals)
        
        # Apply confidence adjustments from web intelligence and LLM reasoning
        confidence_adjustments = {}
        confidence_adjustments.update(web_intel_result.get("confidence_adjustments", {}))
        confidence_adjustments.update(llm_result.get("confidence_adjustments", {}))
        
        # Adjust rule scores based on confidence adjustments
        adjusted_rule_scores = self._adjust_rule_scores(rule_scores, confidence_adjustments, 
                                                         web_intel_result, app_context_result, llm_result)
        
        # Prepare rule scores for explanation
        top_rules_list = []
        for rule, score, matched_conditions, top_signals in adjusted_rule_scores[:5]:
            top_rules_list.append({
                "name": rule.name,
                "score": score,
                "matched_conditions": len(matched_conditions),
                "top_signals": top_signals[:3]
            })
        explanation.top_rules = top_rules_list
        explanation.rule_scores = {rule.name: score for rule, score, _, _ in adjusted_rule_scores}
        
        explanation.add_event(ExplanationEvent(
            event_type=ExplanationEventType.RULE_SCORING,
            step=step,
            description=f"Scored {len(rule_scores)} rules, top score: {adjusted_rule_scores[0][1]:.2f}",
            input_signals={"rule_count": len(rule_scores)},
            processing_details={"confidence_adjustments": confidence_adjustments},
            output={"top_rules": top_rules_list[:3]},
            reasoning="Rule scoring with confidence adjustments from web intelligence and LLM reasoning"
        ))
        
        # Step 6: Signal Correlation Analysis
        step += 1
        correlation_insights = self._analyze_signal_correlations(signals, web_intel_result, 
                                                                  app_context_result, llm_result)
        
        explanation.add_event(ExplanationEvent(
            event_type=ExplanationEventType.SIGNAL_CORRELATION,
            step=step,
            description=f"Analyzed signal correlations: {len(correlation_insights)} correlations found",
            input_signals={"signals_analyzed": explanation.signal_count},
            output={"correlations": correlation_insights},
            reasoning="Signal correlation identifies strong patterns across multiple signal categories"
        ))
        
        # Step 7: Contextual Inference
        step += 1
        contextual_result = self._contextual_inference(signals, adjusted_rule_scores, 
                                                       web_intel_result, app_context_result, llm_result)
        
        explanation.add_event(ExplanationEvent(
            event_type=ExplanationEventType.CONTEXTUAL_INFERENCE,
            step=step,
            description=f"Applied contextual inference: {contextual_result.get('reasoning', 'N/A')}",
            input_signals={"rule_scores": len(adjusted_rule_scores), "web_intel": web_intel_result, "app_context": app_context_result},
            output={"inference": contextual_result.get("user_need_state")},
            reasoning=contextual_result.get("reasoning", "")
        ))
        
        # Step 8: Final Decision
        step += 1
        user_need_state, confidence, matched_rule_name, matched_conditions, top_signals = \
            self.infer_need_state(signals, adjusted_rule_scores)
        
        # Check for LLM Override
        llm_inference = llm_result.get("llm_inference_result")
        if llm_inference and llm_inference.get("user_need_state"):
            # LLM provided a decision
            user_need_state = llm_inference.get("user_need_state")
            confidence = float(llm_inference.get("confidence", 5.0))
            matched_rule_name = "LLM_Inference"
            # Use LLM provided metadata if available
            if llm_inference.get("ui_mode"):
                 try:
                     ui_mode = UIMode(llm_inference.get("ui_mode"))
                 except:
                     pass # Keep rule-based default or previous
            if llm_inference.get("language_preference"):
                 try:
                     language_preference = LanguagePreference(llm_inference.get("language_preference"))
                 except:
                     pass

        # Apply final adjustments (if not fully overridden by LLM confidence, or maybe combine)
        # If LLM gave high confidence, we trust it.
        final_confidence = self._calculate_final_confidence(
            confidence, confidence_adjustments, web_intel_result, app_context_result, llm_result
        )
        
        explanation.final_user_need_state = user_need_state
        explanation.final_confidence = final_confidence
        
        # Generate decision factors
        decision_factors = self._generate_decision_factors(
            signals, user_need_state, matched_rule_name, web_intel_result, 
            app_context_result, llm_result, adjusted_rule_scores
        )
        explanation.decision_factors = decision_factors
        
        explanation.add_event(ExplanationEvent(
            event_type=ExplanationEventType.FINAL_DECISION,
            step=step,
            description=f"Final decision: {user_need_state} (confidence: {final_confidence:.2f}/10.0)",
            input_signals={"top_rule": matched_rule_name, "confidence": confidence},
            processing_details={"decision_factors": decision_factors},
            output={"user_need_state": user_need_state, "confidence": final_confidence},
            reasoning=f"Inferred based on {len(matched_conditions)} matching signals, web intelligence, app context, and LLM reasoning"
        ))
        
        # Generate recommendations
        recommended_actions, ui_mode, language_preference = \
            self.generate_recommendations(user_need_state, matched_rule_name, signals)
        
        # Override recommendations if LLM provided them
        if llm_inference and llm_inference.get("recommended_actions"):
            recommended_actions = llm_inference.get("recommended_actions")
            # Ensure we have enums correct if LLM provided them
            if llm_inference.get("ui_mode"):
                try:
                    ui_mode = UIMode(llm_inference.get("ui_mode"))
                except:
                    pass
            if llm_inference.get("language_preference"):
                try:
                    language_preference = LanguagePreference(llm_inference.get("language_preference"))
                except:
                    pass

        # Enhance recommendations with app context
        if app_context_result.get("prompt_suggestions"):
            recommended_actions = self._enhance_recommendations(
                recommended_actions, app_context_result.get("prompt_suggestions", [])
            )
        
        # Generate human-readable explanation
        human_explanation = explanation.generate_human_readable()
        explanation.human_readable_explanation = human_explanation
        
        # Store explanation
        self.explanations[inference_id] = explanation
        
        # Generate Personalized Feed using Perplexity
        feed_items = []
        try:
            # Use the inferred state and language to get real content
            raw_feed = self.llm_service.generate_feed_from_perplexity(user_need_state, language_preference.value)
            
            for item in raw_feed:
                feed_items.append(FeedItem(
                    id=item.get('id', str(uuid.uuid4())),
                    type=item.get('type', 'news'),
                    title=item.get('title', 'Update'),
                    summary=item.get('summary', ''),
                    source=item.get('source', 'BharatAI'),
                    time=item.get('time', 'Just now'),
                    tags=item.get('tags', [])
                ))
        except Exception as e:
            print(f"Feed generation failed: {e}")
            # Fallback to empty feed or default items if needed

        # Create final output
        return InferenceOutput(
            user_need_state=user_need_state,
            confidence=final_confidence,
            recommended_actions=recommended_actions,
            ui_mode=ui_mode,
            language_preference=language_preference,
            explanation=human_explanation,
            matched_rule=matched_rule_name,
            matched_signals=matched_conditions,
            signal_count=len(matched_conditions),
            feed=feed_items
        )
    
    def _extract_signal_summary(self, signals: RawSignals) -> Dict[str, int]:
        """Extract summary of signals by category"""
        summary = {}
        
        # Device signals
        device_signals = [s for s in ["device_class", "ram_size", "network_type", "battery_level"] 
                         if getattr(signals, s, None) is not None]
        if device_signals:
            summary["device"] = len(device_signals)
        
        # App ecosystem signals
        app_signals = [s for s in ["business_apps", "education_apps", "payment_apps_installed", 
                                   "ecommerce_apps", "whatsapp_installed"] 
                      if getattr(signals, s, None) is not None]
        if app_signals:
            summary["app_ecosystem"] = len(app_signals)
        
        # SMS signals
        sms_signals = [s for s in ["sms_volume", "otp_message_frequency", "banking_sms_presence"] 
                       if getattr(signals, s, None) is not None]
        if sms_signals:
            summary["sms"] = len(sms_signals)
        
        # WhatsApp signals
        whatsapp_signals = [s for s in ["whatsapp_installed", "whatsapp_business_usage", 
                                       "whatsapp_notification_frequency"] 
                           if getattr(signals, s, None) is not None]
        if whatsapp_signals:
            summary["whatsapp"] = len(whatsapp_signals)
        
        # Notification signals
        notification_signals = [s for s in ["total_notification_volume", "notification_response_rate"] 
                               if getattr(signals, s, None) is not None]
        if notification_signals:
            summary["notifications"] = len(notification_signals)
        
        # Temporal signals
        temporal_signals = [s for s in ["time_of_day", "hour_of_day", "day_of_week"] 
                           if getattr(signals, s, None) is not None]
        if temporal_signals:
            summary["temporal"] = len(temporal_signals)
        
        # Language signals
        language_signals = [s for s in ["system_language", "keyboard_language", "messaging_language"] 
                           if getattr(signals, s, None) is not None]
        if language_signals:
            summary["language"] = len(language_signals)
        
        return summary
    
    def _adjust_rule_scores(self, rule_scores: List[Tuple], confidence_adjustments: Dict[str, float],
                           web_intel: Dict[str, Any], app_context: Dict[str, Any], 
                           llm_result: Dict[str, Any]) -> List[Tuple]:
        """Adjust rule scores based on confidence adjustments"""
        adjusted_scores = []
        
        for rule, score, matched_conditions, top_signals in rule_scores:
            adjusted_score = score
            
            # Apply pattern-based adjustments
            for pattern, adjustment in confidence_adjustments.items():
                # Check if this rule matches the pattern
                if self._rule_matches_pattern(rule, pattern, web_intel, app_context, llm_result):
                    adjusted_score += adjustment
            
            adjusted_scores.append((rule, adjusted_score, matched_conditions, top_signals))
        
        # Re-sort by adjusted score
        adjusted_scores.sort(key=lambda x: x[1], reverse=True)
        return adjusted_scores
    
    def _rule_matches_pattern(self, rule: InferenceRule, pattern: str, 
                             web_intel: Dict[str, Any], app_context: Dict[str, Any],
                             llm_result: Dict[str, Any]) -> bool:
        """Check if rule matches a pattern"""
        # Simple pattern matching - can be enhanced
        detected_patterns = web_intel.get("detected_patterns", [])
        if pattern in detected_patterns:
            # Check if rule name suggests it matches
            if "business" in pattern and "business" in rule.name.lower():
                return True
            if "education" in pattern and "student" in rule.name.lower():
                return True
            if "hindi" in pattern and "hindi" in rule.name.lower():
                return True
        return False
    
    def _analyze_signal_correlations(self, signals: RawSignals, web_intel: Dict[str, Any],
                                   app_context: Dict[str, Any], llm_result: Dict[str, Any]) -> List[str]:
        """Analyze correlations between signals"""
        correlations = []
        
        # Business correlation
        if (signals.business_apps and isinstance(signals.business_apps, list) and len(signals.business_apps) > 0 and
            signals.whatsapp_business_usage == "yes" and
            signals.payment_apps_installed):
            correlations.append("Strong correlation: Business apps + WhatsApp Business + Payment apps")
        
        # Student correlation
        if (signals.education_apps and isinstance(signals.education_apps, list) and len(signals.education_apps) > 0 and
            signals.session_duration == "long" and
            signals.text_input_length == "long"):
            correlations.append("Strong correlation: Education apps + Long sessions + Long text")
        
        # Transaction correlation
        if (signals.otp_message_frequency == "high" and
            signals.banking_sms_presence == "yes" and
            signals.payment_apps_installed):
            correlations.append("Strong correlation: High OTP + Banking SMS + Payment apps")
        
        return correlations
    
    def _contextual_inference(self, signals: RawSignals, rule_scores: List[Tuple],
                             web_intel: Dict[str, Any], app_context: Dict[str, Any],
                             llm_result: Dict[str, Any]) -> Dict[str, Any]:
        """Apply contextual inference combining all sources"""
        if not rule_scores:
            return {"user_need_state": "First-time AI Explorer", "reasoning": "No rules matched"}
        
        top_rule, top_score, _, _ = rule_scores[0]
        
        # Enhance reasoning with context
        reasoning_parts = [f"Rule '{top_rule.name}' scored {top_score:.2f}"]
        
        if web_intel.get("detected_patterns"):
            reasoning_parts.append(f"Web intelligence detected {len(web_intel.get('detected_patterns', []))} patterns")
        
        if app_context.get("detected_use_cases"):
            reasoning_parts.append(f"App context detected {len(app_context.get('detected_use_cases', []))} use cases")
        
        if llm_result.get("reasoning_steps"):
            reasoning_parts.append(f"LLM reasoning applied {len(llm_result.get('reasoning_steps', []))} reasoning steps")
        
        return {
            "user_need_state": top_rule.output.get("user_need_state", "Unknown"),
            "reasoning": ". ".join(reasoning_parts)
        }
    
    def _calculate_final_confidence(self, base_confidence: float, 
                                    confidence_adjustments: Dict[str, float],
                                    web_intel: Dict[str, Any], app_context: Dict[str, Any],
                                    llm_result: Dict[str, Any]) -> float:
        """Calculate final confidence with adjustments"""
        final_confidence = base_confidence
        
        # Apply adjustments (capped)
        total_adjustment = sum(confidence_adjustments.values())
        final_confidence += min(total_adjustment, 2.0)  # Cap at +2.0
        
        # Boost if multiple sources agree
        if (web_intel.get("detected_patterns") and 
            app_context.get("detected_use_cases") and
            llm_result.get("insights")):
            final_confidence += 0.5  # Multi-source agreement boost
        
        # Cap at 10.0
        return min(final_confidence, 10.0)
    
    def _generate_decision_factors(self, signals: RawSignals, user_need_state: str,
                                   matched_rule: str, web_intel: Dict[str, Any],
                                   app_context: Dict[str, Any], llm_result: Dict[str, Any],
                                   rule_scores: List[Tuple]) -> List[str]:
        """Generate key decision factors"""
        factors = []
        
        # Top rule
        if rule_scores:
            top_rule, top_score, _, _ = rule_scores[0]
            factors.append(f"Rule '{top_rule.name}' scored {top_score:.2f} points")
        
        # Web intelligence patterns
        if web_intel.get("detected_patterns"):
            factors.append(f"Web intelligence: {len(web_intel.get('detected_patterns', []))} patterns detected")
        
        # App context use cases
        if app_context.get("detected_use_cases"):
            factors.append(f"App context: {len(app_context.get('detected_use_cases', []))} use cases detected")
        
        # LLM reasoning
        if llm_result.get("reasoning_steps"):
            factors.append(f"LLM reasoning: {len(llm_result.get('reasoning_steps', []))} reasoning steps applied")
        
        # Key signals
        if signals.business_apps and isinstance(signals.business_apps, list) and len(signals.business_apps) > 0:
            factors.append("Business apps present")
        if signals.whatsapp_business_usage == "yes":
            factors.append("WhatsApp Business usage")
        if signals.otp_message_frequency == "high":
            factors.append("High OTP frequency")
        if signals.education_apps and isinstance(signals.education_apps, list) and len(signals.education_apps) > 0:
            factors.append("Education apps present")
        
        return factors
    
    def _enhance_recommendations(self, base_recommendations: List[str], 
                                prompt_suggestions: List[str]) -> List[str]:
        """Enhance recommendations with app context suggestions"""
        enhanced = base_recommendations.copy()
        
        # Add unique prompt suggestions
        for suggestion in prompt_suggestions[:2]:  # Add top 2
            if suggestion not in enhanced:
                enhanced.append(suggestion)
        
        # Limit to 5
        return enhanced[:5]
    
    def get_explanation(self, inference_id: str) -> Optional[InferenceExplanation]:
        """Get explanation for an inference"""
        return self.explanations.get(inference_id)
    
    def log_explanation(self, inference_id: str, file_path: Optional[str] = None):
        """Log explanation to file"""
        explanation = self.explanations.get(inference_id)
        if not explanation:
            return
        
        if file_path is None:
            file_path = f"explanations/{inference_id}.log"
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(explanation.generate_human_readable())
            f.write("\n\n")
            f.write("=" * 80)
            f.write("\n\n")
            f.write("Detailed Event Log:\n")
            for event in explanation.events:
                f.write(f"\n[{event.step}] {event.event_type.value}\n")
                f.write(f"  Description: {event.description}\n")
                if event.reasoning:
                    f.write(f"  Reasoning: {event.reasoning}\n")
                if event.output:
                    f.write(f"  Output: {event.output}\n")


# Singleton instance
_enhanced_engine_instance: Optional[EnhancedInferenceEngine] = None


def get_enhanced_inference_engine(rules_path: Optional[str] = None) -> EnhancedInferenceEngine:
    """Get or create enhanced inference engine instance"""
    global _enhanced_engine_instance
    
    if _enhanced_engine_instance is None:
        _enhanced_engine_instance = EnhancedInferenceEngine(rules_path)
    
    return _enhanced_engine_instance

