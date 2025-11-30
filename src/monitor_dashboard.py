import json
import datetime
import requests
import os

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK_URL")

def load_targets():
    try:
        with open("bug_bounty_targets.txt", "r") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        return []

def load_vulns():
    try:
        with open("logs/vulns_found.json", "r") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []

def send_discord_report(total_targets, total_vulns):
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    message = {
        "content": (
            f"📊 **Digital Sentinel Daily Report**\n"
            f"🕓 Date: {now}\n\n"
            f"🎯 Total Targets Scanned: **{total_targets}**\n"
            f"⚠️ Vulnerabilities Found: **{total_vulns}**\n"
            f"💾 Log File: `logs/vulns_found.json`\n\n"
            f"🚀 System running in 4x Parallel Cluster Mode"
        )
    }
    try:
        requests.post(DISCORD_WEBHOOK, json=message)
    except Exception as e:
        print("❌ Failed to send Discord report:", e)

if __name__ == "__main__":
    targets = load_targets()
    vulns = load_vulns()
    send_discord_report(len(targets), len(vulns))
