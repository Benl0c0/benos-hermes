---
name: benos-live-dashboard
---

# BEN//OS Live Dashboard

> Builds a live-updating system dashboard using Python's `http.server` and vanilla JS. No build tools required.

## Trigger
User wants to visualize Ollama status, system stats, or agent tree on their local machine (WSL).

## Architecture
**Backend:** Single Python file (`server.py`) serving static files and API endpoints.
**Frontend:** Single HTML file (`dashboard.html`) fetching from `/api/*` via JS `fetch`.

## Implementation: Backend (`server.py`)
```python
#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json, urllib.request, os

def check_ollama():
    try:
        with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=2) as r:
            data = json.loads(r.read())
            return {"running": True, "models": [m['name'] for m in data.get('models', [])]}
    except:
        return {"running": False, "models": []}

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/ollama":
            self.send_json(check_ollama())
        else:
            super().do_GET()
    def send_json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    def log_message(self, format, *args): pass

HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
```

## Implementation: Frontend
Use `setInterval` to poll APIs every 3-5s:
```javascript
async function updateStatus() {
  const res = await fetch('/api/ollama');
  const data = await res.json();
  if(data.running) {
    document.getElementById('status').innerText = 'ONLINE';
    document.getElementById('status').style.color = '#00ff41'; // Neon Green
  }
}
setInterval(updateStatus, 5000);
```

## Deployment
Run in WSL: `python3 server.py &`
Open in Windows: `http://localhost:8000/dashboard.html`

## Troubleshooting
- **Connection Refused:** Ensure server is running in WSL background.
- **No models:** Run `ollama list` in WSL to verify.
- **Restricted Shells (locolap):** Avoid `curl` commands; use `urllib` in Python for network checks.

## Notes for Ben
The dashboard is black + neon. Keep the contrast sharp.
This pattern doesn't depend on external package managers; plain Python stdlib.
Use as fallback if Node/Framer setup fails.