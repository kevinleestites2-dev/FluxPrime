#!/bin/bash
#
# Activate Real Pantheon Prime Execution
# Phase 3 → Production
#

set -e

echo "╔════════════════════════════════════════════════════════════════════════════════╗"
echo "║                  FLUXPRIME PHASE 3 REAL EXECUTION ACTIVATION                   ║"
echo "╚════════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check prerequisites
echo "🔍 Checking prerequisites..."

if [ ! -f "fluxprime_core/flux_captain.py" ]; then
    echo "❌ flux_captain.py not found. Are you in the right directory?"
    exit 1
fi

if [ ! -f "fluxprime_core/prime_bridge.py" ]; then
    echo "❌ prime_bridge.py not found. Phase 3 files missing."
    exit 1
fi

# Check environment
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "⚠️  TELEGRAM_BOT_TOKEN not set. Using default (may fail)."
    export TELEGRAM_BOT_TOKEN="8679655550:AAGUB1m5fmqHc8OHqqM24Vixz8FfwX-gqD4"
fi

if [ -z "$TELEGRAM_CHAT_ID" ]; then
    echo "⚠️  TELEGRAM_CHAT_ID not set. Using default (may fail)."
    export TELEGRAM_CHAT_ID="7135054241"
fi

echo "✅ Prerequisites OK"
echo ""

# Confirm before activating
echo "⚠️  REAL EXECUTION MODE ACTIVATION"
echo ""
echo "This will connect to:"
echo "  • Scout Prime (via Nexus Relay → Phone)"
echo "  • Zeus Prime (via Nexus Relay → Phone)"
echo "  • Ghost Prime (CloakPrime swarm)"
echo ""
echo "The Pantheon will start earning real revenue."
echo ""
read -p "Type 'ACTIVATE' to proceed: " confirm

if [ "$confirm" != "ACTIVATE" ]; then
    echo "❌ Activation cancelled."
    exit 1
fi

echo ""
echo "🔱 ACTIVATING REAL EXECUTION..."
echo ""

export USE_REAL_PRIMES="true"

# Run captain in background with logging
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="fluxprime_core/logs/real_execution_${TIMESTAMP}.log"

mkdir -p fluxprime_core/logs

echo "📝 Logging to: $LOG_FILE"
echo ""

python3 fluxprime_core/flux_captain.py 2>&1 | tee "$LOG_FILE"

echo ""
echo "🏆 MISSION COMPLETE"
echo "📊 Check $LOG_FILE for full results"
echo ""
