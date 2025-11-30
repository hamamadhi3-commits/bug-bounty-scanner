import asyncio, aiohttp, json, os
from bs4 import BeautifulSoup

async def check_xss(session, url):
    payload = "<script>alert(1)</script>"
    async with session.get(url + "?q=" + payload) as r:
        text = await r.text()
        if payload in text:
            return {"type": "XSS", "url": url, "severity": "High"}

async def check_sqli(session, url):
    payload = "' OR '1'='1"
    async with session.get(url + "?id=" + payload) as r:
        if "syntax" in await r.text().lower() or "mysql" in await r.text().lower():
            return {"type": "SQL Injection", "url": url, "severity": "Critical"}

async def scan_target(url):
    vulns = []
    async with aiohttp.ClientSession() as session:
        checks = [check_xss(session, url), check_sqli(session, url)]
        results = await asyncio.gather(*checks)
        for r in results:
            if r: vulns.append(r)
    return vulns

async def main():
    targets = ["https://testphp.vulnweb.com", "https://demo.testfire.net"]
    all_vulns = []
    for url in targets:
        vulns = await scan_target(url)
        all_vulns.extend(vulns)
    os.makedirs("logs", exist_ok=True)
    with open("logs/vulns_found.json", "w") as f:
        json.dump(all_vulns, f, indent=2)

if __name__ == "__main__":
    asyncio.run(main())
