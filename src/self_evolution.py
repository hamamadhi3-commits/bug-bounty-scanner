#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧬 Digital Sentinel PRIME v5.0 – Self-Evolution Core
Learns from past runs, improves retry targeting, prioritizes failed ones.
"""

import os, json, random, time

ERROR_LOG = "logs/errors.log"
TARGET_FILE = "targets/bugcrowd_203.txt"
EVOLVED_FILE = "targets/bugcrowd_evolved.txt"

def evolve_targets():
    if not os.path.exists(ERROR_LOG): return
    failed_targets = []
    with open(ERROR_LOG, "r", encoding="utf-8") as f:
        for line in f:
            if "Failed" in line and "http" not in line:
                parts = line.split("Failed ")[-1].split(":")[0]
                failed_targets.append(parts.strip())

    if not failed_targets:
        print("✅ No failed targets to evolve.")
        return

    print(f"🧠 Evolving {len(failed_targets)} targets...")

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        base = [t.strip() for t in f if t.strip() and not t.startswith("#")]

    new_targets = base + failed_targets
    new_targets = sorted(list(set(new_targets)), key=lambda x: random.random())

    with open(EVOLVED_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(new_targets))
    print(f"⚡ Evolution complete → {EVOLVED_FILE}")

if __name__ == "__main__":
    evolve_targets()
