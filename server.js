const express = require('express');
const path = require('path');
const app = express();

// ─── In-memory store (keyed by client_id) ───────────
// pendingTexts[clientId] = { id, text, timestamp }
const pendingTexts = {};
let globalTextId = 0;

// ─── Middleware ─────────────────────────────────────
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  next();
});

// ─── Routes ─────────────────────────────────────────

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// POST /send  — body: { text, client_id }
app.post('/send', (req, res) => {
  const { text, client_id } = req.body;

  if (!text || !text.trim()) {
    return res.status(400).json({ error: 'No text provided' });
  }

  if (client_id === undefined || client_id === null || client_id === '') {
    return res.status(400).json({ error: 'client_id is required' });
  }

  const cid = parseInt(client_id);
  if (isNaN(cid)) {
    return res.status(400).json({ error: 'client_id must be a number' });
  }

  globalTextId++;
  pendingTexts[cid] = {
    id: globalTextId,
    text: text.trim(),
    timestamp: Date.now()
  };

  console.log(`[SEND] client_id=${cid} id=${globalTextId} len=${text.length}`);
  res.json({ success: true, id: globalTextId });
});

// GET /poll?last_id=N&client_id=N
app.get('/poll', (req, res) => {
  const lastId   = parseInt(req.query.last_id   || '0');
  const clientId = parseInt(req.query.client_id || '0');

  if (isNaN(clientId) || clientId === 0) {
    return res.status(400).json({ error: 'client_id is required' });
  }

  const pending = pendingTexts[clientId];

  if (pending && pending.id > lastId) {
    return res.json({
      available: true,
      id: pending.id,
      text: pending.text
    });
  }

  res.json({ available: false });
});

// POST /ack  — body: { id, client_id }
app.post('/ack', (req, res) => {
  const { id, client_id } = req.body;
  const cid = parseInt(client_id);

  if (pendingTexts[cid] && pendingTexts[cid].id === id) {
    console.log(`[ACK] client_id=${cid} id=${id} cleared`);
    delete pendingTexts[cid];
  }

  res.json({ success: true });
});

// ─── Start ───────────────────────────────────────────
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Typer server running on port ${PORT}`);
});