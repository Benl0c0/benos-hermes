# 02 - SKILL LIBRARY
> Alle gelernten Skills und Prozeduren als Text-Bibliothek

════════════════════════════════════════════════════════════════════════════════
## TIER 1: SURVIVAL & SICHERHEIT (Kritisch!)
════════════════════════════════════════════════════════════════════════════════

### hermes-3-day-safety-net
Prevent chaos cycle. Covers startup validation, crash recovery, safe model switching.

GOLDEN RULES:
- ALWAYS: `hermes --resume` (NEVER bare `hermes`)
- NEVER: `hermes config set model ...` — destroys config dict
- Emergency: `/model qwen/qwen3.6-plus:free` (in-chat)

XIAOMI SETUP CHECKLIST:
1. Config.yaml: `model` must be DICTIONARY (not string!)
2. Custom providers entry with base_url required
3. Auth pool must have Xiaomi key under `custom:xiaomi`
4. Activation: `/model mimo-v2-pro --provider custom:xiaomi`

VERIFICATION:
```bash
python3 -c "import yaml; m=yaml.safe_load(open('~/.hermes/config.yaml'))['model']; print(type(m), m.get('provider'))"
```

---

### hermes-survival-guide-lessons-learned
Critical survival rules learned the hard way.

GOLDEN RULES:
1. USE: `hermes --resume` — preserves config state, session history, overrides
2. NEVER: `hermes config set model "custom/xiaomi"`
   → Writes simple string, DELETES entire dictionary structure
   → Result: System loses URL and Key, falls back to OpenRouter
3. BUG: ":free" normalization in model_normalize.py can trigger API errors

EMERGENCY RESET:
- In-chat: `/model qwen/qwen3.6-plus:free`
- Terminal: `hermes config set model qwen/qwen3.6-plus:free && hermes --resume`

MULTI-KI CHECK RULE:
Before trusting major config changes:
1. GPT writes the fix
2. Claude checks and edits
3. Grok analyzes if it actually changes root cause

════════════════════════════════════════════════════════════════════════════════
## TIER 2: ARCHITECTUR & PATTERNS
════════════════════════════════════════════════════════════════════════════════

### benos-agent-patterns
9 proven patterns for agent workflows.

PATTERN 1: Lane-Based FIFO Queuing
- Problem: OpenClaw global lane limits fail (Bug #16055)
- Solution: Dedicated lanes per agent type
  - agent-pri: 2 concurrency (Primary agents)
  - res-*: 4 (Research agents)
  - cnt-*: 4 (Content agents)
  - cron-jobs: 2 (Automation)
  - heartbeat-*: 2 (Monitoring)

PATTERN 2: Heartbeat Optimization (COST CRITICAL!)
- ❌ BAD: Every 30min with full context = $$$$$
- ✅ GOOD: 6-hour minimum, lightContext, isolatedSession
- Output: "HEARTBEAT_OK" only if nothing urgent
- Alert: Telegram ONLY for critical items

PATTERN 3: Context Management (6 Cost Drivers)
1. Context accumulation (40-50%)
2. Tool outputs (20-30%)
3. Systemprompt (10-15%)
4. Reasoning chains (10-15%)
5. Model selection (5-10%)
6. Heartbeat frequency (variable)

Actions:
- Run `/compact` after task completion
- Move status-checks to isolated sessions
- Keep sessions under 50% window usage

PATTERN 4: Cron Job Isolation
- isolatedSession: true
- lightContext: true  
- Dedicated lane (cron-jobs)
- Cheapest model (S1/S2)

PATTERN 5: Sub-Agent Spawning
- Spawn for truly atomic independent tasks
- Must have own lane budget
- Parent waits for completion
- ALWAYS structured JSON output

PATTERN 6: Always-On + Notification
- Use systemd or pm2 for auto-restart
- Critical → Immediate Telegram
- Important → Daily digest
- General → Weekly digest

PATTERN 7: Multi-Agent Protocol
Every agent-to-agent message MUST include:
```json
{
  "task_id": "uuid",
  "from_agent": "agent_name",
  "to_agent": "target_agent",
  "task_type": "research|write|analyze",
  "priority": "S1|S2|S3|S4|S5",
  "context": "minimal|full",
  "output_format": "structured_json",
  "deadline_seconds": 300
}
```

ANTI-PATTERNS (DANGER!):
| Anti-Pattern | Detection | Fix |
|-------------|-----------|-----|
| Expensive models for trivial tasks | Model tier > task level | Apply routing matrix |
| Heartbeats with full context every 30min | interval < 3600 | Set >=21600, isolate |
| All tool outputs stored in context | Session >50% window | Create debug session |
| No lane separation | All default/main lane | Assign specific lanes |
| Missing JSON schemas | Unstructured interfaces | Define schemas |
| Cron jobs in main context | !isolatedSession | Add isolatedSession |

PITFALLS:
- Forgetting lane separation → sub-agents queue up and block
- Running heartbeats too frequent → hundreds of $/month wasted
- Session never compacted → cost explosion over months
- No timeouts on sub-agent calls → permanent hangs
- Ambiguous agent messages → 79% of multi-agent failures

---

### benos-cost-routing
5-Tier routing system (S0-S4).

TIER DEFINITIONS:
| Tier | Model | Cost | Use Case |
|------|-------|------|----------|
| S0 | openrouter/free | $0 | 24/7 background, light tasks |
| S1 | xiaomi/flash | Free | Status checks, heartbeats |
| S2 | xiaomi/v2_omni | $0.4/MT | Summaries, extraction, templates |
| S3 | xiaomi/v2_pro | $1.0/MT | Code, research, analysis |
| S4 | SkillBoss/Opus | Variable | Complex, strategic tasks |

TASK CLASSIFICATION:
| Complexity | Trigger Words | Tier |
|------------|---------------|------|
| Trivial | "status check", "ok?", "ping" | S1 |
| Simple | "summarize", "list files", "extract" | S2 |
| Medium | "scrape", "analyze CSV", "write code" | S3 |
| Complex | "multi-step", "debug complex" | S3/S4 |
| Critical | "strategic", "approve", "irreversible" | S4 + manual approval |

CONTEXT OPTIMIZATION (BEFORE every call):
- Run `/compact` on completed tasks
- Move large outputs to isolated debug sessions
- Strip systemprompt to minimum
- Split multi-step tasks into separate calls
- Threshold: 58%+ context window → compact NOW

HEARTBEAT COST CONTROLS:
```yaml
INTERVAL: minimum 6 hours (NOT 30 minutes!)
CONTEXT: lightContext=true
SESSION: isolatedSession=true
PROMPT: minimal HEARTBEAT.md checklist
RESPONSE: HEARTBEAT_OK nominal, Telegram only urgent
```

CRITICAL: Model changes require Hermes RESTART
- Config changes don't take effect live
- Must: Strg+C → `hermes` (or `hermes --resume`)

PITFALLS:
- S4/S5 for trivial tasks = 5-25x cost
- Heartbeat every 30min with full context = $100s/month
- Context >50% window = exponential cost
- openrouter/free cannot do Vision → use SkillBoss GPT-4o

---

### benos-workflow-prompts
Ready-to-use prompt templates.

SYSTEMPROMPT: KIRA CEO Agent
```
Du bist KIRA, der zentrale orchestrierende Agent von BEN//OS.

AUFGABE:
- Koordination aller Sub-Agents
- Kostenoptimierung: Erste Frage — Kann S1 das lösen?
- Tägliches Reporting an Ben via Telegram
- Eskalation kritischer Probleme sofort

MODELL-ROUTING:
- S1 (kostenlos): Status-Checks, HEARTBEAT_OK, triviale Antworten
- S2 (günstig): Einfache Zusammenfassungen, Datenextraktion
- S3 (mittel): Recherche, strukturierte Analyse
- S4 (Sonnet): Code, Reasoning, Entscheidungen
- S5 (Opus, NUR mit manueller Freigabe): Kritisches

KOMMUNIKATION:
- Output immer als JSON-Schema wenn an andere Agents
- Alle Ergebnisse via Telegram an Ben
- Fehler sofort eskalieren, nicht still ignorieren
```

SYSTEMPROMPT: Research Agent
```
Du bist ein spezialisierter Research-Agent.

AUFGABE: [spezifisch]
INPUT-FORMAT: { "topic": "", "depth": "basic|deep", "sources": [] }
OUTPUT-FORMAT:
{
  "summary": "max 3 Sätze",
  "key_findings": ["finding1", "finding2"],
  "sources": ["url1", "url2"],
  "confidence": 0.0-1.0,
  "next_steps": ["action1"]
}

REGELN:
- Nur verifizierte Informationen
- Keine Halluzinationen — lieber "unbekannt" als falsch
- Token-effizient arbeiten
```

HEARTBEAT TEMPLATE (Optimized):
```
Run every 6 hours:
1. Check email from boss/important contacts only
2. Check calendar for events in next 2 hours
3. Verify active background jobs still running
4. If all clear → respond "HEARTBEAT_OK"
5. If urgent → Telegram alert with summary

Settings:
- model: S1 (free)
- isolatedSession: true
- lightContext: true
- prompt-size: <200 tokens
```

════════════════════════════════════════════════════════════════════════════════
## TIER 3: OPERATIONS & WORKFLOWS
════════════════════════════════════════════════════════════════════════════════

### inbox-processing-sop
Standard Operating Procedure for Ben's Inbox.

TRIGGER PATHS:
- `/mnt/c/Users/benlo/Desktop/Hermes-Inbox/` (recursive)
- Includes: `bens Smartphone - Inbox/`

FILE TYPE HANDLING:
| Type | Tool | Notes |
|------|------|-------|
| Images (.jpg/.png) | SkillBoss Vision (gpt-4o) | Describe layout, text, UI |
| DOCX | docx2txt CLI | NOT python-docx module! |
| PDF | pdftotext command | CLI extraction |
| HTML | browser_navigate | Full structure analysis |
| TXT | Read + follow links | Verify URL destinations |

⚠️ CRITICAL RULE — LINK FOLLOWING:
- ALWAYS open URLs with browser_navigate
- Follow MINIMUM 2 levels deep
- NEVER rate as "trash" just because it "only contains a link"
- A link IS the content gateway
- PITFALL: "please study this" + link → NOT trash, it's valuable info

⚠️ CRITICAL RULE — FULL INSPECTION:
- Never stop at first page/first few lines
- Always read/scroll to end
- If file appears empty/corrupted → FLAG immediately
- Superficial responses FORBIDDEN

RATING SYSTEM (1-10):
- 10 = Gold for system building (bauplan, config, critical instructions)
- 7-9 = Very useful (reference, design specs)
- 4-6 = Background info (tutorials, generic docs)
- 1-3 = Trash (self-tests, duplicates, no value)

IMPORTANT: Rate based on ACTUAL content, not file type!
- Selfie with dashboard in background = 8/10
- Always look beyond the obvious

BATCH MODE ACTIONS:
- `sofort/` — A/8-10 (Immediate action needed)
- `archiv/` — B/6-7 (Store for reference)
- `pruefen/` — C/D/unclear (Manual review)
- `muell/` — E/1-5 useless (Trash)

CRITICAL COMMUNICATION RULES:
- NEVER ask user for API keys/passwords in Telegram
- If message is ambiguous/system error → LOG it, don't reply
- Only reply if explicitly question/command to Hermes

---

### inbox-triage-3-systems
Three-tier inbox classification.

SYSTEMS:
1. **Alarm** — Immediate fix required
2. **Research Pre-processed** — Analyze + Telegram preview
3. **Research Raw** — Rough filing for later

FLOW: File arrives → Auto-classify → Route to appropriate system

---

### inbox-watchdog
Folder monitoring automation.

MONITORS:
- `Hermes-Inbox/` — Main drop folder
- `bensmartphone-inbox/` — Phone sync folder

ACTION: New file detected → Trigger processing pipeline

════════════════════════════════════════════════════════════════════════════════
## TIER 4: HARDWARE & SETUP
════════════════════════════════════════════════════════════════════════════════

### config-xiaomi-mimo
Safely add/update Xiaomi MiMo provider.

STEPS:
1. Backup `~/.hermes/config.yaml`
2. Add custom provider entry in `custom_providers:`
3. Set `base_url: https://api.xiaomimimo.com/v1`
4. Update `auth.json` credential pool with `custom:xiaomi`
5. Set `model.provider` to `custom:xiaomi`
6. Test with lightweight task first

VERIFICATION:
```bash
curl -s -H "Authorization: Bearer $KEY" \
  https://api.xiaomimimo.com/v1/models | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d['data']), 'models OK')"
```

---

### wsl-nightmode-setup
Keep WSL running 24/7 while display off.

USE CASE: Ben's Nachtmodus.bat
- Bildschirm aus
- Laptop läuft weiter
- WSL2 + Hermes durchlaufen

════════════════════════════════════════════════════════════════════════════════
## TIER 5: TELEGRAM ECOSYSTEM
════════════════════════════════════════════════════════════════════════════════

### hermes-telegram-integration
Core Telegram Bot setup and health.

COMPONENTS:
- Bot health checks
- Heartbeat integration
- Command reception
- Inbound message polling

---

### telegram-alerts
Configure notifications for Hermes events.

TYPES:
- Critical → Immediate
- Warning → Batch digest
- Info → Weekly summary

---

### telegram-command-center
Robust bot daemon with SQLite persistence.

FEATURES:
- Message queue
- Auto-acknowledge
- Rate limiting
- Error recovery

---

### telegram-vision-voice-bot
Vision AI + Voice TTS with async processing.

CAPABILITIES:
- Image analysis via SkillBoss
- Voice message transcription
- TTS replies
- Async queue handling

---

### telegram-voice-tts
Voice message reception and TTS replies.

════════════════════════════════════════════════════════════════════════════════
## TIER 6: HERMES SYSTEM OPERATIONS
════════════════════════════════════════════════════════════════════════════════

### hermes-github-setup
GitHub access configuration.

RESULT (2026-04-11):
- SSH verified (Benl0c0)
- Git credential helper = store
- SSH rewrite configured
- User: Benl0c0
- Email: benloco187@googlemail.com

---

### hermes-model-session-management
Safe model switching and session continuity.

RULES:
- Always `--resume` never bare start
- Test new models with lightweight tasks
- Keep fallback ready

---

### hermes-provider-auth-pool-fix
Diagnose/fix provider exchange in auth.json.

ISSUES ADDRESSED:
- Credential pool corruption
- Provider key mismatches
- Fallback chain failures

---

### hermes-provider-switch-runtime
Safe non-destructive provider switching.

METHOD:
- Runtime override (not config change)
- Preserves fallback chain
- Rollback capability

---

### hermes-session-durability-fix
Fix session persistence failures.

---

### hermes-usage-tracking
Token usage logging and budget control.

---

### hermes-wrapper-durability-enhancement
Fixes session persistence and config corruption.

════════════════════════════════════════════════════════════════════════════════
## TIER 7: BEN//OS SPECIALIZED
════════════════════════════════════════════════════════════════════════════════

### benos-kira-architecture
Hierarchical multi-agent system.

### benos-live-dashboard
Live dashboard components.

### benos-multi-agent-protocol
Agent-to-agent communication schemas.

### benos-tools-knowledge
Tools & APIs quick reference.

---

### skillboss / skillboss-integration
Premium model API wrapper.

USE: On-demand S4/S5 tasks without restart
Vision: GPT-4o for image analysis

---

### generate-system-blueprint
Structured technical system blueprints.

---

### dogfood
Exploratory QA testing methodology.

---

### telecom-provider-config-separation
Clean separation of OpenRouter and Xiaomi configs.

---

### smart-inbox-pipeline
Two-way inbox processing concept.

════════════════════════════════════════════════════════════════════════════════
## TIER 8: PLATFORM SPECIFIC (WSL LEGACY)
════════════════════════════════════════════════════════════════════════════════

### wsl-desktop-sync
Create folders visible on Windows Desktop.

### wsl-pc-maintenance
WSL system maintenance guide.

NOTE: These are WSL-specific. May not apply to Hostinger VPS.
