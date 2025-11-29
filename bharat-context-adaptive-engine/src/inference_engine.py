"""
Bharat Context-Adaptive Engine - Inference Engine
Core logic for inferring user need states from implicit signals
"""

import yaml
import os
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime
from .models import RawSignals, InferenceOutput, UIMode, LanguagePreference


class RuleCondition:
    """Represents a single condition in a rule"""
    
    def __init__(self, condition_dict: Dict[str, Any]):
        self.signal = condition_dict.get("signal")
        self.operator = condition_dict.get("operator")
        self.value = condition_dict.get("value")
        self.weight = condition_dict.get("weight", 1.0)
    
    def evaluate(self, signal_value: Any) -> Tuple[bool, float]:
        """
        Evaluate condition against signal value
        Returns: (matches, score)
        """
        if signal_value is None:
            return (False, 0.0)
        
        matches = False
        
        if self.operator == "equals":
            matches = signal_value == self.value
        elif self.operator == "not_equals":
            matches = signal_value != self.value
        elif self.operator == "in":
            if isinstance(self.value, list):
                matches = signal_value in self.value
            else:
                matches = signal_value == self.value
        elif self.operator == "not_in":
            if isinstance(self.value, list):
                matches = signal_value not in self.value
            else:
                matches = signal_value != self.value
        elif self.operator == "between":
            if isinstance(self.value, list) and len(self.value) == 2:
                matches = self.value[0] <= signal_value <= self.value[1]
        elif self.operator == "greater_than":
            matches = signal_value > self.value
        elif self.operator == "less_than":
            matches = signal_value < self.value
        elif self.operator == "contains":
            if isinstance(signal_value, (str, list)):
                if isinstance(self.value, str):
                    matches = self.value in str(signal_value)
                elif isinstance(self.value, list):
                    matches = any(v in str(signal_value) for v in self.value)
        
        score = self.weight if matches else 0.0
        return (matches, score)


class InferenceRule:
    """Represents a single inference rule"""
    
    def __init__(self, rule_dict: Dict[str, Any]):
        self.name = rule_dict.get("name")
        self.description = rule_dict.get("description", "")
        self.conditions = [
            RuleCondition(cond) for cond in rule_dict.get("conditions", [])
        ]
        self.output = rule_dict.get("output", {})
        self.confidence_threshold = self.output.get("confidence_threshold", 0.0)
    
    def score(self, signals: RawSignals) -> Tuple[float, List[str], List[str]]:
        """
        Score this rule against signals
        Returns: (total_score, matched_conditions, top_signals)
        """
        total_score = 0.0
        matched_conditions = []
        top_signals = []
        
        for condition in self.conditions:
            signal_value = getattr(signals, condition.signal, None)
            matches, score = condition.evaluate(signal_value)
            
            if matches:
                total_score += score
                matched_conditions.append(condition.signal)
                top_signals.append(f"{condition.signal}={signal_value}")
        
        # Sort top signals by weight (simplified - showing all matched)
        return (total_score, matched_conditions, top_signals[:5])


class InferenceEngine:
    """Main inference engine class"""
    
    def __init__(self, rules_path: Optional[str] = None):
        """
        Initialize inference engine
        Args:
            rules_path: Path to rules.yaml file. If None, looks for rules.yaml in current directory.
        """
        if rules_path is None:
            rules_path = Path(__file__).parent / "rules.yaml"
        
        self.rules_path = Path(rules_path)
        self.rules: List[InferenceRule] = []
        self.default_rule: Dict[str, Any] = {}
        self.scoring_config: Dict[str, Any] = {}
        self.output_config: Dict[str, Any] = {}
        
        self._load_rules()
    
    def _load_rules(self):
        """Load rules from YAML file"""
        if not self.rules_path.exists():
            raise FileNotFoundError(f"Rules file not found: {self.rules_path}")
        
        with open(self.rules_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Load rules
        rules_list = config.get("rules", [])
        self.rules = [InferenceRule(rule) for rule in rules_list]
        
        # Load default rule
        self.default_rule = config.get("default_rule", {})
        
        # Load scoring config
        self.scoring_config = config.get("scoring", {})
        
        # Load output config
        self.output_config = config.get("output", {})
    
    def extract_signals(self, payload: Dict[str, Any]) -> RawSignals:
        """
        Extract and validate signals from raw payload
        Args:
            payload: Raw dictionary of signals
        Returns:
            RawSignals object
        """
        # Convert payload to RawSignals, handling nested structures
        signals_dict = {}
        
        for key, value in payload.items():
            # Handle nested signal structures if needed
            if isinstance(value, dict):
                # Flatten if necessary
                signals_dict[key] = value
            else:
                signals_dict[key] = value
        
        return RawSignals(**signals_dict)
    
    def score_rules(self, signals: RawSignals) -> List[Tuple[InferenceRule, float, List[str], List[str]]]:
        """
        Score all rules against signals
        Returns:
            List of (rule, score, matched_conditions, top_signals) tuples, sorted by score
        """
        rule_scores = []
        
        for rule in self.rules:
            score, matched_conditions, top_signals = rule.score(signals)
            rule_scores.append((rule, score, matched_conditions, top_signals))
        
        # Sort by score (descending)
        rule_scores.sort(key=lambda x: x[1], reverse=True)
        
        return rule_scores
    
    def infer_need_state(
        self, 
        signals: RawSignals,
        rule_scores: Optional[List[Tuple[InferenceRule, float, List[str], List[str]]]] = None
    ) -> Tuple[str, float, str, List[str], List[str]]:
        """
        Infer user need state from signals
        Returns:
            (user_need_state, confidence, matched_rule_name, matched_conditions, top_signals)
        """
        if rule_scores is None:
            rule_scores = self.score_rules(signals)
        
        if not rule_scores:
            # Fallback to default rule
            default_state = self.default_rule.get("user_need_state", "First-time AI Explorer")
            return (default_state, 0.0, "default", [], [])
        
        # Get top scoring rule
        top_rule, top_score, matched_conditions, top_signals = rule_scores[0]
        
        # Check if score meets threshold
        min_confidence = self.scoring_config.get("min_confidence", 3.0)
        max_confidence = self.scoring_config.get("max_confidence", 10.0)
        
        if top_score < top_rule.confidence_threshold:
            # Check if any rule meets minimum confidence
            default_state = self.default_rule.get("user_need_state", "First-time AI Explorer")
            for rule, score, conditions, signals_list in rule_scores:
                if score >= rule.confidence_threshold and score >= min_confidence:
                    output = rule.output
                    confidence = min(score, max_confidence)
                    return (
                        output.get("user_need_state", default_state),
                        confidence,
                        rule.name,
                        conditions,
                        signals_list
                    )
            
            # Fallback to default
            return (default_state, 0.0, "default", [], [])
        
        # Use top rule
        output = top_rule.output
        confidence = min(top_score, max_confidence)
        user_need_state = output.get("user_need_state", self.default_rule.get("user_need_state"))
        
        return (user_need_state, confidence, top_rule.name, matched_conditions, top_signals)
    
    def generate_recommendations(
        self,
        user_need_state: str,
        matched_rule_name: str,
        signals: RawSignals
    ) -> Tuple[List[str], UIMode, LanguagePreference]:
        """
        Generate recommendations based on user need state
        Returns:
            (recommended_actions, ui_mode, language_preference)
        """
        # Find the rule that generated this state
        matched_rule = None
        for rule in self.rules:
            if rule.name == matched_rule_name:
                matched_rule = rule
                break
        
        if matched_rule:
            output = matched_rule.output
            actions = output.get("recommended_actions", [])
            ui_mode_str = output.get("ui_mode", "standard")
            lang_pref_str = output.get("language_preference", "system_default")
        else:
            # Use default rule
            actions = self.default_rule.get("recommended_actions", [])
            ui_mode_str = self.default_rule.get("ui_mode", "standard")
            lang_pref_str = self.default_rule.get("language_preference", "system_default")
        
        # Limit actions count
        max_actions = self.output_config.get("max_recommended_actions", 5)
        min_actions = self.output_config.get("min_recommended_actions", 3)
        actions = actions[:max_actions]
        
        # Ensure minimum actions
        if len(actions) < min_actions:
            default_actions = self.default_rule.get("recommended_actions", [])
            actions.extend(default_actions[:min_actions - len(actions)])
        
        # Convert to enums
        try:
            ui_mode = UIMode(ui_mode_str)
        except ValueError:
            ui_mode = UIMode.STANDARD
        
        try:
            language_preference = LanguagePreference(lang_pref_str)
        except ValueError:
            language_preference = LanguagePreference.SYSTEM_DEFAULT
        
        return (actions, ui_mode, language_preference)
    
    def generate_explanation(
        self,
        user_need_state: str,
        matched_conditions: List[str],
        top_signals: List[str],
        confidence: float
    ) -> str:
        """
        Generate human-readable explanation for inference
        """
        template = self.output_config.get(
            "explanation_template",
            "Inferred based on {matched_conditions} signals: {top_signals}"
        )
        
        explanation = template.format(
            matched_conditions=len(matched_conditions),
            top_signals=", ".join(top_signals[:3]) if top_signals else "system defaults",
            confidence=confidence,
            user_need_state=user_need_state
        )
        
        # Enhanced explanation
        if matched_conditions:
            explanation = (
                f"Inferred '{user_need_state}' with confidence {confidence:.1f}/10.0 "
                f"based on {len(matched_conditions)} matching signals: "
                f"{', '.join(matched_conditions[:5])}. "
                f"Key indicators: {', '.join(top_signals[:3]) if top_signals else 'N/A'}."
            )
        else:
            explanation = (
                f"Inferred '{user_need_state}' using default rule. "
                f"Confidence: {confidence:.1f}/10.0 (low - insufficient signals)."
            )
        
        return explanation
    
    def infer(self, signals: RawSignals) -> InferenceOutput:
        """
        Complete inference pipeline
        Args:
            signals: RawSignals object
        Returns:
            InferenceOutput object
        """
        # Score all rules
        rule_scores = self.score_rules(signals)
        
        # Infer need state
        user_need_state, confidence, matched_rule_name, matched_conditions, top_signals = \
            self.infer_need_state(signals, rule_scores)
        
        # Generate recommendations
        recommended_actions, ui_mode, language_preference = \
            self.generate_recommendations(user_need_state, matched_rule_name, signals)
        
        # Generate explanation
        explanation = self.generate_explanation(
            user_need_state, matched_conditions, top_signals, confidence
        )
        
        # Create output
        return InferenceOutput(
            user_need_state=user_need_state,
            confidence=confidence,
            recommended_actions=recommended_actions,
            ui_mode=ui_mode,
            language_preference=language_preference,
            explanation=explanation,
            matched_rule=matched_rule_name,
            matched_signals=matched_conditions,
            signal_count=len(matched_conditions)
        )


# Singleton instance (can be initialized with custom rules path)
_engine_instance: Optional[InferenceEngine] = None


def get_inference_engine(rules_path: Optional[str] = None) -> InferenceEngine:
    """
    Get or create inference engine instance
    Args:
        rules_path: Optional path to rules.yaml file
    Returns:
        InferenceEngine instance
    """
    global _engine_instance
    
    if _engine_instance is None:
        _engine_instance = InferenceEngine(rules_path)
    
    return _engine_instance

