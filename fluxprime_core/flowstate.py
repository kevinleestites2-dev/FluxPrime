"""
Flowstate — Layer 2 Persistence for FluxPrime
Ensures crash-proof continuity and mission checkpointing.
"""

import json
import os
import time
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[Flowstate] %(message)s')
logger = logging.getLogger("Flowstate")

class Flowstate:
    def __init__(self, mission_id: str, base_dir: str = "fluxprime_core/missions"):
        self.mission_id = mission_id
        self.checkpoint_dir = Path(base_dir) / mission_id
        self.checkpoint_path = self.checkpoint_dir / "flow_anchor.json"
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"🌊 Flowstate anchor established for: {mission_id}")

    def save_checkpoint(self, state: dict):
        """Saves the current mission state to disk."""
        try:
            checkpoint = {
                "mission_id": self.mission_id,
                "timestamp": time.time(),
                "state": state
            }
            with open(self.checkpoint_path, "w") as f:
                json.dump(checkpoint, f, indent=2)
            logger.info(f"📍 Checkpoint saved at cycle {state.get('cycle', 'unknown')}")
            return True
        except Exception as e:
            logger.error(f"Failed to save checkpoint: {e}")
            return False

    def recover(self) -> dict:
        """Loads the last saved checkpoint if it exists."""
        if not self.checkpoint_path.exists():
            logger.info("No checkpoint found. Starting fresh.")
            return None
        
        try:
            with open(self.checkpoint_path, "r") as f:
                checkpoint = json.load(f)
            logger.info(f"🔄 Recovered mission from {time.ctime(checkpoint['timestamp'])}")
            return checkpoint["state"]
        except Exception as e:
            logger.error(f"Recovery failed: {e}")
            return None

    def purge(self):
        """Deletes the checkpoint (mission complete or failed)."""
        if self.checkpoint_path.exists():
            self.checkpoint_path.unlink()
            logger.info("💀 Flowstate anchor purged.")
