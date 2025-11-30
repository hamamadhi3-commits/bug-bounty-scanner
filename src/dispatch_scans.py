import sys
import time
import random

def main():
    if len(sys.argv) < 3:
        print("⚙️ Usage: python3 dispatch_scans.py --worker <id>")
        sys.exit(1)

    worker_id = sys.argv[2]
    print(f"🚀 Worker #{worker_id} started scanning...")

    # simulate scanning (in real version this would call the actual scanner)
    time.sleep(random.randint(3, 8))

    print(f"✅ Worker #{worker_id} finished scanning successfully.")

if __name__ == "__main__":
    main()
