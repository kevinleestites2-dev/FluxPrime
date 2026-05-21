"""
Task Executor — Layer 4 (The Jet)
Intelligent task prioritization and resource allocation.
"""

import logging
from typing import Dict, List, Any
import json

logging.basicConfig(level=logging.INFO, format='[Jet] %(message)s')
logger = logging.getLogger("Jet")

class TaskExecutor:
    """
    The Jet prioritizes tasks based on:
    - SAFLA weights (what has worked before)
    - Available resources
    - Current regime (STABLE_FLOW, CHAOTIC_NOISE, etc.)
    - Entropy level
    """
    
    def __init__(self):
        self.execution_history = []
        logger.info("🚀 Jet initialized")
    
    def prioritize(self, tasks: List[Dict], safla_state: Dict, resources: Dict) -> List[Dict]:
        """
        Rank tasks by priority based on SAFLA intelligence.
        
        Higher priority = Execute first, allocate more resources.
        """
        
        weights = safla_state.get("weights", {})
        regime = safla_state.get("regime", "UNKNOWN")
        entropy = safla_state.get("entropy", 0.5)
        
        logger.info(f"📋 Prioritizing {len(tasks)} tasks")
        logger.info(f"   Regime: {regime} | Entropy: {entropy:.2f}")
        
        scored_tasks = []
        
        for task in tasks:
            prime = task.get("prime")
            task_name = task.get("name")
            
            # Get weight for this Prime from SAFLA history
            prime_weight = weights.get(f"{prime}_prime", 1.0)
            
            # Entropy-based adjustments
            if entropy > 0.8:
                # Chaotic times: prefer conservative, proven strategies
                priority_score = prime_weight * 0.8
                logger.info(f"   ⚠️  High entropy: dampening {prime}")
            elif entropy < 0.3:
                # Stable times: push higher-risk tasks
                priority_score = prime_weight * 1.2
                logger.info(f"   ✅ Low entropy: accelerating {prime}")
            else:
                # Normal times: use historical weights
                priority_score = prime_weight
            
            # Regime-based boost
            if regime == "STABLE_FLOW":
                priority_score *= 1.0  # Normal
            elif regime == "MOMENTUM_UP":
                priority_score *= 1.15  # Accelerate
            elif regime == "CHAOTIC_NOISE":
                priority_score *= 0.85  # Conservative
            
            # Resource availability boost
            allocated = resources.get(prime, 0.0)
            if allocated > 0.4:
                priority_score *= 1.1  # More resources = more aggressive
            
            scored_tasks.append({
                **task,
                "priority_score": priority_score,
                "weight": prime_weight,
                "regime_boost": 1.15 if regime == "MOMENTUM_UP" else (0.85 if regime == "CHAOTIC_NOISE" else 1.0)
            })
        
        # Sort by priority_score (highest first)
        sorted_tasks = sorted(scored_tasks, key=lambda x: x["priority_score"], reverse=True)
        
        # Log the ranking
        logger.info(f"🎯 Task Execution Order:")
        for i, task in enumerate(sorted_tasks, 1):
            logger.info(f"   {i}. {task['name']:30} (score: {task['priority_score']:.2f})")
        
        return sorted_tasks
    
    def allocate_resources(self, tasks: List[Dict], total_budget: float, safla_state: Dict) -> Dict:
        """
        Dynamically allocate resources across tasks based on priority scores.
        """
        
        total_score = sum(t.get("priority_score", 1.0) for t in tasks)
        allocations = {}
        
        logger.info(f"💰 Allocating ${total_budget:.2f} across {len(tasks)} tasks")
        
        for task in tasks:
            score = task.get("priority_score", 1.0)
            allocation = (score / total_score) * total_budget
            
            task_id = task.get("name")
            allocations[task_id] = allocation
            
            logger.info(f"   {task_id}: ${allocation:.2f}")
        
        return allocations
    
    def record_execution(self, task: Dict, outcome: Dict):
        """Log execution for future learning."""
        record = {
            "task": task.get("name"),
            "prime": task.get("prime"),
            "priority_score": task.get("priority_score"),
            "outcome_value": outcome.get("value", 0),
            "efficiency": outcome.get("value", 0) / task.get("resource_budget", 1.0) if task.get("resource_budget") else 0
        }
        self.execution_history.append(record)
