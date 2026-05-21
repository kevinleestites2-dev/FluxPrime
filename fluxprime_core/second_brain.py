"""
Second-Brain — Layer 6 Long-Term Memory
Distills experience into patterns. Identifies multi-mission trends.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any
import time

logging.basicConfig(level=logging.INFO, format='[Second-Brain] %(message)s')
logger = logging.getLogger("Second-Brain")

class SecondBrain:
    """
    Second-Brain is the long-term memory kernel.
    Unlike SAFLA (which is short-term adaptive), Second-Brain
    looks at the "regime of regimes" across multiple missions.
    """
    
    def __init__(self, brain_dir: str = "fluxprime_core/brain"):
        self.brain_path = Path(brain_dir)
        self.brain_path.mkdir(parents=True, exist_ok=True)
        self.knowledge_file = self.brain_path / "long_term_knowledge.json"
        
        self.knowledge = self.load_knowledge()
        logger.info("🧠 Second-Brain online")

    def load_knowledge(self) -> Dict:
        if self.knowledge_file.exists():
            try:
                with open(self.knowledge_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load brain: {e}")
        
        return {
            "patterns": {},
            "prime_competencies": {
                "scout": {"success_rate": 1.0, "total_value": 0},
                "zeus": {"success_rate": 1.0, "total_value": 0},
                "ghost": {"success_rate": 1.0, "total_value": 0}
            },
            "regime_history": [],
            "last_updated": time.time()
        }

    def save_knowledge(self):
        try:
            self.knowledge["last_updated"] = time.time()
            with open(self.knowledge_file, "w") as f:
                json.dump(self.knowledge, f, indent=2)
            logger.info("🧠 Knowledge persisted to long-term memory")
        except Exception as e:
            logger.error(f"Failed to save brain: {e}")

    def distill_experience(self, mission_id: str, results: List[Dict]):
        """
        Takes raw mission results and distills them into long-term patterns.
        """
        logger.info(f"🧪 Distilling experience from mission: {mission_id}")
        
        for cycle in results:
            for outcome in cycle.get("outcomes", []):
                prime = outcome.get("prime")
                value = outcome.get("value", 0)
                result = outcome.get("result")
                
                # Update competency
                comp = self.knowledge["prime_competencies"].get(prime, {"success_rate": 1.0, "total_value": 0})
                comp["total_value"] += value
                
                # Simple success rate update
                current_rate = comp.get("success_rate", 1.0)
                new_data_point = 1.0 if result == "SUCCESS" else 0.0
                comp["success_rate"] = (current_rate * 0.9) + (new_data_point * 0.1) # Rolling average
                
                self.knowledge["prime_competencies"][prime] = comp
        
        self.save_knowledge()

    def get_strategic_guidance(self, goal: str) -> Dict:
        """Returns strategic weight modifiers based on long-term memory."""
        
        guidance = {
            "prime_modifiers": {},
            "strategy": "ADAPTIVE"
        }
        
        # Prefer primes with higher historical success rates and value generation
        for prime, comp in self.knowledge["prime_competencies"].items():
            modifier = comp["success_rate"] * (1 + (comp["total_value"] / 100000)) # Bonus for high value
            guidance["prime_modifiers"][prime] = min(modifier, 1.5) # Cap at 1.5x
            
        logger.info(f"💡 Second-Brain strategic guidance loaded")
        return guidance
