#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -i :$port >/dev/null 2>&1; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Function to kill processes on specific ports
kill_port() {
    local port=$1
    local pids=$(lsof -ti :$port)
    if [ ! -z "$pids" ]; then
        print_warning "Killing processes on port $port: $pids"
        kill $pids
        sleep 2
    fi
}

# Function to cleanup on exit
cleanup() {
    print_status "Shutting down services..."
    
    # Kill background processes
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
    fi
    
    # Kill any remaining processes on our ports
    kill_port 8001
    kill_port 3000
    
    print_status "Services stopped"
    exit 0
}

# Set up trap for cleanup on exit
trap cleanup SIGINT SIGTERM

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

print_status "🚀 Starting Google Scholar Spider Development Server"

# Clean up any existing processes
kill_port 8001
kill_port 3000

# Create data directory if it doesn't exist
mkdir -p data

# Start backend
print_status "📦 Starting backend server on port 8001..."
cd backend
nohup python run.py > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Check if backend is running
if ! check_port 8001; then
    print_error "Backend failed to start. Check logs/backend.log for details."
    exit 1
fi

print_status "✅ Backend started successfully (PID: $BACKEND_PID)"

# Test backend health
if curl -s http://localhost:8001/api/health > /dev/null; then
    print_status "✅ Backend health check passed"
else
    print_error "Backend health check failed"
    cleanup
    exit 1
fi

# Start frontend
print_status "🎨 Starting frontend server on port 3000..."
cd frontend
nohup npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
sleep 5

# Check if frontend is running
if ! check_port 3000; then
    print_error "Frontend failed to start. Check logs/frontend.log for details."
    cleanup
    exit 1
fi

print_status "✅ Frontend started successfully (PID: $FRONTEND_PID)"

# Display service information
echo ""
echo -e "${BLUE}✨ Google Scholar Spider is now running!${NC}"
echo ""
echo -e "${GREEN}🌐 Frontend:${NC} http://localhost:3000"
echo -e "${GREEN}📡 Backend:${NC}  http://localhost:8001"
echo -e "${GREEN}📚 API Docs:${NC} http://localhost:8001/docs"
echo ""
echo -e "${YELLOW}📝 Logs:${NC}"
echo -e "   Backend: logs/backend.log"
echo -e "   Frontend: logs/frontend.log"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"
echo ""

# Monitor services
while true; do
    # Check if backend is still running
    if ! check_port 8001; then
        print_error "Backend service stopped unexpectedly"
        cleanup
        exit 1
    fi
    
    # Check if frontend is still running
    if ! check_port 3000; then
        print_error "Frontend service stopped unexpectedly"
        cleanup
        exit 1
    fi
    
    sleep 5
done