#!/bin/bash
set -e

# LiveKit Voice Agent Railway Entrypoint Script

echo "🎙️  Starting LiveKit Voice Agent..."

# Validate required environment variables
REQUIRED_VARS=(
    "LIVEKIT_URL"
    "LIVEKIT_API_KEY"
    "LIVEKIT_API_SECRET"
    "OPENAI_API_KEY"
)

echo "🔍 Checking required environment variables..."
for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ ERROR: $var is not set!"
        exit 1
    fi
    echo "   ✅ $var is set"
done

# Set optional variables with defaults
export ODOO_FRONTEND_URL="${ODOO_FRONTEND_URL:-http://localhost:8069}"
export LOG_LEVEL="${LOG_LEVEL:-INFO}"

echo ""
echo "📋 Configuration:"
echo "   LiveKit URL: $LIVEKIT_URL"
echo "   LiveKit API Key: ${LIVEKIT_API_KEY:0:10}..."
echo "   OpenAI API Key: ${OPENAI_API_KEY:0:10}..."
echo "   Odoo Frontend: $ODOO_FRONTEND_URL"
echo "   Log Level: $LOG_LEVEL"
echo ""

# Health check endpoint (simple HTTP server for Railway)
# This allows Railway to monitor the agent's health
if [ "$ENABLE_HEALTH_CHECK" = "true" ]; then
    echo "🏥 Starting health check endpoint on port 8080..."
    python -m http.server 8080 &
    HEALTH_PID=$!
    echo "   Health check PID: $HEALTH_PID"
fi

# Trap signals for graceful shutdown
trap 'echo "🛑 Received shutdown signal..."; [ -n "$HEALTH_PID" ] && kill $HEALTH_PID 2>/dev/null; exit 0' SIGTERM SIGINT

echo "🚀 Launching LiveKit agent..."
echo ""

# Execute the agent
exec "$@"
