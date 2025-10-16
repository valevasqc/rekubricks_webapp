#!/bin/bash
# Quick start script for Webscraper V2
# Run from project root: bash webscraping/quick_start.sh

echo "=================================="
echo "RekuBricks Webscraper V2"
echo "=================================="
echo ""

# Get Python executable
PYTHON="/Users/valevasqc/Library/CloudStorage/OneDrive-UniversidadFranciscoMarroquin/30 UFM/Trabajos/Semestre 6/SI105. Taller de Ingeniería II/rekubricks_webapp/.venv/bin/python"

# Step 1: Run tests
echo "Step 1: Running tests..."
cd webscraping
$PYTHON test_scraper.py
TEST_RESULT=$?

if [ $TEST_RESULT -ne 0 ]; then
    echo ""
    echo "❌ Tests failed. Please fix errors before running full scraper."
    exit 1
fi

echo ""
echo "✅ Tests passed!"
echo ""
read -p "Continue with full scraper? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Step 2: Running full webscraper..."
    echo "⏱️  This will take approximately 30-40 minutes..."
    echo ""
    $PYTHON webscraping_v2.py
    
    echo ""
    echo "✅ Done! Check data/bricklink_pieces.xlsx"
else
    echo "Cancelled."
    exit 0
fi
