#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Recon Engine – Digital Sentinel v5.0
Performs parallel domain scans from Bugcrowd scope lists.
"""

import os, asyncio, aiohttp
from datetime import datetime

TARGET_DIR = "targets"
REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)

async def check_domain(session, domain):
    url = f"https://{domain}"
    try:
        async with session.get(url, timeout=8) as resp:
            code = resp.status
            if code < 400:
                return f"🟢 {domain} – OK ({code})"
            return f"🟡 {domain} – Warning ({code})"
    except Exception:
        return f"🔴 {domain} – Unreachable"

async def scan_program(session, program):
    path = os.path.join(TARGET_DIR, f"{program}.txt")
    if not os.path.exists(path):
        return [f"⚠️ No targets for {program}"]
    with open(path) as f:
        domains = [x.strip() for x in f if x.strip()]
    results = await asyncio.gather(*[check_domain(session, d) for d in domains])
    return [f"[{program}] {r}" for r in results]

async def main_scan():
    tasks = []
    async with aiohttp.ClientSession() as session:
        for file in os.listdir(TARGET_DIR):
            if file.endswith(".txt"):
                program = file.replace(".txt", "")
                tasks.append(scan_program(session, program))
        result_sets = await asyncio.gather(*tasks)
        return [item for subset in result_sets for item in subset]

def save_report(data):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M")
    filename = f"reports/recon_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(data))
    print(f"✅ Report saved: {filename}")

def main():
    print("🚀 Running Recon Engine...")
    results = asyncio.run(main_scan())
    save_report(results)
    print("✅ Recon cycle completed successfully.")

if __name__ == "__main__":
    main()
