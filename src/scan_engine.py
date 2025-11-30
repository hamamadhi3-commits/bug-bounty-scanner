#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ Digital Sentinel PRIME v4.2 – Deep Mode Worker
Self-logging, resilient, auto-recovery scanning engine for authorized Bugcrowd targets.
"""

import os
import sys
import time
import traceback
import requests
from datetime import datetime

# ========== Configuration ==========
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK_URL")
TARGET_FILE = "targets/bugcrowd_203.txt"  # Main target list
LOG_DIR = "logs"
ERROR_LOG = os.path.join(LOG_DIR, "errors.log")
MAIN_LOG = os.path.join(LOG_DIR, f"worker_{int(time.time())}.log")

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)


# ========== Logging ==========
def log(msg: str):
    """Write message to log file and stdout."""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(MAIN_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def log_error(msg: str):
    """Record critical error message."""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    err_line = f"[{timestamp}] ❌ ERROR: {msg}"
    with open(ERROR_LOG, "a", encoding="utf-8") as ef:
        ef.write(err_line + "\n")
    log(err_line)


def send_discord(msg: str):
    """Send notification to Discord channel."""
    if not DISCORD_WEBHOOK:
        log("⚠️ Discord webhook not set; skipping send.")
        return
    try:
        payload = {"content": msg}
        requests.post(DISCORD_WEBHOOK, json=payload, timeout=10)
    except Exception as e:
        log_error(f"Failed to send Discord message: {e}")


# ========== Scanning Logic ==========
def scan_target(target: str):
    """Simulated target scanning process (replace with real scanner)."""
    log(f"🧠 Scanning target: {target}")
    time.sleep(0.8)  # Simulate scan duration

    # Simulated errors for certain targets
    if "staging" in target or "dev" in target:
        raise RuntimeError(f"{target} seems unreachable or rate-limited.")

    log(f"✅ Scan completed successfully: {target}")


# ========== Main Worker Routine ==========
def main():
    log("🚀 Starting Deep Sentinel Worker Engine...")

    # Check target list existence
    if not os.path.exists(TARGET_FILE):
        log_error("Target list not found!")
        send_discord("⚠️ No target list found for Worker Sentinel.")
        sys.exit(1)

    # Read targets
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        targets = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    if not targets:
        log_error("Target list is empty — skipping scan.")
        send_discord("⚠️ Worker Sentinel found no targets to scan.")
        sys.exit(0)

    total = len(targets)
    log(f"🔎 Loaded {total} targets from {TARGET_FILE}")

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
            with open(ERROR_LOG, "a", encoding="utf-8") as ef:
                traceback.print_exc(file=ef)

    summary = f"✅ Success: {success} | ❌ Failed: {fail} | Total: {total}"
    log(summary)

    if fail > 0:
        send_discord(f"⚠️ Worker Sentinel finished with errors:\n```\n{summary}\n```")
    else:
        send_discord(f"✅ Worker Sentinel finished successfully.\n```\n{summary}\n```")


if __name__ == "__main__":
    try:
        main()
    except Exception as main_err:
        log_error(f"🔥 Fatal engine error: {main_err}")
        send_discord(f"🔥 Fatal error in Worker Sentinel:\n```\n{main_err}\n```")
        sys.exit(1)
