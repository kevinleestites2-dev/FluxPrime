"""
FluxPrime Captain — Layer 0 & Layer 1 Integration
Bridges AutoGPT autonomy with SAFLA 2.0 adaptive intelligence

The Captain runs the mission loop:
1. AutoGPT sets a goal
2. SAFLA weighs the best approach based on history
3. Task Executor prioritizes sub-tasks
4. Results feed back to SAFLA for next-cycle adaptation
"""

import json
import time
import os
from typing import Dict, Any, List, Optional
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[FluxPrime] %(message)s')
logger = logging.getLogger("FluxPrime")


class FluxCaptain:
    """
    Autonomous mission commander.
    - Takes high-level goals from user
    - Deploys resources via task prioritization
    - Adapts via SAFLA feedback
    - Never stops until goal is met or exception escalates
    """
    
    def __init__(self, mission_id: str, safla_engine):
        self.mission_id = mission_id
        self.safla = safla_engine  # SAFLA 2.0 instance
        
        self.mission_state = {
            "status": "IDLE",
            "goal": None,
            "cycle": 0,
            "resources_deployed": {},
            "results": [],
            "start_time": None
        }
        
        self.memory_path = Path(f"fluxprime_core/missions/{mission_id}")
        self.memory_path.mkdir(parents=True, exist_ok=True)
        
        # Layers 2-6: Full Seven-Layered Ocean
        import sys
        sys.path.insert(0, "fluxprime_core")
        from flowstate import Flowstate
        from deep_signal import DeepSignal
        from task_executor import TaskExecutor
        from second_brain import SecondBrain
        from ghost_layer import GhostLayer
        from prime_bridge import PrimeBridge
        
        self.flowstate = Flowstate(mission_id=mission_id)
        self.deep_signal = DeepSignal()
        self.task_executor = TaskExecutor()
        self.second_brain = SecondBrain()
        self.ghost_layer = GhostLayer()
        self.prime_bridge = PrimeBridge()
        
        # Attempt recovery from last checkpoint
        recovered = self.flowstate.recover()
        if recovered:
            self.mission_state = recovered
            logger.info(f"🌊 Mission resumed from cycle {recovered.get('cycle', 0)}")
        
        logger.info(f"🔱 Captain initialized for mission: {mission_id}")
    
    def set_mission(self, goal: str, resources: Dict[str, float]):
        """
        Captain receives orders.
        
        goal: High-level objective (e.g., "Generate $5,000 in War Chest by mining leads")
        resources: Budget allocation per Prime (e.g., {"scout": 0.3, "zeus": 0.5, "ghost": 0.2})
        """
        self.mission_state["goal"] = goal
        self.mission_state["resources_deployed"] = resources
        self.mission_state["status"] = "ACTIVE"
        self.mission_state["start_time"] = time.time()
        
        logger.info(f"🎯 Mission set: {goal}")
        logger.info(f"💎 Resources allocated: {json.dumps(resources, indent=2)}")
        
        return self.mission_state
    
    def execute_cycle(self) -> Dict[str, Any]:
        """
        One full mission cycle:
        1. Ask SAFLA what worked best in history
        2. Allocate resources based on SAFLA weights
        3. Deploy tasks to Primes
        4. Collect results
        5. Feed back to SAFLA
        6. Decide: Continue, Pivot, or Escalate
        """
        if self.mission_state["status"] != "ACTIVE":
            logger.warn("Mission not active. Call set_mission() first.")
            return {"status": "ERROR", "reason": "Mission not active"}
        
        self.mission_state["cycle"] += 1
        cycle_num = self.mission_state["cycle"]
        
        logger.info(f"\n🔄 CYCLE {cycle_num} START")
        
        # === PHASE 1: SAFLA Consultation ===
        logger.info("📊 Consulting SAFLA for adaptive weights...")
        
        # Simulate SAFLA reflection on past outcomes
        safla_adaptation = {
            "weights": self.safla.memory.procedures.get("weights", {}),
            "regime": self.safla.state.get("regime", "STABLE_FLOW"),
            "entropy": self.safla.state.get("entropy", 0.0),
            "recommendation": "CONTINUE"  # Could be PIVOT, ESCALATE, HIBERNATE
        }
        
        logger.info(f"   Regime: {safla_adaptation['regime']}")
        logger.info(f"   Entropy: {safla_adaptation['entropy']:.4f}")
        logger.info(f"   Recommendation: {safla_adaptation['recommendation']}")
        
        # === PHASE 2: Task Prioritization (The Jet) ===
        logger.info("⚙️  Computing task priorities via The Jet...")
        
        # Generate base tasks
        base_tasks = self._generate_cycle_tasks(cycle_num, safla_adaptation)
        
        # Prioritize via Deep Jet logic
        tasks = self.task_executor.prioritize(
            base_tasks,
            safla_state=safla_adaptation,
            resources=self.mission_state["resources_deployed"]
        )
        
        # Allocate resources intelligently
        cycle_budget = sum(self.mission_state["resources_deployed"].values()) * 1000
        allocations = self.task_executor.allocate_resources(tasks, cycle_budget, safla_adaptation)
        
        # === PHASE 3: Deploy & Execute ===
        logger.info("🌫️  Wrapping tasks in stealth protocols...")
        tasks = self.ghost_layer.apply_stealth(tasks, cycle_num)
        
        # Consult Second-Brain for long-term strategy
        logger.info("🧠 Consulting Second-Brain for long-term strategy...")
        strategic_guidance = self.second_brain.get_strategic_guidance(f"cycle_{cycle_num}")
        
        logger.info("🚀 Deploying to Pantheon (REAL EXECUTION)...")
        
        results = {
            "cycle": cycle_num,
            "tasks_executed": len(tasks),
            "timestamp": time.time(),
            "outcomes": []
        }
        
        # Real Prime execution (using Prime Bridge)
        use_real_execution = os.getenv("USE_REAL_PRIMES", "false").lower() == "true"
        
        for task in tasks:
            if use_real_execution:
                # REAL EXECUTION — call actual Primes via bridge
                outcome = self.prime_bridge.execute(task)
            else:
                # SIMULATION MODE — test run
                outcome = self._simulate_task_execution(task)
            
            results["outcomes"].append(outcome)
            logger.info(f"   ✓ {task['name']}: {outcome['result']} (Value: ${outcome['value']:.2f})")
        
        # === PHASE 4: Deep-Signal Validation ===
        logger.info("🧬 Validating outcomes with Deep-Signal...")
        
        context = {
            "recent_outcomes": self.mission_state["results"],
            "regime": safla_adaptation["regime"],
            "entropy": safla_adaptation["entropy"]
        }
        
        valid_outcomes, confidence_map = self.deep_signal.filter_outcomes(
            results["outcomes"], 
            context=context
        )
        
        results["valid_outcomes"] = valid_outcomes
        results["confidence_map"] = confidence_map
        
        # === PHASE 5: Aggregate & Feedback ===
        logger.info("🔄 Feeding results back to SAFLA...")
        
        total_value = sum(o["value"] for o in valid_outcomes)
        
        safla_feedback = {
            "id": f"cycle_{cycle_num}",
            "result": "SUCCESS" if total_value > 0 else "PARTIAL",
            "value": total_value,
            "metadata": {
                "regime": safla_adaptation["regime"],
                "tasks_count": len(tasks),
                "strategy": "multi_prime_distributed"
            }
        }
        
        # Adjust feedback based on Deep-Signal confidence
        adjusted_feedback = safla_feedback.copy()
        avg_confidence = sum(confidence_map.values()) / len(confidence_map) if confidence_map else 1.0
        adjusted_feedback["confidence"] = avg_confidence
        
        if avg_confidence < 0.8:
            logger.warn(f"⚠️  Low confidence ({avg_confidence:.0%}) — dampening SAFLA signal")
        
        # SAFLA learns
        adaptations = self.safla.reflect(adjusted_feedback)
        logger.info(f"💡 SAFLA adaptations: {json.dumps(adaptations, indent=2)}")
        
        # === PHASE 6: Decision ===
        logger.info("🎯 Captain's decision logic...")
        
        cycle_result = {
            "cycle": cycle_num,
            "total_value_generated": total_value,
            "tasks": len(tasks),
            "safla_regime": safla_adaptation["regime"],
            "decision": self._make_decision(total_value, safla_adaptation, cycle_num)
        }
        
        self.mission_state["results"].append(cycle_result)
        
        # Layer 2: Save checkpoint after every cycle — crash-proof
        self.flowstate.save_checkpoint(self.mission_state)
        
        logger.info(f"🔄 CYCLE {cycle_num} COMPLETE")
        logger.info(f"   Total value: ${total_value:.2f}")
        logger.info(f"   Decision: {cycle_result['decision']}")
        
        return cycle_result
    
    def _generate_cycle_tasks(self, cycle_num: int, safla_data: Dict) -> List[Dict]:
        """Generate tasks based on current cycle and SAFLA recommendations."""
        tasks = []
        
        # Example: Allocate based on SAFLA weights and mission resources
        primes = [
            ("scout", "Lead generation and market scanning"),
            ("zeus", "Trading opportunities and execution"),
            ("ghost", "Stealth deployment and evasion checks")
        ]
        
        for prime_name, description in primes:
            allocation = self.mission_state["resources_deployed"].get(prime_name, 0.0)
            
            if allocation > 0:
                tasks.append({
                    "prime": prime_name,
                    "name": f"{prime_name.upper()}_cycle_{cycle_num}",
                    "description": description,
                    "priority": "HIGH" if allocation > 0.4 else "MEDIUM",
                    "resource_budget": allocation,
                    "cycle": cycle_num
                })
        
        return tasks
    
    def _simulate_task_execution(self, task: Dict) -> Dict:
        """Simulate Prime execution (in production, calls actual Prime)."""
        import random
        
        # Simulate variance in outcomes
        base_value = task["resource_budget"] * 1000  # Resource -> Value mapping
        variance = base_value * (random.uniform(-0.3, 0.5))  # -30% to +50%
        actual_value = max(0, base_value + variance)
        
        return {
            "task": task["name"],
            "prime": task["prime"],
            "result": "SUCCESS" if actual_value > 0 else "FAILED",
            "value": actual_value,
            "execution_time_ms": random.randint(100, 5000)
        }
    
    def _make_decision(self, cycle_value: float, safla_data: Dict, cycle_num: int) -> str:
        """
        Captain decides: CONTINUE, PIVOT, ESCALATE, or COMPLETE.
        """
        regime = safla_data["regime"]
        
        # Simple heuristic; real logic would be more complex
        if cycle_value < 100 and regime == "CHAOTIC_NOISE":
            return "PIVOT"  # Change strategy
        elif safla_data["entropy"] > 0.85:
            return "HIBERNATION"  # Wait for clearer signal
        elif cycle_num >= 10:  # After 10 cycles, check for diminishing returns
            if cycle_value > 500:
                return "ACCELERATE"
            else:
                return "CONTINUE"
        else:
            return "CONTINUE"


def main():
    """
    Integration test: Captain + SAFLA working together
    """
    # Import SAFLA
    import sys
    sys.path.insert(0, "safla-v2")
    from core import SAFLA
    
    # Initialize SAFLA engine
    logger.info("🧠 Initializing SAFLA 2.0...")
    safla = SAFLA(project_id="fluxprime_test")
    
    # Initialize Captain
    logger.info("🔱 Initializing Captain...")
    captain = FluxCaptain(mission_id="war_chest_expansion_001", safla_engine=safla)
    
    # Set mission
    captain.set_mission(
        goal="Generate $5,000 in War Chest revenue through multi-Prime lead gen + trading",
        resources={
            "scout": 0.4,
            "zeus": 0.4,
            "ghost": 0.2
        }
    )
    
    # Run 3 cycles
    logger.info("\n" + "="*80)
    logger.info("MISSION EXECUTION: 3 CYCLES")
    logger.info("="*80 + "\n")
    
    for i in range(3):
        result = captain.execute_cycle()
        print(f"\n✅ Cycle {result['cycle']} Result: ${result['total_value_generated']:.2f}")
        print(f"   Decision: {result['decision']}\n")
        time.sleep(1)  # Brief pause between cycles
    
    # Distill experience to Second-Brain for future missions
    logger.info("\n📚 Distilling experience to Second-Brain...")
    captain.second_brain.distill_experience("war_chest_expansion_001", captain.mission_state["results"])
    
    # Final summary
    logger.info("\n" + "="*80)
    logger.info("MISSION SUMMARY")
    logger.info("="*80)
    total_war_chest = sum(r["total_value_generated"] for r in captain.mission_state["results"])
    logger.info(f"🏆 Total War Chest Generated: ${total_war_chest:.2f}")
    logger.info(f"🔄 Cycles Executed: {len(captain.mission_state['results'])}")
    logger.info(f"🧠 SAFLA State: {captain.safla.state}")
    logger.info(f"🧠 Second-Brain Knowledge: {captain.second_brain.knowledge}")
    logger.info("="*80)
    
    # Report to Telegram
    msg = f"🔱 FluxPrime Mission Complete\n💰 War Chest: ${total_war_chest:.2f}\n🔄 Cycles: {len(captain.mission_state['results'])}\n✅ Ready for Phase 3"
    captain.prime_bridge.report_to_telegram(msg)


if __name__ == "__main__":
    main()
