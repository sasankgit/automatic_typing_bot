const express = require('express');
const app = express();

app.use(express.json());

let pendingText = null;
let textId = 0;

app.get('/', (req, res) => {
  res.json({ message: "Server running 🚀" });
});

app.post('/send', (req, res) => {
  const { text } = req.body;
  if (!text) return res.status(400).json({ error: 'No text' });

  textId++;
  pendingText = { id: textId, text };

  res.json({ success: true, id: textId });
});

app.get('/poll', (req, res) => {
  const lastId = parseInt(req.query.last_id || '0');

  if (pendingText && pendingText.id > lastId) {
    return res.json({ available: true, ...pendingText });
  }

  res.json({ available: false });
});

app.post('/ack', (req, res) => {
  if (pendingText && pendingText.id === req.body.id) {
    pendingText = null;
  }
  res.json({ success: true });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Running on ${PORT}`));