#!/bin/bash

echo "🛑 Stopping Google Scholar Spider services..."

# Kill processes by port
echo "Stopping backend (port 8001)..."
pkill -f "uvicorn.*8001" 2>/dev/null
lsof -ti :8001 | xargs kill 2>/dev/null

echo "Stopping frontend (port 3000)..."
pkill -f "vite.*3000" 2>/dev/null
lsof -ti :3000 | xargs kill 2>/dev/null

# Kill any remaining node processes for this project
pkill -f "node.*vite" 2>/dev/null

echo "✅ Services stopped"