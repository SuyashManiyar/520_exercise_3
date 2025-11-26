#!/bin/bash
# Simple script to run the coverage analysis

echo "=================================="
echo "Running Coverage Analysis"
echo "=================================="
echo ""

# Check if dependencies are installed
if ! python3 -c "import pytest" 2>/dev/null; then
    echo "⚠️  Dependencies not installed. Installing..."
    pip install -r requirements.txt
    echo ""
fi

# Run the analysis
echo "Running demo_humaneval_clean.py..."
echo ""
python3 demo_humaneval_clean.py

echo ""
echo "=================================="
echo "✅ Analysis Complete!"
echo "=================================="
