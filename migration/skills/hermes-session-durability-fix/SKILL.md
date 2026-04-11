---
name: hermes-session-durability-fix
description: Diagnose and fix session persistence where .hermes_history parsing fails due to format mismatch
tags: [hermes, session, history, recovery, wrapper]
---

## Problem
After crash/session close, all context lost because `.hermes_history` uses V2 format but wrapper expected old format. Session log stayed empty.

## History Formats
Old format: `2026-04-04 14:23:22.422872 | user | Hallo`
New format: `# 2026-04-02 19:18:34.941012\n+Nachrichtentext`

## Solution Steps
1. Read entire `.hermes_history` file content
2. Parse line-by-line:
   - Lines starting with `#` are timestamps
   - Next line starting with `+` is message content
3. Extract last 500 entries as session turns  
4. Write to `session_log.json` (only if empty/idempotent)
5. Add config auto-recovery to `hermes-wrapper` - if config invalid, restore `openrouter/free` default

## Verification
```python
rm ~/.hermes/session_log.json
python3 /tmp/test_wrapper.py
```

## Critical Paths
- Wrapper: `~/.local/bin/hermes-wrapper`  
- History: `~/.hermes/.hermes_history`
- Session log: `~/.hermes/session_log.json`
- Config: `~/.hermes/config.yaml`

## User Context (Ben)
- Frustrated after 7 crashes in one day  
- Has Ubuntu password saved as memory for sudo operations  
- Desktop path in WSL: `/mnt/c/Users/benlo/Desktop/` (not OneDrive path)
- Model: openrouter/free (default fallback)