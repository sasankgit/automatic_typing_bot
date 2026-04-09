import pyautogui
import time
import requests
import sys

# ─── CONFIG ─────────────────────────────────────────
SERVER_URL    = "https://automatic-typing-bot.onrender.com"
POLL_INTERVAL = 2        # normal polling
TYPING_DELAY  = 0.01
COUNTDOWN     = 4

MAX_BACKOFF   = 30       # max retry delay (seconds)

pyautogui.FAILSAFE = True

# reuse connection (IMPORTANT for long run)
session = requests.Session()


def poll_once(last_id):
    try:
        r = session.get(
            f"{SERVER_URL}/poll",
            params={"last_id": last_id},
            timeout=10
        )
        r.raise_for_status()
        data = r.json()
        return data if data.get("available") else None

    except requests.exceptions.RequestException as e:
        print(f"\n[WARN] Connection issue: {e}")
        return "ERROR"


def acknowledge(text_id):
    try:
        session.post(
            f"{SERVER_URL}/ack",
            json={"id": text_id},
            timeout=5
        )
    except Exception as e:
        print(f"[WARN] Ack failed: {e}")


def type_text(text):
    for char in text:
        pyautogui.write(char)
        time.sleep(TYPING_DELAY)


def countdown(seconds):
    for i in range(seconds, 0, -1):
        print(f"\rSwitch window in {i}s...", end="", flush=True)
        time.sleep(1)
    print()


def main():
    print("=" * 50)
    print("   TYPER BOT — ALWAYS ON MODE 🚀")
    print(f"   Server: {SERVER_URL}")
    print("=" * 50)

    last_id = 0
    backoff = 2   # start retry delay

    while True:
        result = poll_once(last_id)

        # ─── ERROR HANDLING (Render sleep / network issues) ───
        if result == "ERROR":
            print(f"[INFO] Retrying in {backoff}s...")
            time.sleep(backoff)
            backoff = min(backoff * 2, MAX_BACKOFF)
            continue

        # reset backoff if successful
        backoff = 2

        # ─── NEW TEXT RECEIVED ───
        if result:
            text = result["text"]
            text_id = result["id"]

            print(f"\n[✓] Received text (id={text_id}, len={len(text)})")

            acknowledge(text_id)
            last_id = text_id

            countdown(COUNTDOWN)

            print("[→] Typing...")
            start = time.time()

            type_text(text)

            print(f"[✓] Done in {time.time() - start:.1f}s\n")

        else:
            # silent idle (no spam dots)
            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[Stopped]")
        sys.exit(0)