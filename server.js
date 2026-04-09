const http = require('http');
const fs   = require('fs');
const path = require('path');

// ─── In-memory store ────────────────────────────────────────────────
let pendingText = null;
let textId      = 0;

// ─── Helpers ────────────────────────────────────────────────────────
function readBody(req) {
  return new Promise((resolve, reject) => {
    let data = '';
    req.on('data', chunk => (data += chunk));
    req.on('end',  () => resolve(data));
    req.on('error', reject);
  });
}

function json(res, statusCode, obj) {
  const body = JSON.stringify(obj);
  res.writeHead(statusCode, {
    'Content-Type' : 'application/json',
    'Access-Control-Allow-Origin' : '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  });
  res.end(body);
}

function serveFile(res, filePath, contentType) {
  fs.readFile(filePath, (err, data) => {
    if (err) { res.writeHead(404); res.end('Not found'); return; }
    res.writeHead(200, { 'Content-Type': contentType });
    res.end(data);
  });
}

// ─── Router ─────────────────────────────────────────────────────────
const server = http.createServer(async (req, res) => {
  const url    = new URL(req.url, `http://${req.headers.host}`);
  const route  = url.pathname;
  const method = req.method;

  // CORS preflight
  if (method === 'OPTIONS') {
    res.writeHead(204, {
      'Access-Control-Allow-Origin' : '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    });
    return res.end();
  }

  // GET / → serve UI
  if (method === 'GET' && (route === '/' || route === '/index.html')) {
    return serveFile(res, path.join(__dirname, 'public', 'index.html'), 'text/html');
  }

  // POST /send → accept text from web UI
  if (method === 'POST' && route === '/send') {
    try {
      const raw  = await readBody(req);
      const body = JSON.parse(raw);
      if (!body.text || !body.text.trim()) return json(res, 400, { error: 'No text provided' });
      textId++;
      pendingText = { id: textId, text: body.text.trim(), timestamp: Date.now() };
      console.log(`[SEND] id=${textId} len=${body.text.length}`);
      return json(res, 200, { success: true, id: textId });
    } catch (e) {
      return json(res, 400, { error: 'Invalid JSON' });
    }
  }

  // GET /poll → Python client polls here
  if (method === 'GET' && route === '/poll') {
    const lastId = parseInt(url.searchParams.get('last_id') || '0');
    if (pendingText && pendingText.id > lastId) {
      return json(res, 200, { available: true, id: pendingText.id, text: pendingText.text });
    }
    return json(res, 200, { available: false });
  }

  // POST /ack → Python confirms receipt, clear queue
  if (method === 'POST' && route === '/ack') {
    try {
      const raw  = await readBody(req);
      const body = JSON.parse(raw);
      if (pendingText && pendingText.id === body.id) {
        console.log(`[ACK]  id=${body.id} cleared`);
        pendingText = null;
      }
      return json(res, 200, { success: true });
    } catch (e) {
      return json(res, 400, { error: 'Invalid JSON' });
    }
  }

  // 404
  res.writeHead(404);
  res.end('Not found');
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => console.log(`Typer server → http://localhost:${PORT}`));