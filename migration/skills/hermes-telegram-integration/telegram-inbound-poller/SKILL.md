---
name: telegram-inbound-poller
category: hermes-telegram-integration
description: Receive incoming Telegram messages, save them to local inbox, and auto-respond.
---

# Telegram Inbound Poller & Auto-Ack

## Purpose
Receive incoming Telegram messages, save them to a local JSON inbox, and optionally send an automatic acknowledgment. Polls every 2 seconds.

## Setup Steps
1. **Create `telegram_receiver.py`**:
   - Uses `requests.get()` against `api.telegram.org/bot<TOKEN>/getUpdates`.
   - Updates `/tmp/hermes_telegram_inbox.json` with new messages from the target `chat_id`.
   - Saves the last processed `update_id` to `~/.hermes/telegram_offset.txt`.

2. **Create `telegram_autoack.py`**:
   - Reads `/tmp/hermes_telegram_inbox.json` every 2 seconds.
   - Sends an acknowledgment message via `curl` back to the `chat_id`.
   - Updates the last processed message to avoid double-replies.

3. **Run in background**:
   ```bash
   nohup python3 telegram_receiver.py > /tmp/telegram_receiver.log 2>&1 &
   nohup python3 telegram_autoack.py > /tmp/telegram_autoack.log 2>&1 &
   ```

## Pitfalls & Recommended Architecture (2026 Update)

- **409 Conflict lock**: Calling `getUpdates` from more than one process causes Telegram API to return 409 Conflict. The old two-process model (receiver + autoack) was fragile. **New recommended approach**: Use a single `tg_daemon.py` (see hermes-telegram-integration) that combines polling, queueing, auto-ack, and command dispatch in one process with SQLite DB. NO concurrent getUpdates calls.
- **Offset=0 spam**: Starting with offset=0 re-triggers all old messages. **Fix**: On daemon start, fetch the latest `update_id` via `getUpdates(offset=0, limit=1)` once, then `offset = latest_update_id + 1`. Store this in DB, not in a separate text file.
- **write_file trailing quote bug**: Hermes toolchain sometimes appends an extra `"` at end of Python files written via `write_file`. Always verify with `python3 -m py_compile <file>` after writing. If it fails, `tail -n 5 <file>` to spot stray quote.
- **Duplicate processes**: Never run more than one poller/daemon. Always `pkill -f telegram_` before starting new instances. Use PID files (`/tmp/tg_daemon.pid`) for tracking.
- **WSL background persistence**: Use `nohup python3 script.py > /tmp/script.log 2>&1 &` and write a PID file. Cron should monitor with `pgrep -f script.py` and restart if missing.
- **Auto-Ack vs Command Dispatch**: Separate concerns: auto-ack (instant <2s) should happen before any command processing. The unified achieves this by immediate `sendMessage` upon reception, then queueing the command for later execution.
- **Database queue**: Prefer SQLite (`~/.hermes/tg_daemon.db`) over JSON files. Tables: `queue` (incoming messages, state='pending'/'processing'/'done'), `settings` (offset), `outbox` (outgoing, retry on 429).

## Files
- `~/hermes-base/monitoring/telegram_receiver.py`
- `~/hermes-base/monitoring/telegram_autoack.py`
- `/tmp/hermes_telegram_inbox.json` (Inbox data)
