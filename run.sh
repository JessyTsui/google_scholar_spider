#!/bin/bash

echo "🚀 Starting Google Scholar Spider..."

# Kill any existing processes
pkill -f "uvicorn.*8001" 2>/dev/null
pkill -f "vite.*3000" 2>/dev/null

# Create directories
mkdir -p data logs

echo "📦 Starting backend..."
cd backend
python run.py > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
cd ..

echo "⏳ Waiting for backend to start..."
sleep 3

# Check if backend is running
if curl -s http://localhost:8001/api/health > /dev/null; then
    echo "✅ Backend is running"
else
    echo "❌ Backend failed to start"
    exit 1
fi

echo "🎨 Starting frontend..."
cd frontend
npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo "⏳ Waiting for frontend to start..."
sleep 5

echo ""
echo "✨ Services started!"
echo "🌐 Frontend: http://localhost:3000"
echo "📡 Backend:  http://localhost:8001"
echo "📚 API Docs: http://localhost:8001/docs"
echo ""
echo "📝 Logs:"
echo "   Backend: logs/backend.log"
echo "   Frontend: logs/frontend.log"
echo ""
echo "To stop services:"
echo "   kill $BACKEND_PID $FRONTEND_PID"