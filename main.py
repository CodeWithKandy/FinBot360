import argparse
import os
import sys
import subprocess

def run_dashboard():
    print("Starting FinBot360 Dashboard...")
    dashboard_path = os.path.join("ui", "dashboard.py")
    subprocess.run([sys.executable, "-m", "streamlit", "run", dashboard_path])

def run_bot():
    print("Starting FinBot360 Telegram Bot...")
    from bot import run_bot as start_bot
    start_bot()

def main():
    parser = argparse.ArgumentParser(description="FinBot360 - Financial Assistant")
    parser.add_argument("--mode", choices=["dashboard", "bot"], required=True, help="Mode to run: 'dashboard' or 'bot'")
    
    args = parser.parse_args()
    
    if args.mode == "dashboard":
        run_dashboard()
    elif args.mode == "bot":
        run_bot()

if __name__ == "__main__":
    main()
