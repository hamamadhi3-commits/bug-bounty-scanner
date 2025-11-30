import json

def generate_report():
    with open("logs/vulns_found.json") as f:
        vulns = json.load(f)

    for v in vulns:
        print(f"⚠️ {v['type']} found at {v['url']} – Severity: {v['severity']}")
    print(f"\n✅ Total vulnerabilities: {len(vulns)}")

if __name__ == "__main__":
    generate_report()
