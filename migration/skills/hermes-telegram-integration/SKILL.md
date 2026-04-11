---
name: hermes-telegram-integration
description: Telegram Bot setup for alerts and command reception
version: 1.0.0
---

# Hermes Telegram Integration

Integration of Telegram for automated alerts, notifications, and command reception.

## Configuration

Credentials stored in two places:
1. **Memory**: `TELEGRAM_BOT_TOKEN`, `TG_CHAT_ID` (in Hermes long-term memory).
2. **Config**: `~/.hermes/config.yaml` under `telegram:` section.

## Sending Alerts (Inbox Processor)

Used by `inbox_processor.py` via `requests.post`:
```python
url = f"https://api.telegram.org/bot{token}/sendMessage"
data = {"chat_id": TG_CHAT, "text": msg, "parse_mode": "HTML"}
r = requests.post(url, data=data, timeout=10)
```

## Receiving Messages (Two-Process Architecture)

### 1. Receiver (polls Telegram → writes JSON inbox)
- **Script**: `/home/benlo/hermes-base/monitoring/telegram_receiver.py`
- Polls `getUpdates` every 2 seconds.
- Writes to `/tmp/hermes_telegram_inbox.json` (Max 50 entries).
- Each entry contains: `text`, `sender`, `date`, `timestamp`, `message_id`.
- **CRITICAL**: `message_id` field is REQUIRED for deduplication. Without it, the Auto-Ack processor can't distinguish new from old messages.
- **Offset handling**: Stored in `~/.hermes/telegram_offset.txt`.

### 2. Auto-Ack (reads JSON inbox → sends instant reply)
- **Script**: `/home/benlo/hermes-base/monitoring/telegram_autoack.py`
- Reads inbox JSON every 1 second.
- Sends instant acknowledgment: "✅ Empfangen von {sender} um {HH:MM} – werde sofort bearbeiten."
- Tracks highest `message_id` seen — only replies to NEW messages.
- If it crashes or exits, restart with `nohup python3 ... &`.

## Clean Restart Procedure (when Telegram gets stuck)

```bash
# 1. Kill both processes
pkill -f telegram_receiver || true
pkill -f telegram_autoack || true
sleep 2

# 2. Reset offset and clear inbox
echo "0" > ~/.hermes/telegram_offset.txt
echo "[]" > /tmp/hermes_telegram_inbox.json

# 3. Start Receiver FIRST
nohup python3 /home/benlo/hermes-base/monitoring/telegram_receiver.py > /tmp/telegram_receiver.log 2>&1 &

# 4. Start Auto-Ack SECOND
nohup python3 /home/benlo/hermes-base/monitoring/telegram_autoack.py > /tmp/telegram_autoack.log 2>&1 &
```

## Pitfalls & Fixes

- **409 Conflict auf getUpdates**: Wenn MEHR ALS EIN Prozess gleichzeitig `getUpdates` aufruft, gibt Telegram einen Lock-Fehler (409 Conflict). **Nur EIN EINZIGER Prozess darf pollten.** Niemals Poller und Daemon parallel laufen lassen. Vor Start: `pkill -f telegram_; pkill -f tg_`.
- **Offset=0 spamt den User**: Wenn der Offset beim Start 0 ist, liest er ALTE Nachrichten von heute und antwortet auf jede. **Fix**: Bei Erststart `getUpdates` ohne Offset aufrufen, den letzten `update_id` holen + 1, und DAS als Startoffset setzen.
- **message_id missing in receiver**: Original receiver.py did NOT write `message_id`, causing auto-ack to never detect new messages. Patch: added `message_id = update.get("message_id", 0)` to entry dict.
- **Auto-Ack SyntaxError / write_file trailing quote**: `write_file` hangt manchmal ein `"` an die letzte Zeile von Python-Dateien. Fix: Nach write_file immer `tail -c 5 file` prüfen. Vor Start: `python3 -c "compile(open(file).read(), file, 'exec')"`
- **Dual receiver processes creep**: cron restarts or manual restarts spawn extra instances. Fix: `pkill -f telegram_receiver` ALL instances before restarting.
- **Cross-Mount Locks**: Windows files on Desktop (mounted in WSL) often lock if open in apps. `inbox_processor.py` tries `rename`, then `copy+remove`, then marks as "locked" and skips if still fail.
- **Telegram Offset loss**: If offset gets out of sync, `getUpdates` returns empty list even if messages exist. Fix: delete offset file, restart receiver. Note: Telegram deletes updates after ~24h if not polled.
- **Sudo Setup**: `sudo` is enabled without password via `/etc/sudoers.d/hermes` (added for automation scripts).
- **WSL Cron**: Cron service is enabled and running in WSL. Jobs added via standard crontab.
- **Watchdog Multiples**: `pkill -f inbox_watcher` to kill all multiples. Only start ONE instance via `nohup`.

## Key Paths
- Token/Config: `~/.hermes/config.yaml`
- Processor: `/home/benlo/hermes-base/monitoring/inbox_processor.py`
- Receiver: `/home/benlo/hermes-base/monitoring/telegram_receiver.py`
- Inbox: `/mnt/c/Users/benlo/Desktop/Hermes-Inbox/` (Main), `.../bens Smartphone - Inbox/` (Phone)
- Sudoers: `/etc/sudoers.d/hermes` (benlo ALL=(ALL) NOPASSWD: ALL)

## Testing Commands

```bash
# Send test message
curl -s "https://api.telegram.org/bot$TOKEN/sendMessage" -d "chat_id=$CID" -d "text=Test"

# Check Receiver logs
tail -f /tmp/telegram_receiver.log

# Check Inbox Processor logs
tail -f /tmp/inbox_processor_cron.log
```