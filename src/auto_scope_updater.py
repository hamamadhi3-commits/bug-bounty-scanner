#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
♻️ Auto Scope Updater – Digital Sentinel v5.0
Keeps target scopes refreshed every 6 hours.
"""

import os
import time
import subprocess

LOG_FILE = "logs/auto_updater.log"
os.makedirs("logs", exist_ok=True)

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(msg)

def main():
    log("🔁 Running auto scope updater...")
    try:
        subprocess.run(["python3", "src/scope_fetcher.py"], check=True)
        log("✅ Scope updated successfully.")
    except Exception as e:
        log(f"❌ Scope update failed: {e}")

if __name__ == "__main__":
    main()
