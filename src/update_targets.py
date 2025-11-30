#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛰️ Digital Sentinel Target Auto-Updater v1.0
Automatically refreshes the 203-domain Bugcrowd target list every 5 days.
"""

import os
import time
import requests
from datetime import datetime

TARGET_PATH = "targets/bugcrowd_203.txt"
BACKUP_DIR = "targets/backups"
BUGCROWD_SOURCE = "https://raw.githubusercontent.com/arkadiyt/bounty-targets-data/main/data/bugcrowd_data.json"

os.makedirs(BACKUP_DIR, exist_ok=True)

def log(msg):
    print(f"[{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def update_targets():
    try:
        log("🌐 Fetching latest Bugcrowd data...")
        response = requests.get(BUGCROWD_SOURCE, timeout=15)
        response.raise_for_status()

        # save backup of old list
        if os.path.exists(TARGET_PATH):
            backup_name = os.path.join(
                BACKUP_DIR, f"bugcrowd_203_{int(time.time())}.bak"
            )
            os.rename(TARGET_PATH, backup_name)
            log(f"📦 Backup saved: {backup_name}")

        data = response.text
        domains = []
        for line in data.splitlines():
            if '"target_url"' in line:
                url = line.split(":")[1].strip().strip('" ,')
                domain = url.replace("https://", "").replace("http://", "")
                if domain and "." in domain:
                    domains.append(domain)

        domains = list(set(domains))
        domains = sorted(domains)[:203]

        with open(TARGET_PATH, "w", encoding="utf-8") as f:
            f.write("# Auto-generated Bugcrowd authorized targets (203 domains)\n")
            f.write("# Updated: " + datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC\n"))
            f.write("# Source: " + BUGCROWD_SOURCE + "\n\n")
            f.write("\n".join(domains))

        log(f"✅ Updated {len(domains)} domains successfully!")

    except Exception as e:
        log(f"❌ Update failed: {e}")

if __name__ == "__main__":
    update_targets()
