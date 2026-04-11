---
name: telegram-command-center
category: hermes
description: Build a robust Telegram bot daemon with SQLite persistence, polling, modular command handlers, and error handling.
---

# Telegram Command Center

Build a Telegram bot daemon that receives commands and executes them with persistent storage, logging, and modular handlers.

## Use When

- Need to expose Hermes functionality via Telegram
- Building a CLI/daemon responding to Telegram commands
- Want persistent offset tracking and command logging
- Need modular command handlers with easy extensibility

## Directory Structure

```
~/.hermes/command-center/
├── config.py          # BOT_TOKEN, AUTHORIZED_CHAT_ID, API_URL, DB_PATH
├── utils/
│   └── database.py   # SQLite: offsets, command logs, error logs
├── handlers/
│   ├── __init__.py   # COMMANDS dict mapping cmd->handler
│   ├── help_cmd.py
│   ├── usage_cmd.py
│   └── ...
├── daemon.py          # Main polling loop
└── requirements.txt   # psutil, requests, python-dotenv
```

## Dependencies (Ubuntu 24.04)

Ubuntu 24.04 blocks pip install --user (PEP 668). Use apt:

```bash
sudo apt install -y python3-psutil python3-dotenv
```

requests is pre-installed on most systems.

## Critical Pitfalls

- **Import structure**: When daemon runs as script (not module), relative imports fail with "attempted relative import beyond top-level package". Solution: EITHER use absolute imports everywhere (recommended) OR inline DB_PATH in utils/database.py to avoid circular dependency. Example fix: replace `from ..config import DB_PATH` with `DB_PATH = Path.home() / '.hermes' / 'command-center' / 'data.db'`
- **Handler imports**: All handlers must use absolute imports only. If a handler tries relative imports, it will crash during auto-registration. Common culprits: `from ..config import ...` or `from utils.database import ...` (should be from local imports only if using package structure, but safer to avoid cross-module deps in handlers).
- **PEP 668**: pip install fails on system Python. Must use apt or venv.
- **Offset persistence**: Save offset immediately after processing each update via database.set_offset()
- **Never let exceptions kill the loop**: Catch all in process_update() with try/except
- **ReadTimeout is normal**: getUpdates with timeout=50 returns ReadTimeout. Continue, don't error.
- **Test token first**: curl to /bot<token>/getMe before running daemon
- **Systemd environment**: Set PYTHONPATH if modules not installed globally. In service: `Environment=PYTHONPATH=/home/benlo/.hermes/command-center`
- **Handler auto-registration**: Use `importlib.import_module('handlers.' + fname.stem)` in handlers/__init__.py. Any broken handler prints error but doesn't stop registration.
- **Non-command messages**: Messages without `/` prefix cause parse_command to return `(None, None)`. The daemon MUST handle these — either reply normally or queue them. A daemon that silently drops messages is broken. Add a `handle_chat_message()` method and call it when `cmd is None`.
- **Health check**: The polling loop MUST include a periodic health check (e.g. every 5 min via `/getMe`). On failure, set an `emergency.active` flag file. On recovery, remove it. This enables downstream components to detect TG outage without killing the daemon.

## Event Bus Integration Pattern

Components (inbox_watcher, health check, emergency handler) push JSONL events to `~/.hermes/events/`:
```
~/.hermes/events/
├── inbox_events.jsonl   # {"type": "inbox_file", "path": ..., "category": ..., "timestamp": ...}
└── tg_notfall.jsonl     # {"type": "tg_notfall", "chat_id": ..., "text": ..., "timestamp": ...}
```

Hermes consumer reads these files in its turn — no real-time consumer needed. Simple, crash-resistant.

## Health Check + Emergency Mode Implementation

Add to daemon poll loop (before getUpdates):
```python
now = time.time()
if now - self.last_health_check > self.health_interval:
    self.last_health_check = now
    try:
        r = self.session.get(API_URL + "/getMe", timeout=5)
        if r.status_code != 200 or not r.json().get('ok'):
            raise Exception(f"Health failed: {r.status_code}")
        emergency_path = os.path.expanduser("~/.hermes/command-center/emergency.active")
        if os.path.exists(emergency_path):
            os.remove(emergency_path)  # Health restored
    except Exception as e:
        emergency_path = os.path.expanduser("~/.hermes/command-center/emergency.active")
        if not os.path.exists(emergency_path):
            with open(emergency_path, "w") as f:
                f.write(f"TG health check failed at {datetime.now().isoformat()}\n")
```

When non-command messages arrive during emergency mode, queue them to `~/.hermes/events/tg_notfall.jsonl` instead of ignoring them.

## 409 Conflict Resolution (Telegram 409: Conflict)

Der Telegram 409 Fehler ("Conflict: terminated by other getUpdates request") passiert wenn ZWEI Prozesse gleichzeitig poll-en. Typischerweise: alter `telegram_bot_v2.py` oder Watchdog neben `daemon.py`.

**Diagnose:**
```bash
ps aux | grep -E "telegram_bot|daemon\.py|poll" | grep -v grep
```

**Fix:**
```bash
pkill -9 -f telegram_bot_v2
pkill -9 -f daemon.py
sleep 5
cd ~/.hermes/command-center && python3 daemon.py > daemon.log 2>&1 &
sleep 10 && tail -30 daemon.log
```

**Check sauber:** Daemon loggt `Polling loop started` OHNE 409 Errors.

## Non-Command Messages → Inbox Writer

Ben hat festgestellt: Freie Textnachrichten vom Phone landen NICHT automatisch als Dateien in `/mnt/c/Users/benlo/Desktop/Hermes-Inbox/bens Smartphone - Inbox/`. Nur strukturierte Reports/Commands erzeugen Dateien.

**Gap**: Der Bot empfängt Text, antwortet mit Index-Report, aber der Inhalt wird nicht persistent gespeichert.

**Empfohlene Erweiterung**: `handle_chat_message()` soll Nachrichten als `.txt` oder `.jsonl` in die Smartphone-Inbox schreiben:
```python
def handle_chat_message(self, message):
    text = message.get('text', '')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    inbox_path = Path('/mnt/c/Users/benlo/Desktop/Hermes-Inbox/bens Smartphone - Inbox')
    inbox_path.mkdir(parents=True, exist_ok=True)
    with open(inbox_path / f'msg_{timestamp}.txt', 'w') as f:
        f.write(f'From: Phone\nText: {text}\n')
```
Damit kommen ALLE Phone-Nachrichten als verarbeitbare Dateien an.