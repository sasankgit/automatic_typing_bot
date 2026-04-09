# TYPER — Remote Keystroke Control System

Paste text in the web UI → Python client auto-types it wherever your cursor is.

```
┌─────────────────────┐         ┌──────────────────────┐
│   Browser (you)     │  POST   │  Vercel Node Server  │
│   Web UI            │ ──────► │  /send               │
│   paste + SEND btn  │         │  stores pending text │
└─────────────────────┘         └──────────┬───────────┘
                                           │  GET /poll
                                ┌──────────▼───────────┐
                                │  Python Typer Bot    │
                                │  (your local PC)     │
                                │  pyautogui types it  │
                                └──────────────────────┘
```

---

## 1 · Deploy the Server to Vercel

```bash
cd typer-server
npm install

# Install Vercel CLI if needed
npm i -g vercel

vercel deploy --prod
```

Copy the production URL (e.g. `https://typer-server-xyz.vercel.app`).

---

## 2 · Configure the Python Client

Open `typer-client/typer_client.py` and edit the top section:

```python
SERVER_URL    = "https://your-app.vercel.app"  # ← paste your Vercel URL here
POLL_INTERVAL = 1.5    # seconds between polls
TYPING_DELAY  = 0.01   # seconds between each keystroke
COUNTDOWN     = 4      # seconds to switch window before typing begins
```

---

## 3 · Install Python Dependencies

```bash
pip install pyautogui requests
```

On Linux you may also need:
```bash
sudo apt install python3-tk python3-dev
pip install pyautogui[linux]
```

---

## 4 · Run the Typer Bot

```bash
cd typer-client
python typer_client.py
```

Leave this terminal running in the background.

---

## 5 · Use It

1. Open your Vercel URL in the browser
2. Paste your code / text into the editor
3. Click **SEND** (or press `Ctrl+Enter`)
4. The bot will print a **4-second countdown** — switch to your target window
5. Watch it type ✓

---

## Tips

| Tip | Detail |
|-----|--------|
| **Abort mid-type** | Move mouse to the very top-left corner of screen |
| **Slower typing** | Increase `TYPING_DELAY` (e.g. `0.05`) |
| **Faster typing** | Decrease `TYPING_DELAY` (e.g. `0.005`) |
| **Longer countdown** | Increase `COUNTDOWN` seconds |
| **Keyboard shortcut** | `Ctrl+Enter` in the web UI to send |

---

## File Structure

```
typer-server/
├── server.js          ← Express API + serves the web UI
├── package.json
├── vercel.json        ← Vercel deployment config
└── public/
    └── index.html     ← Web UI

typer-client/
└── typer_client.py    ← Run this on your local machine
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET`  | `/`  | Web UI |
| `POST` | `/send` | Submit text `{ text: "..." }` |
| `GET`  | `/poll?last_id=N` | Check for new text |
| `POST` | `/ack` | Confirm received `{ id: N }` |