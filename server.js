const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

let pendingText = null;
let textId = 0;

// Web UI
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Client sends text from the web UI
app.post('/send', (req, res) => {
  const { text } = req.body;
  if (!text || !text.trim()) {
    return res.status(400).json({ error: 'No text provided' });
  }
  textId++;
  pendingText = { id: textId, text: text.trim(), timestamp: Date.now() };
  console.log(`[${new Date().toISOString()}] New text queued (id=${textId}), length=${text.length}`);
  res.json({ success: true, id: textId });
});

// Python client polls this endpoint
app.get('/poll', (req, res) => {
  const lastId = parseInt(req.query.last_id || '0');
  if (pendingText && pendingText.id > lastId) {
    res.json({ available: true, id: pendingText.id, text: pendingText.text });
  } else {
    res.json({ available: false });
  }
});

// Python client confirms it received the text
app.post('/ack', (req, res) => {
  const { id } = req.body;
  if (pendingText && pendingText.id === id) {
    pendingText = null;
    console.log(`[${new Date().toISOString()}] Text id=${id} acknowledged and cleared`);
  }
  res.json({ success: true });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Typer server running on http://localhost:${PORT}`);
});