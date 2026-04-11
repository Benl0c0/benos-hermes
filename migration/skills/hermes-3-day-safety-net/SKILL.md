---
name: hermes-3-day-safety-net
category: devops
description: Prevents the 3-day chaos cycle. Covers startup validation, crash recovery, safe model switching, and session continuity.
---

# HERMES 3-DAY SAFETY NET

This skill prevents the system from entering the "3-day chaos" loop where restarts, broken configs, and missing context cause hours of wasted work.

## RULE 0: SESSION START
ALWAYS start Hermes with `hermes --resume`. NEVER with bare `hermes`.
```bash
hermes --resume
```
Why: `resume` preserves config state, session history, and runtime overrides.

## RULE 1: NEVER BREAK THE CONFIG
NEVER use `hermes config set model ...` — it destroys the config dict and turns it into a string.
```bash
# ❌ NEVER DO THIS:
hermes config set model openrouter/qwen3.6-plus:free

# ✅ USE INSTEAD:
hermes --resume
```

## RULE 2: EMERGENCY MODEL SWITCH
If Xiaomi is dead, switch to fallback without breaking config:
```bash
# In-chat (preferred):
/model qwen/qwen3.6-plus:free

# Terminal (if chat is dead):
hermes config set model qwen/qwen3.6-plus:free
hermes --resume
```

## RULE 3: BACKUP BEFORE RISKY OPERATIONS
Before any model switch, config change, or update:
```bash
mkdir -p ~/hermes_backup_$(date +%Y%m%d_%H%M)
cp ~/.hermes/.hermes_history ~/hermes_backup_*/
cp ~/.hermes/state.db ~/hermes_backup_*/
cp ~/.hermes/config.yaml ~/hermes_backup_*/
```

## RULE 4: KILL PROTECTION
Terminal must have Ctrl+C/D protection:
```bash
# Check:
grep 'trap.*INT' ~/.bashrc
grep 'ignoreeof' ~/.bashrc

# If missing, add to ~/.bashrc:
trap 'echo "⚠️ Ctrl-C! Session protected."' INT
set -o ignoreeof
```

## RULE 5: CONFIG HEALTH CHECK
At session start, verify config is a dict, not a string:
```bash
python3 -c "
import yaml
cfg = yaml.safe_load(open('/home/benlo/.hermes/config.yaml'))
m = cfg.get('model', {})
assert isinstance(m, dict), f'BROKEN: model is {type(m).__name__}'
print('✅ Config OK')
"
```

## RULE 6: SMART MODEL ROUTING
- **Complex/Debugging** → Xiaomi MiMo-v2-pro
- **Normal tasks** → Xiaomi MiMo-v2-flash
- **Emergency/OpenRouter** → qwen/qwen3.6-plus:free

## RULE 7: PROVIDER ARCHITECTURE
- Xiaomi = PRIMARY (custom:xiaomi)
- OpenRouter = FALLBACK ONLY
- Config key is `xiaomi` (NOT `custom:xiaomi` in CLI)
- CLI command: `/model mimo-v2-pro --provider xiaomi`

## RULE 8: SESSION RECOVERY
If Hermes crashes:
```bash
# Don't panic. Just resume:
hermes --resume

# If that fails, restore backup:
cp ~/hermes_backup_*/.hermes_history ~/.hermes/
cp ~/hermes_backup_*/state.db ~/.hermes/
cp ~/hermes_backup_*/config.yaml ~/.hermes/
hermes --resume
```

## SUMMARY
The chaos loop: Kill → Start without resume → Lose context → Try to recover → Config breaks → Kill again → Repeat forever.
The fix: Always `resume`, always backup, never `config set model`.

## VERIFICATION
After applying any rule, verify with:
```bash
# Config intact?
python3 -c "import yaml; m=yaml.safe_load(open('/home/benlo/.hermes/config.yaml'))['model']; print(type(m), m.get('provider'), m.get('default'))"

# Session alive?
hermes status

# Xiaomi reachable?
curl -s -H "Authorization: Bearer sk-ejgyeew8nffbd310f2p0fe0u2agvpt54hkr3jxqx4k6nvz8u" https://api.xiaomimimo.com/v1/models | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d['data']), 'models OK')"
```
