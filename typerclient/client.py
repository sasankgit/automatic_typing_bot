import pyautogui
import time
import requests
import sys

# ─── CONFIG ─────────────────────────────────────────
SERVER_URL   = "https://automatic-typing-bot.onrender.com"  # NO trailing /
POLL_INTERVAL = 1.5
TYPING_DELAY  = 0.01
COUNTDOWN     = 4

pyautogui.FAILSAFE = True


def poll_once(last_id):
    try:
        r = requests.get(
            f"{SERVER_URL}/poll",
            params={"last_id": last_id},
            timeout=5
        )
        r.raise_for_status()
        data = r.json()
        return data if data.get("available") else None
    except Exception as e:
        print(f"[WARN] Poll error: {e}")
        return None


def acknowledge(text_id):
    try:
        requests.post(
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
    print("=== TYPER BOT STARTED ===\n")

    last_id = 0

    while True:
        payload = poll_once(last_id)

        if payload:
            text = payload["text"]
            text_id = payload["id"]

            print(f"\n[✓] Received text (id={text_id})")

            acknowledge(text_id)
            last_id = text_id

            countdown(COUNTDOWN)

            print("[→] Typing...")
            type_text(text)

            print("[✓] Done\n")
        else:
            print(".", end="", flush=True)
            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped")
        sys.exit(0)