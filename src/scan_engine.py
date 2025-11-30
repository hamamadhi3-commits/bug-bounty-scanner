#!/usr/bin/env python3
# ==============================================================
#  🚀 Digital Sentinel – Deep Mode Worker Engine v4.2 (Stable)
#  Author: hamamadhi3
#  Description:
#   Runs Deep Scan tasks on authorized Bugcrowd targets.
#   Includes absolute-path patch for GitHub Actions.
# ==============================================================

import os
import sys
import time
import requests

# ==============================================================
#  PATH CONFIGURATION (FIXED for GitHub Actions)
# ==============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TARGET_FILE = os.path.join(BASE_DIR, "..", "bug-bounty-scanner", "targets", "bugcrowd_203.txt")

# ==============================================================
#  DISCORD NOTIFY (Optional)
# ==============================================================

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK_URL", None)

def notify_discord(message: str):
    """Send message to Discord if webhook exists."""
    if not DISCORD_WEBHOOK:
        print("⚠️ Discord webhook not set; skipping send.")
        return
    try:
        requests.post(DISCORD_WEBHOOK, json={"content": message}, timeout=10)
    except Exception as e:
        print(f"⚠️ Discord send failed: {e}")

# ==============================================================
#  MAIN SCAN LOGIC
# ==============================================================

def load_targets():
    """Load targets safely, raise clear error if missing."""
    if not os.path.exists(TARGET_FILE):
        print(f"❌ ERROR: Target list not found at {TARGET_FILE}")
        sys.exit(1)

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        targets = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    if not targets:
        print("❌ ERROR: Target list file is empty!")
        sys.exit(1)

    print(f"✅ Loaded {len(targets)} authorized targets.")
    return targets

def scan_target(target):
    """Simulated scan process for target (extendable)."""
    print(f"🔎 Scanning: {target}")
    time.sleep(0.3)  # simulate scan delay
    result = {"target": target, "status": "OK"}
    return result

def run_worker():
    """Run the Deep Sentinel Worker Scan Engine."""
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 🚀 Starting Deep Sentinel Worker Engine...")

    targets = load_targets()
    print(f"🧠 Initiating deep scan across {len(targets)} Bugcrowd targets...\n")

    notify_discord("🧠 Deep Sentinel Worker Engine Started.")

    results = []
    success = 0

    for idx, target in enumerate(targets, start=1):
        try:
            res = scan_target(target)
            results.append(res)
            success += 1
            print(f"✅ [{idx}/{len(targets)}] Done: {target}")
        except Exception as e:
            print(f"❌ [{idx}/{len(targets)}] Failed: {target} ({e})")

    print("\n🧩 Summary Report")
    print("--------------------------------------------------")
    print(f"🟢 Total Scanned: {len(targets)}")
    print(f"✅ Success: {success}")
    print(f"🔴 Failed: {len(targets) - success}")
    print("--------------------------------------------------")

    notify_discord(f"✅ Deep Sentinel Worker finished.\n🟢 Scanned: {len(targets)} | ✅ Success: {success}")

# ==============================================================
#  ENTRY POINT
# ==============================================================

if __name__ == "__main__":
    try:
        run_worker()
        sys.exit(0)
    except KeyboardInterrupt:
        print("🛑 Interrupted by user.")
        notify_discord("🛑 Sentinel Worker Interrupted.")
        sys.exit(1)
    except Exception as e:
        print(f"💀 Fatal Error: {e}")
        notify_discord(f"💀 Fatal Error: {e}")
        sys.exit(1)
