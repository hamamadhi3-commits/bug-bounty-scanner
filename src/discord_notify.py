import requests, json, os

def send_to_discord():
    webhook = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook:
        print("❌ Discord webhook not found!")
        return

    with open("logs/vulns_found.json") as f:
        vulns = json.load(f)

    if not vulns:
        print("✅ No vulnerabilities found.")
        return

    for v in vulns:
        data = {
            "embeds": [{
                "title": f"⚠️ Vulnerability Found – {v['type']}",
                "color": 16711680,
                "fields": [
                    {"name": "🌐 URL", "value": v["url"], "inline": False},
                    {"name": "🔥 Severity", "value": v["severity"], "inline": True},
                    {"name": "📆 Detected", "value": "AutoScan Cycle", "inline": True}
                ]
            }]
        }
        requests.post(webhook, json=data)
        print(f"📤 Sent report for {v['url']}")

if __name__ == "__main__":
    send_to_discord()
