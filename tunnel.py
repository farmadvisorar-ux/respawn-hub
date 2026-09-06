import os
import sys
import subprocess
import urllib.request
import re
import time

CLOUDFLARED_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cloudflared.exe")

def ensure_cloudflared():
    if os.path.exists(CLOUDFLARED_PATH):
        return True
    
    print("[TUNNEL] Downloading official Cloudflare Tunnel client (zero config)...")
    url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
    try:
        urllib.request.urlretrieve(url, CLOUDFLARED_PATH)
        print("[TUNNEL] Cloudflare Tunnel binary downloaded successfully.")
        return True
    except Exception as e:
        print(f"[TUNNEL] Could not download cloudflared: {e}")
        return False

def start_tunnel():
    print("=" * 60)
    print(">>> DEPLOYING RESPAWN // SQUADFINDER LIVE ON PUBLIC HTTPS URL")
    print("=" * 60)

    if ensure_cloudflared():
        print("[TUNNEL] Initiating Cloudflare Quick Tunnel on port 8000...")
        cmd = [CLOUDFLARED_PATH, "tunnel", "--url", "http://127.0.0.1:8000"]
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        public_url = None
        start_time = time.time()

        for line in proc.stdout:
            # Look for *.trycloudflare.com URL
            match = re.search(r'(https://[a-zA-Z0-9-]+\.trycloudflare\.com)', line)
            if match:
                public_url = match.group(1)
                break
            if time.time() - start_time > 30:
                break

        if public_url:
            print("\n" + "=" * 60)
            print(">>> YOUR APP IS LIVE PUBLICLY ON THE INTERNET! <<<")
            print(f">>> LIVE HTTPS URL: {public_url}")
            print("=" * 60 + "\n")
            print("Share this link with your squadmates anywhere in the world!")
            print("Press Ctrl+C to stop the tunnel.\n")
            
            # Save the live URL to a file
            with open("LIVE_URL.txt", "w") as f:
                f.write(public_url + "\n")

            try:
                proc.wait()
            except KeyboardInterrupt:
                proc.terminate()
                print("\n[TUNNEL] Tunnel stopped.")
            return

    # Fallback to SSH tunnel via localhost.run / pinggy if cloudflared fails
    print("[TUNNEL] Trying alternative SSH tunnel...")
    ssh_cmd = ["ssh", "-o", "StrictHostKeyChecking=no", "-R", "80:localhost:8000", "nokey@localhost.run"]
    subprocess.run(ssh_cmd)

if __name__ == "__main__":
    start_tunnel()
