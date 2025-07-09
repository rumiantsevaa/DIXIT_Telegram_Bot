import os
import subprocess
import time

# Install requirements (once and initial)
def install_requirements():
    req_path = os.path.join(os.getcwd(), "requirements.txt")
    if os.path.isfile(req_path):
        print("[*] Installing dependecies...")
        subprocess.call("pip3 install -r requirements.txt", shell=True)
    else:
        print("[!] requirements.txt was not found")

def run_bot_loop():
    while True:
        print("[*] Starting main.py...")
        try:
            result = subprocess.run("python3 main.py", shell=True)
            print(f"[!] main.py stopped: {result.returncode}")
        except Exception as e:
            print(f"[!] Error: {e}")
        
        print("[*] Restart in 5secs...\n")
        time.sleep(5)

if __name__ == "__main__":
    install_requirements()
    run_bot_loop()
