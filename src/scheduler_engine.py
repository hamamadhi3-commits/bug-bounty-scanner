#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🕒 Digital Sentinel PRIME v5.0 – Scheduler Engine
Handles 6-hour rest cycles, auto-restart, and resume from last checkpoint.
"""

import os, time, json, subprocess
from datetime import datetime

STATE_FILE = "state.json"
COOLDOWN_HOURS = 6

def save_state(data):
    with open(STATE_FILE, "w") as f: json.dump(data, f)

def load_state():
    if not os.path.exists(STATE_FILE): return {"last_run": None}
    with open(STATE_FILE) as f: return json.load(f)

def wait_hours(h):
    print(f"⏳ Cooling down for {h} hours...")
    time.sleep(h * 3600)

def run_worker():
    print(f"⚙️ Launching parallel worker at {datetime.utcnow()}")
    subprocess.run(["python3", "src/scan_engine_parallel.py"], check=False)

def main():
    while True:
        state = load_state()
        last = state.get("last_run")
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        run_worker()
        save_state({"last_run": now})
        wait_hours(COOLDOWN_HOURS)

if __name__ == "__main__":
    main()
