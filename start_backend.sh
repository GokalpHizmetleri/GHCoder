#!/bin/bash
# Start the FastAPI backend

echo "Starting AnyCoder FastAPI Backend..."
echo "API will be available at: http://localhost:8000"
echo "API docs at: http://localhost:8000/docs"
echo ""

# Check if OPENCODE_ZEN_API_KEY is set
if [ -z "$OPENCODE_ZEN_API_KEY" ]; then
    echo "⚠️  WARNING: OPENCODE_ZEN_API_KEY environment variable is not set!"
    echo "Please set it with: export OPENCODE_ZEN_API_KEY=your_zen_api_key_here"
    echo ""
fi

# Activate virtual environment
source /Users/ahsenkhaliq/anycoder/.venv/bin/activate

# Start the backend
python backend_api.py

