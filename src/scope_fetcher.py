#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 Bugcrowd Scope Fetcher – Recon Sentinel v5.0
Automatically collects in-scope targets from Bugcrowd programs (up to 203).
"""

import requests, os, time
from bs4 import BeautifulSoup

BASE_URL = "https://bugcrowd.com"
OUTPUT_DIR = "targets"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_programs():
    html = requests.get(f"{BASE_URL}/programs", timeout=20).text
    soup = BeautifulSoup(html, "html.parser")
    links = soup.select("a.bc-program-card__link")
    programs = [a.get("href").strip("/") for a in links if a.get("href")]
    return list(set(programs))[:203]

def fetch_scope(program):
    url = f"{BASE_URL}/{program}"
    print(f"🔎 Fetching scope for: {program}")
    html = requests.get(url, timeout=20).text
    soup = BeautifulSoup(html, "html.parser")

    targets = []
    for li in soup.select("li[data-test='target-asset']"):
        text = li.get_text(strip=True)
        if any(x in text for x in [".com", ".net", ".org"]):
            targets.append(text)

    if targets:
        with open(f"{OUTPUT_DIR}/{program}.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(targets))
        print(f"✅ Saved {len(targets)} targets for {program}")
    else:
        print(f"⚠️ No targets found for {program}")

def main():
    print("🚀 Starting Bugcrowd scope fetcher...")
    programs = fetch_programs()
    print(f"📦 Found {len(programs)} programs.")

    for p in programs:
        try:
            fetch_scope(p)
            time.sleep(3)
        except Exception as e:
            print(f"❌ Error on {p}: {e}")

    print("✅ All scopes fetched successfully.")

if __name__ == "__main__":
    main()
