import subprocess
import time
import os
import webbrowser
import sys

def run_demo():
    print("--- TalentIQ One-Click Demo Loader ---")
    
    # 1. Set environment
    os.environ["PYTHONPATH"] = os.getcwd()
    
    # Load .env explicitly to ensure backend sees the correct values
    from dotenv import load_dotenv
    load_dotenv(override=True)
    
    groq_key = os.getenv("GROQ_API_KEY")
    mock_parser = os.getenv("USE_MOCK_PARSER", "False" if groq_key else "True")
    print(f"DEBUG (run_demo): USE_MOCK_PARSER is set to {mock_parser}")
    os.environ["USE_MOCK_PARSER"] = mock_parser
    
    # 2. Start Backend (Port 8000)
    print("Starting TalentIQ Backend Agents...")
    backend = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"],
        env=os.environ
    )
    
    # 3. Start Frontend (Port 3001)
    print("Starting TalentIQ Frontend Dashboard...")
    frontend = subprocess.Popen(
        [sys.executable, "-m", "http.server", "3001"],
        cwd=os.path.join(os.getcwd(), "frontend", "public"),
        stdout=subprocess.DEVNULL
    )
    
    # 4. Wait for initialization
    time.sleep(5)
    
    # 5. Open Browser
    url = "http://localhost:3001"
    print(f"\n✅ SYSTEM READY! Opening {url} in your browser...")
    webbrowser.open(url)
    
    print("\nKeep this terminal open during your demo.")
    print("Press Ctrl+C to stop the servers.")
    
    try:
        backend.wait()
        frontend.wait()
    except KeyboardInterrupt:
        print("\nStopping TalentIQ services...")
        backend.terminate()
        frontend.terminate()

if __name__ == "__main__":
    run_demo()
