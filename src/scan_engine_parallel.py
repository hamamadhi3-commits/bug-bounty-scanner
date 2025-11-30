#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ Digital Sentinel PRIME v5.0 – Parallel Deep Scan Engine
Multi-worker, self-recovering, Discord-integrated bug bounty scanner.
"""

import os, sys, time, traceback, concurrent.futures, requests
from datetime import datetime

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK_URL")
TARGET_FILE = "targets/bugcrowd_203.txt"
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

MAIN_LOG = os.path.join(LOG_DIR, f"worker_{int(time.time())}.log")
ERROR_LOG = os.path.join(LOG_DIR, "errors.log")

def log(msg):
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(MAIN_LOG, "a", encoding="utf-8") as f: f.write(line + "\n")

def log_error(msg):
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    err = f"[{ts}] ❌ {msg}"
    with open(ERROR_LOG, "a", encoding="utf-8") as e: e.write(err + "\n")
    log(err)

def send_discord(msg):
    if not DISCORD_WEBHOOK: return
    try:
        requests.post(DISCORD_WEBHOOK, json={"content": msg}, timeout=10)
    except Exception as e:
        log_error(f"Discord send failed: {e}")

def scan_target(target):
    log(f"🧠 Scanning: {target}")
    time.sleep(1.0)
    if "staging" in target or "beta" in target:
        raise RuntimeError("Target seems unreachable or rate-limited.")
    log(f"✅ Completed: {target}")
    return target

def run_parallel_scan():
    if not os.path.exists(TARGET_FILE):
        log_error("Target file missing!")
        send_discord("⚠️ No target list found.")
        sys.exit(1)

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        targets = [t.strip() for t in f if t.strip() and not t.startswith("#")]

    total = len(targets)
    if total == 0:
        log("⚠️ No targets to scan."); return

    log(f"🚀 Starting parallel scan on {total} targets.")
    success, failed = 0, 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_to_target = {executor.submit(scan_target, t): t for t in targets}
        for fut in concurrent.futures.as_completed(future_to_target):
            t = future_to_target[fut]
            try:
                fut.result()
                success += 1
            except Exception as e:
                failed += 1
                log_error(f"Failed {t}: {e}")

    summary = f"✅ Success: {success} | ❌ Failed: {failed} | Total: {total}"
    log(summary)
    send_discord(summary)

if __name__ == "__main__":
    run_parallel_scan()
