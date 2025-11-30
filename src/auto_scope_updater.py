#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
♻️ Auto Scope Updater – Digital Sentinel v5.0
Keeps Bugcrowd scopes fresh on every cycle.
"""

import os, time, subprocess

LOG_FILE = "logs/auto_scope_updater.log"
os.makedirs("logs", exist_ok=True)

def log(msg):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    print(msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")

def main():
    log("🔁 Running Auto Scope Updater...")
    try:
        subprocess.run(["python3", "src/scope_fetcher.py"], check=True)
        log("✅ Scopes updated successfully.")
    except Exception as e:
        log(f"❌ Scope update failed: {e}")

if __name__ == "__main__":
    main()
