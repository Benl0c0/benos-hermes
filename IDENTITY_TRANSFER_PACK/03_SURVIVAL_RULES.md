# 03 - SURVIVAL RULES
> Kritische Regeln die Chaos verhindern

════════════════════════════════════════════════════════════════════════════════
## RULE 0: IMMUTABLE LAWS (Brechen = System tot)
════════════════════════════════════════════════════════════════════════════════

### LAW 1: The Resume Command
**ALWAYS use:** `hermes --resume`  
**NEVER use:** Bare `hermes`

WHY:  
- `--resume` preserves: config state, session history, runtime overrides, context
- Bare `hermes` creates blank slate
- Falls back to broken config.yaml
- Hits 429 errors immediately (OpenRouter fallback)
- Repeats chaos cycle

---

### LAW 2: The Config Set Destruction
**NEVER use:** `hermes config set model "custom/xiaomi"` (or similar)  
**WHY IT DESTROYS:**
- Writes simple string into config.yaml
- DELETES entire dictionary structure
- Loses base_url and api_key
- System falls back to OpenRouter immediately
- Hours of debugging to recover

---

### LAW 3: The Free Normalization Bug
**BEWARE:** `:free` suffix in OpenRouter model IDs  
**EXAMPLE:** `qwen/qwen3.6-plus:free`  
**RISK:** Can trigger API errors in model_normalize.py  
**FIXED:** Patch applied, but manual entry still risky

---

### LAW 4: The Three Day Cycle Prevention
**The Chaos Loop:**
```
Kill → Start without resume → Lose context → Try to recover → 
Config breaks → Kill again → Repeat forever
```

**The Fix:**
1. Always `--resume`
2. Always backup before risky ops
3. Never `config set model`

════════════════════════════════════════════════════════════════════════════════
## EMERGENCY PROTOCOLS
════════════════════════════════════════════════════════════════════════════════

### EMERGENCY 1: Bot Unresponsive
```bash
# In-chat (preferred):
/model qwen/qwen3.6-plus:free

# Terminal (if chat dead):
hermes config set model qwen/qwen3.6-plus:free
hermes --resume
```

---

### EMERGENCY 2: Config Corruption
```bash
# Restore from backup:
cp ~/hermes_backup_*/.hermes_history ~/.hermes/
cp ~/hermes_backup_*/state.db ~/.hermes/
cp ~/hermes_backup_*/config.yaml ~/.hermes/
hermes --resume
```

---

### EMERGENCY 3: Session Crash
```bash
# Don't panic. Just resume:
hermes --resume

# If that fails, check backup exists:
ls -la ~/hermes_backup_*/
```

---

### BACKUP BEFORE RISKY OPERATIONS
```bash
mkdir -p ~/hermes_backup_$(date +%Y%m%d_%H%M)
cp ~/.hermes/.hermes_history ~/hermes_backup_*/
cp ~/.hermes/state.db ~/hermes_backup_*/
cp ~/.hermes/config.yaml ~/hermes_backup_*/
```

════════════════════════════════════════════════════════════════════════════════
## CONFIG HEALTH VERIFICATION
════════════════════════════════════════════════════════════════════════════════

### Check 1: Config is Dict (Not String!)
```bash
python3 -c "
import yaml
cfg = yaml.safe_load(open('/home/benlo/.hermes/config.yaml'))
m = cfg.get('model', {})
assert isinstance(m, dict), f'BROKEN: model is {type(m).__name__}'
print('✅ Config OK')
"
```

### Check 2: Session Alive
```bash
hermes status
```

### Check 3: Xiaomi Reachable
```bash
curl -s -H "Authorization: Bearer $XIAOMI_KEY" \
  https://api.xiaomimimo.com/v1/models | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d['data']), 'models OK')"
```

### Check 4: Config Structure
```bash
python3 -c "import yaml; m=yaml.safe_load(open('~/.hermes/config.yaml'))['model']; print(type(m), m.get('provider'), m.get('default'))"
```

════════════════════════════════════════════════════════════════════════════════
## XIAOMI PROVIDER ARCHITECTURE
════════════════════════════════════════════════════════════════════════════════

### Required Structure in config.yaml:
```yaml
model:
  default: mimo-v2-pro
  provider: custom:xiaomi
  base_url: https://api.xiaomimimo.com/v1

custom_providers:
  - name: xiaomi
    base_url: https://api.xiaomimimo.com/v1
    api_key: sk-ejg...vz8u
    model: mimo-v2-pro
```

### auth.json credential pool:
```json
{
  "credential_pool": {
    "custom:xiaomi": {
      "api_key": "sk-...",
      "status": "ok"
    }
  }
}
```

### Activation Command:
```bash
/model mimo-v2-pro --provider xiaomi
```

---

### Model Routing (Smart Selection):
| Task Type | Model | Provider |
|-----------|-------|----------|
| Complex/Debugging | MiMo-v2-pro | xiaomi |
| Normal tasks | MiMo-v2-flash | xiaomi |
| Emergency | qwen/qwen3.6-plus:free | openrouter |

---

### Provider Philosophy:
- **Xiaomi** = PRIMARY (custom:xiaomi)
- **OpenRouter** = FALLBACK ONLY
- Config key is `xiaomi` (NOT `custom:xiaomi` in CLI)

════════════════════════════════════════════════════════════════════════════════
## LESSONS LEARNED (HARD WAY)
════════════════════════════════════════════════════════════════════════════════

### Lesson 1: Telegram Bot Chaos (2026-04-11)

**What Went Wrong:**
1. Doppelter Prozess — `telegram_bot_v2.py` lief parallel zum Gateway
2. Gateway startete in Endlosschleife (Systemd Limit)
3. `pkill` versucht zu stoppen → blockierte Ben

**Root Cause:**
- Zwei verschiedene Bot-Implementierungen
- Keine Prozess-Überwachung
- Keine graceful shutdown Logik

**Solution for New System:**
- NUR EINEN Prozess laufen lassen
- KEINE Endlosschleifen im Startup
- Immer auf Anweisung warten
- Systemd mit proper restart limit

---

### Lesson 2: Config Corruption Chain

**Sequence:**
1. `hermes config set model xiaomi` → converts dict to string
2. Next start → can't find base_url
3. Falls back to OpenRouter
4. Hits 429 rate limit
5. Tries to fix → more config changes
6. Complete corruption

**Prevention:**
- NEVER use `config set model` for custom providers
- ALWAYS use `/model` in-chat for runtime switches
- Backup before ANY config change

---

### Lesson 3: Session Recovery Failure

**Symptom:**  
`hermes --resume` doesn't restore context

**Cause:**  
state.db corruption or history mismatch

**Fix:**
```bash
# Check integrity
sqlite3 ~/.hermes/state.db "PRAGMA integrity_check;"

# If corrupt, restore from latest backup
# (Backups are in ~/.hermes/backups/)
```

---

### Lesson 4: Multi-KI Validation Required

**Rule:** Before trusting major config changes:
1. GPT writes the fix
2. Claude checks and edits  
3. Grok analyzes root cause coverage

**Why:** Single AI perspective misses edge cases

════════════════════════════════════════════════════════════════════════════════
## AUTOMATIC PROTECTIONS (To Implement)
════════════════════════════════════════════════════════════════════════════════

### Ctrl+C / Ctrl+D Protection
```bash
# Add to ~/.bashrc:
trap 'echo "⚠️ Ctrl-C! Session protected. Use exit command."' INT
set -o ignoreeof  # Prevents Ctrl+D from exiting
```

### Session Auto-Backup
```bash
# Cron every 30 min:
*/30 * * * * cp ~/.hermes/state.db ~/.hermes/backups/auto/state_$(date +\%Y\%m\%d_\%H\%M).db
```

### Config Validation Hook
```bash
# Before Hermes start:
python3 -c "import yaml; yaml.safe_load(open('~/.hermes/config.yaml'))" || echo "Config invalid!"
```

════════════════════════════════════════════════════════════════════════════════
## VERIFICATION CHECKLIST (Before Any Major Change)
════════════════════════════════════════════════════════════════════════════════

- [ ] Backup created: `~/hermes_backup_YYYYMMDD_HHMM/`
- [ ] Config validated: `model` is dict, not string
- [ ] Session can resume: `hermes --resume` test
- [ ] Xiaomi reachable: API test successful
- [ ] Fallback ready: OpenRouter key valid (emergency only!)
- [ ] Multi-KI check: Fix reviewed by 2+ AIs
- [ ] Rollback plan: Known working backup identified
