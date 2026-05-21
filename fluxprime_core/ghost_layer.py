"""
GhostPrime Layer 5 — Stealth & Evasion
Wraps any task execution in stealth protocols.
Delays, randomizes patterns, rotates identities.
"""

import random
import time
import logging
from typing import Dict, Any, Callable

logging.basicConfig(level=logging.INFO, format='[Ghost-Layer] %(message)s')
logger = logging.getLogger("Ghost-Layer")

class GhostLayer:
    """
    Layer 5 — The Mist.
    Every task that passes through GhostLayer is obfuscated:
    - Randomized execution timing
    - Shuffled execution order within priority bands
    - Identity rotation hooks (for real execution)
    - Pattern-break injection (avoid fingerprinting)
    """
    
    def __init__(self):
        self.cycles_since_break = 0
        self.break_interval = random.randint(3, 7) # Inject a break every 3-7 cycles
        logger.info("🌫️  Ghost Layer initialized — Stealth Mode ACTIVE")

    def apply_stealth(self, tasks: list, cycle_num: int) -> list:
        """
        Applies stealth protocols to the task list before execution.
        """
        
        logger.info(f"🌫️  Applying stealth to {len(tasks)} tasks...")
        
        # 1. Inject random delay per task
        for task in tasks:
            delay = round(random.uniform(0.5, 3.0), 2)
            task["ghost_delay"] = delay
            logger.info(f"   ⏱️  {task['name']}: {delay}s stealth delay")
        
        # 2. Pattern-break: shuffle low-priority tasks slightly
        # (High-priority tasks maintain order, lower ones are shuffled)
        if len(tasks) > 2:
            top_task = tasks[0]  # Protect the #1 priority
            rest = tasks[1:]
            random.shuffle(rest)
            tasks = [top_task] + rest
            logger.info("   🔀 Pattern-break: execution order shuffled (protecting P1)")
        
        # 3. Inject a "ghost pause" every N cycles
        self.cycles_since_break += 1
        if self.cycles_since_break >= self.break_interval:
            pause = round(random.uniform(5.0, 15.0), 2)
            logger.info(f"   💤 Ghost pause triggered: {pause}s (pattern evasion)")
            self.cycles_since_break = 0
            self.break_interval = random.randint(3, 7)
        
        return tasks

    def wrap_execution(self, task: Dict, executor: Callable) -> Dict:
        """
        Wraps a task execution with stealth delay and error handling.
        """
        delay = task.get("ghost_delay", 0)
        if delay > 0:
            time.sleep(delay)  # In real deployment — in tests, this is fast

        try:
            result = executor(task)
            logger.info(f"   👻 {task['name']}: executed under Ghost cover")
            return result
        except Exception as e:
            logger.error(f"   Ghost execution error on {task['name']}: {e}")
            return {"task": task["name"], "result": "FAILED", "value": 0, "prime": task.get("prime")}
