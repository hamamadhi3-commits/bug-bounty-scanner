import requests
import time

def fetch_targets():
    """
    دۆزینەوەی هەدفە نوێ لە Bugcrowd API یەکی فەرمی.
    لە رێگەی scraping بەکارهاتووە چونک Bugcrowd API بەردەست نییە بۆ گشتی.
    """
    print("🔍 دۆزینەوەی هەدفە نوێ لە Bugcrowd...")
    url = "https://bugcrowd.com/programs.json?page=1"
    headers = {"User-Agent": "DigitalSentinel/3.1"}
    programs = []

    try:
        for page in range(1, 10):  # 9 پەیج یان زیاتریش
            response = requests.get(f"https://bugcrowd.com/programs.json?page={page}", headers=headers)
            if response.status_code != 200:
                break
            data = response.json().get("programs", [])
            for prog in data:
                name = prog.get("name", "unknown")
                url = prog.get("url", "")
                if name and url:
                    programs.append(f"{name} - {url}")
            time.sleep(1)

        with open("bug_bounty_targets.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(programs))
        print(f"✅ {len(programs)} هەدف نوێ نووسرا لە bug_bounty_targets.txt")

    except Exception as e:
        print(f"⚠️ هەڵە لە دۆزینەوەی هەدفەکان: {e}")

if __name__ == "__main__":
    fetch_targets()
