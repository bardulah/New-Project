#!/bin/bash

# PsycheEdge 2025 Quick Start Script

echo "🧠 PsycheEdge 2025 - Quick Start"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.10+."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your API tokens (optional)"
fi

echo ""
echo "🚀 Choose how to run PsycheEdge:"
echo ""
echo "1) Run Streamlit UI (recommended)"
echo "2) Run CLI swarm simulation"
echo "3) Run Telegram bot"
echo "4) Docker Compose (all services)"
echo ""
read -p "Enter choice [1-4]: " choice

case $choice in
    1)
        echo ""
        echo "🎨 Starting Streamlit UI..."
        echo "Access at: http://localhost:8501"
        echo ""
        streamlit run psyche_edge/ui/streamlit_app.py
        ;;
    2)
        echo ""
        echo "🧬 Starting swarm simulation..."
        python main.py --population 40 --inject-test-data
        ;;
    3)
        echo ""
        echo "🤖 Starting Telegram bot..."
        python psyche_edge/integrations/telegram_bot.py
        ;;
    4)
        echo ""
        echo "🐳 Starting Docker Compose..."
        docker-compose up
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac
