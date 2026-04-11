# 05 - TECH SPECS
> Technische Konfigurationen, Provider-Setup, Model-Routing

════════════════════════════════════════════════════════════════════════════════
## PROVIDER ARCHITECTURE
════════════════════════════════════════════════════════════════════════════════

### Primary: Xiaomi MiMo
**Models:**
- `mimo-v2-flash` — Fast, cheap, good for most tasks
- `mimo-v2-pro` — More capable, reasoning, code

**API:** https://api.xiaomimimo.com/v1  
**Status:** PAID (Ben has subscription)  
**Priority:** ALWAYS first choice

### Fallback: OpenRouter (Emergency Only!)
**Model:** `qwen/qwen3.6-plus:free`  
**Status:** FREE tier  
**Limitations:**  
- Rate limits (429 errors)
- No vision support
- Unreliable
**Use:** ONLY when Xiaomi is completely down

**Ben's Order (2026-04-11):**
> "Ben will kein OpenRouter mehr nutzen. Nur Xiaomi MiMo. 
> Keine Mischung mehr. 'OpenRouter macht nur Probleme'"

→ OpenRouter = strict emergency fallback only!

════════════════════════════════════════════════════════════════════════════════
## CONFIG.YAML STRUCTURE
════════════════════════════════════════════════════════════════════════════════

### Correct Dict Structure (DO NOT STRINGIFY!)
```yaml
model:
  default: mimo-v2-pro
  provider: custom:xiaomi
  base_url: https://api.xiaomimimo.com/v1

custom_providers:
  - name: xiaomi
    base_url: https://api.xiaomimimo.com/v1
    api_key: sk-xxxxxxxxxxxxxxxx  # From auth.json pool
    model: mimo-v2-pro

# Other config sections...
```

### ❌ WRONG (Destroys System):
```yaml
model: custom:xiaomi  # STRING! Destroys everything!
```

### ✅ CORRECT (Preserves Structure):
```yaml
model:
  default: mimo-v2-pro
  provider: custom:xiaomi
  base_url: https://api.xiaomimimo.com/v1
```

════════════════════════════════════════════════════════════════════════════════
## AUTH.JSON STRUCTURE
════════════════════════════════════════════════════════════════════════════════

### Credential Pool:
```json
{
  "credential_pool": {
    "openrouter": {
      "api_key": "sk-or-...",
      "status": "ok"
    },
    "custom:xiaomi": {
      "api_key": "sk-ejg...vz8u",
      "status": "active"
    }
  },
  "active_provider": "custom:xiaomi",
  "fallback_chain": ["custom:xiaomi", "openrouter"]
}
```

**Key Mapping:**
- `custom:xiaomi` — Xiaomi MiMo V2 provider
- `openrouter` — Emergency fallback

════════════════════════════════════════════════════════════════════════════════
## MODEL SWITCHING
════════════════════════════════════════════════════════════════════════════════

### Runtime Switch (In-Chat):
```bash
# To Xiaomi Pro:
/model mimo-v2-pro --provider xiaomi

# To Xiaomi Flash:
/model mimo-v2-flash --provider xiaomi

# Emergency fallback:
/model qwen/qwen3.6-plus:free
```

### Config Change (Requires Restart!):
```bash
# Edit config.yaml manually
# Then:
Ctrl+C  # Kill session
hermes --resume  # Restart with new config
```

**⚠️ WARNING:** Config changes DON'T take effect live!
Hermes loads config only at startup.

════════════════════════════════════════════════════════════════════════════════
## COST ROUTING TIERS (S0-S4)
════════════════════════════════════════════════════════════════════════════════

| Tier | Model | Cost/MT | Use Case |
|------|-------|---------|----------|
| S0 | openrouter/free | $0 | 24/7 background ONLY |
| S1 | xiaomi/flash | ~$0.10 | Status checks, heartbeats |
| S2 | xiaomi/v2_omni | ~$0.40 | Summaries, extraction |
| S3 | xiaomi/v2_pro | ~$1.00 | Code, research, analysis |
| S4 | SkillBoss/Opus | Variable | Complex, strategic |

### Task Classification:
```
Question before every call:
"Can S1 solve this?"
→ YES → Use S1
→ NO → "Can S2 solve this?"
  → YES → Use S2
  → NO → "Need S3 or higher?"
```

### Cost Drivers (Impact Order):
1. Context accumulation (40-50%)
2. Tool outputs (20-30%)
3. Systemprompt (10-15%)
4. Reasoning chains (10-15%)
5. Model choice (5-10%)
6. Heartbeat frequency (variable)

════════════════════════════════════════════════════════════════════════════════
## HEARTBEAT CONFIGURATION
════════════════════════════════════════════════════════════════════════════════

### Optimized Settings:
```yaml
heartbeat:
  interval: 21600  # 6 hours (MINIMUM!)
  model: S1  # Cheapest available
  isolatedSession: true
  lightContext: true
  prompt: |
    1. Check email from boss/important only
    2. Check calendar next 2 hours
    3. Verify background jobs running
    4. If clear → "HEARTBEAT_OK"
    5. If urgent → Telegram alert
```

### ❌ EXPENSIVE (Don't Do):
```yaml
heartbeat:
  interval: 1800  # 30 minutes = $100s/month!
  model: S3  # Overkill
  isolatedSession: false  # Context bloat
```

════════════════════════════════════════════════════════════════════════════════
## TELEGRAM INTEGRATION
════════════════════════════════════════════════════════════════════════════════

### Bot Configuration:
```yaml
telegram:
  bot_name: Hermes
  chat_id: 2029024880
  token: ${TELEGRAM_TOKEN}  # From .env
  enabled: true
  notification_levels:
    critical: immediate
    warning: digest
    info: weekly
```

### Required Files:
- `~/.hermes/.env` — TELEGRAM_TOKEN=xxx
- `~/.hermes/telegram_token.conf` — Backup location
- Permissions: 600 (owner read only)

### Token Storage for Cron:
Token MUST be in `config/.env` for cron jobs to access it.

════════════════════════════════════════════════════════════════════════════════
## CRON JOB SETUP
════════════════════════════════════════════════════════════════════════════════

### Isolation Requirements:
```yaml
cron:
  job_name:
    schedule: "0 */6 * * *"  # Every 6 hours
    lane: cron-jobs
    model: S1
    isolatedSession: true    # REQUIRED!
    lightContext: true       # REQUIRED!
    script: /path/to/job.py
```

### Why Isolation:
- Without isolation: Full context loaded = $$$ per run
- With isolation: Minimal context = $ per run
- Savings: 10-50x cost reduction

════════════════════════════════════════════════════════════════════════════════
## POST-MIGRATION SETUP CHECKLIST
════════════════════════════════════════════════════════════════════════════════

### 1. Install Core:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3 python3-pip git curl sqlite3 tmux

# Hermes Agent
git clone https://github.com/NousResearch/hermes-agent.git ~/.hermes/hermes-agent
cd ~/.hermes/hermes-agent
pip install --user -e .
```

### 2. Copy Identity Pack:
```bash
git clone https://github.com/Benl0c0/benos-hermes.git ~/benos-hermes
cp ~/benos-hermes/IDENTITY_TRANSFER_PACK ~/identity/ -r
```

### 3. Install Secrets (MANUAL!):
```bash
# TODO BEN: Create these files with actual keys:
# ~/.hermes/auth.json
# ~/.hermes/.env
# ~/.hermes/telegram_token.conf
# ~/.ssh/id_rsa (if using Git SSH)
```

### 4. Copy Clean Config:
```bash
# Clean config from pack:
cp ~/identity/config/config.yaml ~/.hermes/config.yaml

# THEN: Add actual keys to auth.json (not config.yaml!)
```

### 5. Verify Structure:
```bash
# Check config is dict:
python3 -c "import yaml; m=yaml.safe_load(open('~/.hermes/config.yaml'))['model']; print(type(m))"
# Should print: <class 'dict'>

# Check auth.json:
cat ~/.hermes/auth.json | python3 -m json.tool
```

### 6. Test Xiaomi:
```bash
curl -s -H "Authorization: Bearer $XIAOMI_KEY" \
  https://api.xiaomimimo.com/v1/models | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print('OK:', len(d['data']), 'models')"
```

### 7. First Start:
```bash
# Start with --resume (even for first time, creates session)
hermes --resume

# In chat, test model:
/model mimo-v2-flash --provider xiaomi

# Verify:
/status
```

### 8. Enable Gateway:
```bash
# Start gateway (for Telegram)
hermes gateway start

# Or via systemd (recommended):
sudo systemctl enable --now hermes-gateway
```

### 9. Test Telegram:
```bash
# Send test message
hermes telegram "Hermes online on Hostinger VPS ✅"
```

### 10. Setup Cron:
```bash
# Add to crontab:
*/10 * * * * python3 ~/inbox-processor/inbox_processor.py
0 */6 * * * hermes heartbeat
```

════════════════════════════════════════════════════════════════════════════════
## SECURITY NOTES
════════════════════════════════════════════════════════════════════════════════

### File Permissions:
```bash
chmod 600 ~/.hermes/auth.json
chmod 600 ~/.hermes/.env
chmod 600 ~/.hermes/telegram_token.conf
chmod 700 ~/.hermes/
```

### No Keys in Git:
- ✅ Core identity files
- ✅ Skill documentation
- ❌ auth.json (API keys)
- ❌ .env (environment secrets)
- ❌ telegram_token.conf

### SSH Keys:
If using GitHub SSH:
```bash
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
chmod 700 ~/.ssh/
```

════════════════════════════════════════════════════════════════════════════════
## ROLLBACK PLAN
════════════════════════════════════════════════════════════════════════════════

### If Setup Fails:
```bash
# 1. Kill Hermes
pkill -f hermes

# 2. Restore backup
cp ~/hermes_backup_*/config.yaml ~/.hermes/
cp ~/hermes_backup_*/auth.json ~/.hermes/

# 3. Resume
hermes --resume
```

### Emergency Fallback:
```bash
# If Xiaomi completely broken:
hermes config set model qwen/qwen3.6-plus:free
hermes --resume
# Then fix Xiaomi config
```

════════════════════════════════════════════════════════════════════════════════
## POST-STARTUP VERIFICATION
════════════════════════════════════════════════════════════════════════════════

After Hermes is running, verify:

```bash
# 1. Config health
python3 -c "import yaml; m=yaml.safe_load(open('~/.hermes/config.yaml'))['model']; assert isinstance(m, dict)"

# 2. Provider connectivity
curl -H "Authorization: Bearer $KEY" https://api.xiaomimimo.com/v1/models

# 3. Session active
hermes status

# 4. Telegram working
hermes telegram "Test message"

# 5. Skills available
hermes skills list

# 6. Inbox processor ready
ls ~/inbox/
```

All green? ✅ System ready.
