#!/bin/bash
# Quick launcher for FluxPrime Phase 3

MODE="${1:-sim}"

if [ "$MODE" = "real" ] || [ "$MODE" = "prod" ]; then
  echo "🔱 ACTIVATING REAL EXECUTION..."
  bash fluxprime_core/activate_real_execution.sh
else
  echo "🧪 RUNNING SIMULATION..."
  python3 fluxprime_core/flux_captain.py
fi
