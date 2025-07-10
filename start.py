#!/usr/bin/env python3
"""
Google Scholar Spider - Main Launcher
Supports simultaneous frontend and backend startup
"""
import os
import sys
import subprocess
import time
import signal
import platform
from pathlib import Path

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

class GoogleScholarSpiderLauncher:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.backend_dir = self.root_dir / "backend"
        self.frontend_dir = self.root_dir / "frontend"
        self.processes = []
        
    def print_banner(self):
        """Print application banner"""
        print(f"{Colors.CYAN}{Colors.BOLD}")
        print("=" * 60)
        print("  Google Scholar Spider 2.0")
        print("  学术文献搜索分析系统 | Academic Literature Search System")
        print("  学術文献検索分析システム")
        print("=" * 60)
        print(f"{Colors.END}")
        
    def check_requirements(self):
        """Check if all requirements are met"""
        print(f"{Colors.YELLOW}🔍 Checking requirements...{Colors.END}")
        
        # Check Python version
        if sys.version_info < (3, 8):
            print(f"{Colors.RED}❌ Python 3.8+ is required{Colors.END}")
            return False
            
        # Check if backend requirements are installed
        try:
            import fastapi
            import uvicorn
            print(f"{Colors.GREEN}✅ Backend dependencies OK{Colors.END}")
        except ImportError:
            print(f"{Colors.RED}❌ Backend dependencies not installed{Colors.END}")
            print(f"   Run: cd backend && pip install -r requirements.txt")
            return False
            
        # Check if frontend dependencies are installed
        if not (self.frontend_dir / "node_modules").exists():
            print(f"{Colors.RED}❌ Frontend dependencies not installed{Colors.END}")
            print(f"   Run: cd frontend && npm install")
            return False
        else:
            print(f"{Colors.GREEN}✅ Frontend dependencies OK{Colors.END}")
            
        return True
        
    def kill_existing_processes(self):
        """Kill any existing processes on our ports"""
        print(f"{Colors.YELLOW}🧹 Cleaning up existing processes...{Colors.END}")
        
        if platform.system() != "Windows":
            # Kill processes on port 8001 (backend)
            subprocess.run("lsof -ti :8001 | xargs kill -9 2>/dev/null", shell=True)
            # Kill processes on port 3000 (frontend)
            subprocess.run("lsof -ti :3000 | xargs kill -9 2>/dev/null", shell=True)
        else:
            # Windows commands
            subprocess.run("netstat -ano | findstr :8001", shell=True)
            subprocess.run("netstat -ano | findstr :3000", shell=True)
            
    def start_backend(self):
        """Start the backend server"""
        print(f"{Colors.BLUE}🚀 Starting backend server...{Colors.END}")
        
        # Create logs directory
        logs_dir = self.root_dir / "logs"
        logs_dir.mkdir(exist_ok=True)
        
        # Start backend
        backend_log = open(logs_dir / "backend.log", "w")
        backend_proc = subprocess.Popen(
            [sys.executable, "run.py"],
            cwd=self.backend_dir,
            stdout=backend_log,
            stderr=backend_log
        )
        self.processes.append(backend_proc)
        
        # Wait for backend to start
        time.sleep(3)
        
        # Check if backend is running
        try:
            import requests
            response = requests.get("http://localhost:8001/api/health")
            if response.status_code == 200:
                print(f"{Colors.GREEN}✅ Backend started successfully{Colors.END}")
                return True
        except:
            pass
            
        print(f"{Colors.RED}❌ Backend failed to start{Colors.END}")
        return False
        
    def start_frontend(self):
        """Start the frontend server"""
        print(f"{Colors.BLUE}🚀 Starting frontend server...{Colors.END}")
        
        # Create logs directory
        logs_dir = self.root_dir / "logs"
        logs_dir.mkdir(exist_ok=True)
        
        # Start frontend
        frontend_log = open(logs_dir / "frontend.log", "w")
        frontend_proc = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=self.frontend_dir,
            stdout=frontend_log,
            stderr=frontend_log
        )
        self.processes.append(frontend_proc)
        
        # Wait for frontend to start
        time.sleep(5)
        
        print(f"{Colors.GREEN}✅ Frontend started{Colors.END}")
        return True
        
    def print_access_info(self):
        """Print access information"""
        print(f"\n{Colors.CYAN}{'=' * 60}{Colors.END}")
        print(f"{Colors.GREEN}{Colors.BOLD}✨ Google Scholar Spider is running!{Colors.END}")
        print(f"\n{Colors.BOLD}Access URLs:{Colors.END}")
        print(f"  🌐 Frontend:   {Colors.CYAN}http://localhost:3000{Colors.END}")
        print(f"  📡 Backend:    {Colors.CYAN}http://localhost:8001{Colors.END}")
        print(f"  📚 API Docs:   {Colors.CYAN}http://localhost:8001/docs{Colors.END}")
        print(f"\n{Colors.BOLD}Log Files:{Colors.END}")
        print(f"  📝 Backend:    logs/backend.log")
        print(f"  📝 Frontend:   logs/frontend.log")
        print(f"\n{Colors.YELLOW}Press Ctrl+C to stop all services{Colors.END}")
        print(f"{Colors.CYAN}{'=' * 60}{Colors.END}\n")
        
    def cleanup(self):
        """Cleanup function to stop all processes"""
        print(f"\n{Colors.YELLOW}🛑 Stopping services...{Colors.END}")
        for proc in self.processes:
            proc.terminate()
        time.sleep(1)
        for proc in self.processes:
            proc.kill()
        print(f"{Colors.GREEN}✅ All services stopped{Colors.END}")
        
    def run(self):
        """Main run function"""
        self.print_banner()
        
        # Check requirements
        if not self.check_requirements():
            sys.exit(1)
            
        # Kill existing processes
        self.kill_existing_processes()
        
        # Start services
        if not self.start_backend():
            self.cleanup()
            sys.exit(1)
            
        if not self.start_frontend():
            self.cleanup()
            sys.exit(1)
            
        # Print access info
        self.print_access_info()
        
        # Setup signal handler
        def signal_handler(sig, frame):
            self.cleanup()
            sys.exit(0)
            
        signal.signal(signal.SIGINT, signal_handler)
        
        # Keep running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.cleanup()


if __name__ == "__main__":
    launcher = GoogleScholarSpiderLauncher()
    launcher.run()