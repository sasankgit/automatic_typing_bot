const express = require('express');
const path = require('path');
const app = express();

// ─── In-memory store ────────────────────────────────
let pendingText = null;
let textId = 0;

// ─── Middleware ────────────────────────────────────
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  next();
});

// ─── Routes ────────────────────────────────────────

// Root → serve HTML UI
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// POST /send
app.post('/send', (req, res) => {
  const { text } = req.body;

  if (!text || !text.trim()) {
    return res.status(400).json({ error: 'No text provided' });
  }

  textId++;
  pendingText = {
    id: textId,
    text: text.trim(),
    timestamp: Date.now()
  };

  console.log(`[SEND] id=${textId} len=${text.length}`);
  res.json({ success: true, id: textId });
});

// GET /poll
app.get('/poll', (req, res) => {
  const lastId = parseInt(req.query.last_id || '0');

  if (pendingText && pendingText.id > lastId) {
    return res.json({
      available: true,
      id: pendingText.id,
      text: pendingText.text
    });
  }

  res.json({ available: false });
});

// POST /ack
app.post('/ack', (req, res) => {
  const { id } = req.body;

  if (pendingText && pendingText.id === id) {
    console.log(`[ACK] id=${id} cleared`);
    pendingText = null;
  }

  res.json({ success: true });
});

// ─── Start Server ──────────────────────────────────
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Typer server running on port ${PORT}`);
});