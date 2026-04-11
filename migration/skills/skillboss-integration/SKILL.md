---
name: skillboss-integration
description: Integration of SkillBoss API for Vision (Image Analysis) and High-End Model routing via single key.
version: 1.0.0
---

# SkillBoss Integration

**Base URL:** `https://api.heybossai.com/v1`
**Auth:** `Authorization: Bearer $SKILLBOSS_API_KEY`
**Key Location:** `~/.hermes/.env`

## Vision Calls (Image Analysis)
Use Python `urllib` (avoid shell escaping issues with curl):

```python
import base64, json, urllib.request

key = "sk-..."  # oder aus env lesen
with open("/path/to/image.png", "rb") as f:
    b64 = base64.b64encode(f.read()).decode()

payload = {
    "model": "openai/gpt-4o",
    "messages": [{
        "role": "user",
        "content": [
            {"type": "text", "text": "Describe this image"},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}", "detail": "high"}}
        ]
    }],
    "max_tokens": 2000
}

data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(
    "https://api.heybossai.com/v1/chat/completions",
    data=data,
    headers={
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    },
    method="POST"
)
with urllib.request.urlopen(req, timeout=60) as resp:
    result = json.loads(resp.read().decode())
    print(result["choices"][0]["message"]["content"])
```

## Chat Completion (Curl)
```bash
curl -s https://api.heybossai.com/v1/chat/completions \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"openai/gpt-4o-mini","messages":[{"role":"user","content":"ping"}],"max_tokens":10}'
```

## Troubleshooting
- `/v1/models` gibt 404 "Not Found" – Ignorieren.
- Verwende immer den `/v1/chat/completions` Endpunkt.
- Models nutzen das Format `openai/model-name` (z.B. `openai/gpt-4o`).