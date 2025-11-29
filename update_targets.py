#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Digital Sentinel PRIME - Bugcrowd Target Intelligence Engine
Auto-fetches all supported companies (public bug bounty programs)
and saves clean domains to bug_bounty_targets.txt
"""

import requests
from bs4 import BeautifulSoup
import re
import time

BASE_URL = "https://bugcrowd.com/programs?page={}"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; DigitalSentinel/1.0; +https://sentinel.local)"
}

OUTPUT_FILE = "bug_bounty_targets.txt"

def extract_domain(text):
    """Extracts clean domain from text or URL"""
    pattern = r'([a-zA-Z0-9-]+\.[a-zA-Z]{2,})'
    match = re.search(pattern, text)
    if match:
        return match.group(1).lower()
    return None

def fetch_page(page):
    """Fetches one Bugcrowd page and returns program names + links"""
    url = BASE_URL.format(page)
    res = requests.get(url, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(res.text, "html.parser")
    cards = soup.select("a.bc-program-card__link")
    programs = []
    for card in cards:
        link = card.get("href")
        name = card.text.strip()
        if link and not link.startswith("http"):
            link = "https://bugcrowd.com" + link
        programs.append((name, link))
    return programs

def main():
    print("[*] Starting Bugcrowd Intelligence Fetcher...")
    all_domains = set()
    total_programs = 0

    for page in range(1, 10):
        print(f"[*] Fetching page {page}/9...")
        try:
            programs = fetch_page(page)
            total_programs += len(programs)
            for name, link in programs:
                domain = extract_domain(link) or extract_domain(name)
                if domain:
                    all_domains.add(domain)
            time.sleep(2)
        except Exception as e:
            print(f"[!] Error on page {page}: {e}")
            continue

    with open(OUTPUT_FILE, "w") as f:
        for d in sorted(all_domains):
            f.write(d + "\n")

    print(f"[✓] Total Programs Fetched: {total_programs}")
    print(f"[✓] Unique Domains Extracted: {len(all_domains)}")
    print(f"[✓] Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
