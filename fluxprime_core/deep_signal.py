"""
Deep-Signal — Layer 3 Truth Validation
Filters noise from signal. Prevents false outcomes from corrupting SAFLA weights.
"""

import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format='[Deep-Signal] %(message)s')
logger = logging.getLogger("Deep-Signal")

class DeepSignal:
    """
    Validates task outcomes before they feed back to SAFLA.
    
    False signals (noise, hallucinations, unverified claims) corrupt
    the learning algorithm. Deep-Signal is the immune system.
    """
    
    def __init__(self):
        self.validation_rules = {
            "min_value": 0,
            "max_value_per_cycle": 10000,  # Sanity check
            "required_fields": ["task", "prime", "result", "value"],
            "allowed_results": ["SUCCESS", "FAILED", "PARTIAL"],
            "entropy_threshold": 0.95  # Panic mode
        }
        logger.info("🧬 Deep-Signal initialized")
    
    def validate_outcome(self, outcome: Dict[str, Any], context: Dict = None) -> tuple:
        """
        Validates a task outcome before it influences SAFLA.
        
        Returns: (is_valid: bool, confidence: float, reason: str)
        """
        
        # === Check 1: Required Fields ===
        missing = [f for f in self.validation_rules["required_fields"] if f not in outcome]
        if missing:
            reason = f"Missing fields: {missing}"
            logger.warn(f"❌ {reason}")
            return False, 0.0, reason
        
        # === Check 2: Value Sanity ===
        value = outcome.get("value", 0)
        
        if value < self.validation_rules["min_value"]:
            reason = f"Negative value: {value} (below minimum)"
            logger.warn(f"❌ {reason}")
            return False, 0.2, reason
        
        if value > self.validation_rules["max_value_per_cycle"]:
            reason = f"Unrealistic value: {value} (exceeds sanity check)"
            logger.warn(f"⚠️  {reason} — marking suspicious")
            return True, 0.4, reason  # Valid but low confidence
        
        # === Check 3: Result Type ===
        result = outcome.get("result")
        if result not in self.validation_rules["allowed_results"]:
            reason = f"Invalid result type: {result}"
            logger.warn(f"❌ {reason}")
            return False, 0.0, reason
        
        # === Check 4: Logical Consistency ===
        if result == "FAILED" and value > 100:
            reason = "Inconsistency: marked FAILED but high value"
            logger.warn(f"⚠️  {reason}")
            return True, 0.5, reason  # Valid but suspicious
        
        if result == "SUCCESS" and value == 0:
            reason = "Inconsistency: marked SUCCESS but zero value"
            logger.warn(f"⚠️  {reason}")
            return True, 0.6, reason  # Valid but low confidence
        
        # === Check 5: Cross-Prime Consistency (if context provided) ===
        if context:
            recent_outcomes = context.get("recent_outcomes", [])
            recent_values = [
                o.get("total_value_generated", o.get("value", 0)) 
                for o in recent_outcomes
            ]
            recent_avg = sum(recent_values) / len(recent_values) if recent_values else 500
            
            # Extreme outliers (>3x the average) are flagged as suspicious
            if value > recent_avg * 3:
                reason = f"Statistical outlier: {value} vs avg {recent_avg:.0f}"
                logger.warn(f"⚠️  {reason}")
                return True, 0.65, reason
        
        # === All checks passed ===
        logger.info(f"✅ Outcome validated: {outcome['task']} = ${value:.2f}")
        return True, 1.0, "Valid"
    
    def filter_outcomes(self, outcomes: list, context: Dict = None) -> tuple:
        """
        Filters a batch of outcomes and returns (valid_outcomes, confidence_map).
        
        outcomes: List of outcome dicts
        context: Mission context (recent history, regime, entropy)
        
        Returns: (filtered_outcomes, confidence_scores)
        """
        valid_outcomes = []
        confidence_map = {}
        
        logger.info(f"🔍 Validating {len(outcomes)} outcomes...")
        
        for outcome in outcomes:
            is_valid, confidence, reason = self.validate_outcome(outcome, context)
            task_id = outcome.get("task", "unknown")
            
            if is_valid:
                valid_outcomes.append(outcome)
                confidence_map[task_id] = confidence
                
                if confidence < 1.0:
                    logger.info(f"   ⚠️  {task_id}: {confidence:.0%} confidence — {reason}")
                else:
                    logger.info(f"   ✅ {task_id}: {confidence:.0%} confidence")
            else:
                logger.info(f"   ❌ {task_id}: REJECTED — {reason}")
                # Rejected outcomes do NOT feed back to SAFLA
        
        logger.info(f"📊 Filtered: {len(valid_outcomes)}/{len(outcomes)} outcomes passed")
        return valid_outcomes, confidence_map
    
    def adjust_safla_feedback(self, outcome: Dict, confidence: float) -> Dict:
        """
        Adjusts SAFLA feedback based on validation confidence.
        
        High confidence (1.0) → Feed as-is
        Medium confidence (0.5-0.99) → Dampen the signal
        Low confidence (<0.5) → Filter out entirely
        """
        
        if confidence < 0.5:
            return None  # Don't feed to SAFLA
        
        if confidence < 0.95:
            # Dampen the value signal
            dampening_factor = confidence
            outcome["value"] = outcome.get("value", 0) * dampening_factor
            outcome["_signal_confidence"] = confidence
            logger.info(f"📉 Dampening signal by {(1-confidence):.0%}")
        
        return outcome
