import pyautogui
import time
import requests
import sys

# ─── CONFIG ───────────────────────────────────────────────────────────────────
SERVER_URL   = "https://your-app.vercel.app"   # ← Replace with your Vercel URL
POLL_INTERVAL = 1.5    # Seconds between polls
TYPING_DELAY  = 0.01   # Seconds between each character
COUNTDOWN     = 4      # Seconds to move cursor to target window after text arrives
# ──────────────────────────────────────────────────────────────────────────────

pyautogui.FAILSAFE = True   # Move mouse to top-left corner to abort typing


def poll_once(last_id: int) -> dict | None:
    """Returns new payload dict if available, else None."""
    try:
        r = requests.get(
            f"{SERVER_URL}/poll",
            params={"last_id": last_id},
            timeout=5
        )
        r.raise_for_status()
        data = r.json()
        return data if data.get("available") else None
    except requests.exceptions.ConnectionError:
        print("[ERROR] Cannot reach server. Check SERVER_URL and your connection.")
        return None
    except Exception as e:
        print(f"[WARN] Poll error: {e}")
        return None


def acknowledge(text_id: int):
    """Tell server this payload was received so it won't be sent again."""
    try:
        requests.post(
            f"{SERVER_URL}/ack",
            json={"id": text_id},
            timeout=5
        )
    except Exception as e:
        print(f"[WARN] Ack failed: {e}")


def type_text(text: str):
    """Type text character by character using pyautogui."""
    for char in text:
        # pyautogui.write() can't handle special unicode chars,
        # so fall back to typewrite for ASCII and hotkey for others
        try:
            pyautogui.write(char, interval=0)
        except Exception:
            pyautogui.hotkey('shift', char) if char.isupper() else None
        time.sleep(TYPING_DELAY)


def countdown(seconds: int, message: str):
    """Print a live countdown in the terminal."""
    for i in range(seconds, 0, -1):
        print(f"\r{message} {i}s ...", end="", flush=True)
        time.sleep(1)
    print()


def main():
    print("=" * 55)
    print("  TYPER BOT — Remote Keystroke Client")
    print(f"  Server : {SERVER_URL}")
    print(f"  Poll   : every {POLL_INTERVAL}s")
    print(f"  Speed  : {TYPING_DELAY}s / char")
    print("=" * 55)
    print("Listening for incoming text...\n")
    print("TIP: Move mouse to top-left corner to abort typing (failsafe).\n")

    last_id = 0

    while True:
        payload = poll_once(last_id)

        if payload:
            text    = payload["text"]
            text_id = payload["id"]
            chars   = len(text)

            print(f"\n[✓] New payload received (id={text_id}, {chars} chars)")
            acknowledge(text_id)
            last_id = text_id

            countdown(COUNTDOWN, "→ Switch to your target window! Starting in")

            print(f"[→] Typing {chars} characters...")
            start = time.time()
            type_text(text)
            elapsed = time.time() - start

            print(f"[✓] Done! Typed {chars} chars in {elapsed:.1f}s")
            print("\nListening for next payload...\n")
        else:
            # Idle indicator — dots cycling
            print(".", end="", flush=True)
            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[Stopped] Typer bot shut down.")
        sys.exit(0)