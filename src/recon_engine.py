#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Recon Engine – Digital Sentinel v5.0
Performs parallel host checks on collected scopes.
"""

import os
import aiohttp
import asyncio
from datetime import datetime

TARGET_DIR = "targets"
REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)

async def check_domain(session, domain):
    url = f"https://{domain}"
    try:
        async with session.get(url, timeout=10) as resp:
            code = resp.status
            if code < 400:
                return f"🟢 {domain} - OK ({code})"
            else:
                return f"🟡 {domain} - Warning ({code})"
    except Exception:
        return f"🔴 {domain} - Unreachable"

async def run_scan():
    results = []
    async with aiohttp.ClientSession() as session:
        for file in os.listdir(TARGET_DIR):
            if file.endswith(".txt"):
                program = file.replace(".txt", "")
                print(f"🧠 Scanning {program}...")
                with open(os.path.join(TARGET_DIR, file)) as f:
                    domains = [x.strip() for x in f if x.strip()]
                checks = [check_domain(session, d) for d in domains]
                batch = await asyncio.gather(*checks)
                results.extend([f"[{program}] {r}" for r in batch])
    return results

def save_report(results):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M")
    path = os.path.join(REPORT_DIR, f"recon_{timestamp}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(results))
    print(f"✅ Report saved: {path}")

def main():
    print("🚀 Running Recon Engine...")
    results = asyncio.run(run_scan())
    save_report(results)
    print("✅ Recon completed successfully.")

if __name__ == "__main__":
    main()
