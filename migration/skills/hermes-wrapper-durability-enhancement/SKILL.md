---
name: hermes-wrapper-durability-enhancement
title: Hermes Wrapper Durability Enhancement
description: Fixes session persistence failures and config corruption recovery in Hermes wrapper
tags: [hermes, durability, recovery, session-persistence, config]
---

## Problem

Hermes loses all conversation state after crashes or config corruption because:

1. **Config corruption** – manual edits or crashes can break `config.yaml`, leaving Hermes unable to start
2. **History format mismatch** – wrapper expects `timestamp | role | content` but BEN/OS writes `# timestamp\n+content`
3. **Empty session_log.json** – due to failed history migration, session persistence doesn't work
4. **User forced to manually rewrite config** after every crash

## Solution

Patch `~/.local/bin/hermes-wrapper` with:

- **Auto-config recovery**: If `config.yaml` is missing or invalid, automatically restore minimal working default (`openrouter/free`) and backup corrupted file with timestamp
- **BEN/OS V2 history parser**: Read `.hermes_history` format (`# timestamp` followed by `+content`), extract last 500 turns, write to `session_log.json`
- **Idempotent migration**: Only migrate if `session_log.json` is empty; existing logs are preserved

## Implementation

Add to top of wrapper (imports, constants):

```python
import yaml
CONFIG_FILE = os.path.join(HERMES_DIR, 'config.yaml')
DEFAULT_CONFIG = 'model:\n  default: openrouter/free\n  provider: openrouter\n  base_url: https://openrouter.ai/api/v1\n  api_mode: chat_completions\n  max_tokens: 4000\n'
```

Add `ensure_valid_config()` function:

```python
def ensure_valid_config():
    """Wenn config.yaml fehlt oder ungültig, auf Minimal-Standard zurücksetzen."""
    try:
        if not os.path.exists(CONFIG_FILE):
            raise FileNotFoundError("config.yaml missing")
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            cfg = yaml.safe_load(f)
        if not (cfg and isinstance(cfg, dict) and 'model' in cfg and 'default' in cfg['model']):
            raise ValueError("model.default not found")
    except Exception as e:
        if os.path.exists(CONFIG_FILE):
            backup = CONFIG_FILE + f'.corrupt.{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}'
            os.rename(CONFIG_FILE, backup)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            f.write(DEFAULT_CONFIG)
        print(f"[Wrapper] Config recovered from corruption: {e}")
```

Replace `ensure_log_from_history()` with BEN/OS V2 parser:

```python
def ensure_log_from_history():
    if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:
        return
    if not os.path.exists(HISTORY_FILE):
        return
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = []
    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('#') and i+1 < len(lines):
            ts = line.lstrip('#').strip()
            i += 1
            if i < len(lines):
                content_line = lines[i].strip()
                if content_line.startswith('+'):
                    msg = content_line[1:]
                    entries.append({
                        "timestamp": ts,
                        "role": "user",
                        "content": msg
                    })
        i += 1

    recent = entries[-500:] if len(entries) > 500 else entries
    if recent:
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(recent, f, indent=2, ensure_ascii=False)
        print(f"[Wrapper] Migrated {len(recent)} turns from history to session_log.json")
```

Call in `main()`:

```python
def main():
    ensure_valid_config()
    ensure_log_from_history()
    # ... rest
```

## Verification

Test with:

```bash
rm ~/.hermes/session_log.json
python3 ~/.local/bin/hermes-wrapper --dry-run  # or just invoke wrapper
```

Expected output:
- `[Wrapper] Migrated X turns from history to session_log.json`
- `session_log.json` populated with last 500 turns

If config is corrupted intentionally (break YAML), wrapper should auto-repair and create `.corrupt.TIMESTAMP` backup.

## Notes

- Requires `python3-yaml` (`sudo apt-get install python3-yaml`)
- Does **not** handle `assistant` role in history (BEN/OS format doesn't include roles); all entries marked `user`
- Wrapper must be executable (`chmod +x ~/.local/bin/hermes-wrapper`)
- This enhancement makes Hermes resilient to user typos, crashes, and manual config errors without manual intervention

### Extended Durability Features (2026-04-05)

**Trottel-Safe Wrapper** (`~/.hermes/scripts/trottel_safe_wrapper.sh`):
- Starts Hermes as a subprocess and traps `SIGTERM`, `SIGINT`, `SIGHUP`, `SIGTSTP`, `SIGQUIT`.
- Logs signals to `/tmp/hermes-wrapper.log`.
- PID stored in `/tmp/hermes.pid` for external control.
- Enables clean shutdown on SIGTERM/SIGINT and restart on SIGHUP.

**Backup System**:
- Script: `~/.hermes/scripts/backup_hermes_config.sh` (tar.gz config + sessions every 4h)
- Cron job: `0 */4 * * * $HOME/.hermes/scripts/backup_hermes_config.sh >> /tmp/hermes-backup.log 2>&1`
- Backups stored in `~/.hermes/backups/` with retention of 10 most recent.

**Implementation Note**: Use these wrapper and backup components for production deployments to ensure 24/7 uptime and crash recovery.
