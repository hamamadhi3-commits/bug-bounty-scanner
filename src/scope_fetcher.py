#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 Bugcrowd Scope Fetcher – Digital Sentinel v5.0
Dynamically collects in-scope targets from Bugcrowd programs.
"""

import requests
from bs4 import BeautifulSoup
import os
import time

BASE_URL = "https://bugcrowd.com"
OUTPUT_DIR = "targets"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_programs():
    url = f"{BASE_URL}/programs"
    html = requests.get(url, timeout=20).text
    soup = BeautifulSoup(html, "html.parser")

    programs = []
    for a in soup.select("a.bc-program-card__link"):
        name = a.get("href", "").strip("/")
        if name and name not in programs:
            programs.append(name)
    return programs

def fetch_scope(program):
    print(f"🔎 Fetching scope for: {program}")
    url = f"{BASE_URL}/{program}"
    html = requests.get(url, timeout=20).text
    soup = BeautifulSoup(html, "html.parser")

    targets = []
    for li in soup.select("li[data-test='target-asset']"):
        txt = li.get_text(strip=True)
        if any(x in txt for x in [".com", ".net", ".org"]):
            targets.append(txt)

    if targets:
        with open(f"{OUTPUT_DIR}/{program}.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(targets))
        print(f"✅ Saved {len(targets)} targets for {program}")
    else:
        print(f"⚠️ No domains found for {program}")

def main():
    print("🚀 Starting Bugcrowd scope fetcher...")
    programs = fetch_programs()[:203]  # limit to 203 for ethical scope
    print(f"📦 Found {len(programs)} programs")

    for p in programs:
        try:
            fetch_scope(p)
            time.sleep(3)
        except Exception as e:
            print(f"❌ Error on {p}: {e}")

    print("✅ Scope fetching completed.")

if __name__ == "__main__":
    main()
