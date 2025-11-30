#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ Digital Sentinel PRIME v4.1 – Deep Mode Worker
Self-logging, self-recovery scan engine.
"""

import os
import sys
import time
import traceback
import requests
from datetime import datetime

# ====== CONFIGURATION ======
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK_URL")

# 🔧 FIXED: file now correctly points to main project root
TARGET_FILE = "bug_bounty_targets.txt"

LOG_DIR = "logs"
ERROR_LOG = os.path.join(LOG_DIR, "errors.log")
MAIN_LOG = os.path.join(LOG_DIR, f"worker_{int(time.time())}.log")

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# ====== LOGGING UTILITIES ======
def log(msg):
    """Write message to log file and stdout."""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(MAIN_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def log_error(msg):
    """Record critical error message."""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    err_line = f"[{timestamp}] ❌ ERROR: {msg}"
    with open(ERROR_LOG, "a", encoding="utf-8") as ef:
        ef.write(err_line + "\n")
    log(err_line)

def send_discord(msg):
    """Send notification to Discord."""
    if not DISCORD_WEBHOOK:
        log("⚠️ Discord webhook not set; skipping send.")
        return
    try:
        payload = {"content": msg}
        requests.post(DISCORD_WEBHOOK, json=payload, timeout=10)
    except Exception as e:
        log_error(f"Failed to send Discord message: {e}")

# ====== SCAN ENGINE ======
def scan_target(target):
    """Dummy scan logic placeholder (replace with real scanner)."""
    log(f"🧠 Scanning target: {target}")
    time.sleep(1.2)  # simulate scan delay
    # simulate random failure
    if "dev" in target or "staging" in target:
        raise RuntimeError(f"Target {target} seems unreachable or rate-limited.")
    log(f"✅ Scan completed: {target}")

# ====== MAIN EXECUTION ======
def main():
    log("🚀 Starting Deep Worker Sentinel Scan Engine...")

    if not os.path.exists(TARGET_FILE):
        log_error("Target list not found!")
        send_discord("⚠️ No target list found for Worker Sentinel.")
        sys.exit(1)

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        targets = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    if not targets:
        log_error("Target list is empty — skipping scan.")
        send_discord("⚠️ Worker Sentinel found no targets to scan.")
        sys.exit(0)

    total = len(targets)
    log(f"🔎 Loaded {total} targets.")

    success = 0
    fail = 0

    for idx, target in enumerate(targets, 1):
        try:
            log(f"▶️ [{idx}/{total}] Processing {target}")
            scan_target(target)
            success += 1
        except Exception as e:
            fail += 1
            log_error(f"Scan failed for {target}: {e}")
            traceback.print_exc(file=open(ERROR_LOG, "a", encoding="utf-8"))

    summary = f"✅ Success: {success} | ❌ Failed: {fail} | Total: {total}"
    log(summary)

    if fail > 0:
        send_discord(f"⚠️ Worker Sentinel finished with errors:\n```\n{summary}\n```")
    else:
        send_discord(f"✅ Worker Sentinel finished successfully.\n```\n{summary}\n```")

# ====== ENTRY POINT ======
if __name__ == "__main__":
    try:
        main()
    except Exception as main_err:
        log_error(f"Fatal engine error: {main_err}")
        send_discord(f"🔥 Fatal error in Worker Sentinel:\n```\n{main_err}\n```")
        sys.exit(1)
