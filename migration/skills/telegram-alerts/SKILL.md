---
name: telegram-alerts
version: 1.0
description: Configure Telegram bot notifications for Hermes events (Inbox alerts, cron status, etc).
---

# Telegram Alerts für Hermes

## Credentials
- **Bot Token:** In `~/.hermes/.env` als `TELEGRAM_BOT_TOKEN=...`
- **Chat ID:** `2029024880` (Ben)
- **Bot Username:** `@hermes187bot`

## Setup
Token in die `.env` schreiben:
```bash
echo 'TELEGRAM_BOT_TOKEN="8674881293:AAHZl42fENa6WSlgDCOLDEmSLHlne_p7vxc"' >> ~/.hermes/.env
echo 'TELEGRAM_CHAT_ID="2029024880"' >> ~/.hermes/.env
```

## Nachrichten senden (curl)
```bash
curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -d "chat_id=${TELEGRAM_CHAT_ID}" \
  -d "text=✅ Test: Telegram funktioniert!"
```

## Nachrichten senden (Python)
```python
import requests, os
token = os.environ.get("TELEGRAM_BOT_TOKEN") or "8674881293:AAHZl42fENa6WSlgDCOLDEmSLHlne_p7vxc"
chat_id = os.environ.get("TELEGRAM_CHAT_ID") or "2029024880"
url = f"https://api.telegram.org/bot{token}/sendMessage"
requests.post(url, data={"chat_id": chat_id, "text": "Nachricht hier"})
```

## Use Cases
1. **Inbox-Alerts:** Bei jeder sortierten Datei → Telegram-Nachricht mit Score + Ort
2. **Cron-Bestätigung:** Cron-Job läuft erfolgreich → "Inbox-Check OK"
3. **Error-Alerts:** Wenn etwas kaputt geht → "⚠️ Error: ..."
4. **Watchdog-Status:** Bot meldet sich wenn Watchdog abstürzt

## Feedback-Loop
WICHTIG: Der Benutzer MUSS Rückmeldung bekommen wenn das System etwas macht.
Ohne Telegram-Benachrichtigung scheint das System tot zu sein.
Immer bei jedem Event eine Nachricht senden!

## Pitfalls
- `getUpdates` löscht Updates nach ~24h. Setze Offset auf 0 um aktuelle zu sehen.
- Telegram API hat Rate-Limits: max 30/sec für sendMessage.
- Bot-Token niemals in Git commiten!