---
name: benos-cost-routing
description: BEN//OS cost-routing skill. Routes tasks to the cheapest appropriate model (S1-S5) and applies context-optimization techniques before every agent call. Prevents cost explosions from context bloat, wrong model choice, and unchecked heartbeats.
version: 1.0.0
author: Hermes Agent (from BEN//OS Wissensbasis)
license: MIT
metadata:
  hermes:
    tags: [BEN//OS, Cost, Routing, Model-Selection, Context-Optimization, Token-Costs]
    related_skills: [benos-agent-patterns, benos-kira-architecture]
    source: /mnt/c/Users/benlo/Desktop/Hermes-Inbox/Good to know/
---

# BEN//OS Cost Routing

## Trigger Conditions
- User asks to execute a task that could use different model tiers
- Planning a new automated workflow (cron, heartbeat, sub-agent)
- Reviewing or estimating token costs for a project
- Context window is approaching 50%+ of limit (check via session state)

## Implementation: The 5-Tier Routing System

**Config files:**
- `~/.hermes/config.yaml` - default model (what the agent uses for normal calls)
- `~/hermes-base/scripts/model-boost.sh` - manual boost switcher
- `~/.hermes/model-router-report.json` - daily health check report

### Tier Definitions

| Tier | Mode | Model | Cost | Use Case |
|------|------|-------|------|----------|
| S0 | Free | openrouter/free (auto-switch) | $0 | 24/7 background, light tasks |
| S1 | Flash | xiaomi/flash | Free | Status checks, simple ops, heartbeats |
| S2 | Normal | xiaomi/v2_omni | $0.4/MT | Summaries, extraction, templates |
| S3 | Power | xiaomi/v2_pro | $1.0/MT | Code, research, analysis, dashboards |
| S4 | Boost | SkillBoss (Opus/GPT-4/etc) | Variable | Complex, strategic tasks (on-demand) |

### Auto-Switch Logic (when Free exhausted)

If S0 (openrouter/free) fails 3 times in a session → auto-promote to S1 (Flash). Track via session state.

### Boost Modes

Two distinct boost mechanisms:

1. **Session Boost** (`./model-boost.sh pro` / `./model-boost.sh skillboss`)
   - Changes default model in `config.yaml`
   - Persists across session restarts
   - Requires manual Hermes restart (`Strg+C`, then `hermes`)
   - Use: "Ich brauch jetzt Big-Power für heute"

2. **SkillBoss On-Demand**
   - Default remains S3 (Pro), but you can invoke SkillBoss for specific tasks:
     ```bash
     skillboss run "komplexe Aufgabe" -m opus-4
     ```
   - Cost: Only for that call
   - Use: "SkillBoss, analysiere diesen Codebase"

## Step 1: Classify Task Complexity

Before calling any model, classify the task:

| Complexity | Tier | Decision Trigger |
|------------|------|-----------------|
| Trivial | S1 | "status check", "ok?", "ping", "confirm" |
| Simple | S2 | "summarize", "list files", "extract dates", "fill template" |
| Medium | S3 | "scrape", "analyze CSV", "write code function", "build dashboard" |
| Complex | S3/S4 | "multi-step workflow", "debug complex error", "design architecture", "research report" |
| Critical | S4 | "strategic decision", "approve", "irreversible", "final deliverable" |

**Rule:** Start at lowest tier, escalate only if inadequate response.

## Step 2: Apply Routing Decision

```
Task assessment checklist:
1. Does this require reasoning/code?  → S4
2. Does this require deep research?  → S3
3. Is this a simple lookup/summary?  → S2
4. Is this a status check/ack?       → S1
5. Is this strategic/irreversible?   → S5 (stop—get manual approval first)
```

## Step 3: Optimize Context Before Call

The 6 cost drivers in order of impact:
1. Context accumulation (40-50%)
2. Tool outputs (20-30%)
3. Systemprompt (10-15%)
4. Reasoning chains (10-15%)
5. Model choice (5-10%)
6. Heartbeat/Cron frequency (variable)

Apply these optimizations BEFORE making any model call:
- Run `/compact` on sessions that have completed their tasks
- Move large tool outputs (status --all, JSON dumps) to isolated debug sessions
- Strip systemprompt to minimum required for the task
- Split multi-step tasks into separate calls instead of one mega-prompt
- Use observation-masking to hide irrelevant context sections
- Set threshold: If session uses 58%+ of context window, compact immediately
- After session completes, `hermos archive` to freeze context

## Step 4: Heartbeat Cost Controls

When creating a heartbeat/cron:
```
INTERVAL: minimum 6 hours (NOT 30 minutes)
CONTEXT: enable lightContext
SESSION: enable isolatedSession
PROMPT: keep HEARTBEAT.md minimal (checklist only)
RESPONSE: HEARTBEAT_OK for nominal, Telegram alert only for urgent
```

## Implementation Commands

```bash
# Switch to S3 (Power mode) – persists across sessions
~/hermes-base/scripts/model-boost.sh pro

# Switch to S1 (Flash) – cheap
~/hermes-base/scripts/model-boost.sh flash

# Reset to Free (safe default)
~/hermes-base/scripts/model-boost.sh reset

# After any model-boost change: restart Hermes (Strg+C, then hermes)

# Run daily router health check manually
python3 ~/hermes-base/scripts/model-router-check.py
# Report: ~/.hermes/model-router-report.json
```

## Step 4: Heartbeat Cost Controls

If creating or configuring a heartbeat:
```
INTERVAL: minimum 6 hours (NOT 30 minutes)
CONTEXT: enable lightContext
SESSION: enable isolatedSession
PROMPT: keep HEARTBEAT.md minimal (checklist only)
RESPONSE: HEARTBEAT_OK for nominal, Telegram alert only for urgent
```

## Critical: Model Switching Requires Session Restart

Changing `config.yaml` (via `model-boost.sh` or manual edit) does NOT take effect in the current session.
The Hermes gateway loads the config at startup only. You MUST:
1. Kill the current session (Strg+C)
2. Restart Hermes (`hermes`)

There is no live-switch mechanism built in yet. This is a known limitation.
Workarounds:
- Use SkillBoss API calls directly for premium model needs (doesn't require restart)
- Plan model boosts before starting complex tasks

## SkillBoss GPT-4o Vision for Design Tasks

Instead of writing CSS/HTML yourself, delegate design work to GPT-4o via SkillBoss:
```python
# 1. Encode screenshot as base64
import base64
with open("screenshot.png", "rb") as f:
    b64 = base64.b64encode(f.read()).decode()

# 2. Call SkillBoss with Vision
import json, urllib.request
payload = {
    "model": "openai/gpt-4o",
    "messages": [
        {"role": "system", "content": "You are a coding machine. Output ONLY HTML code."},
        {"role": "user", "content": [
            {"type": "text", "text": "Describe and recreate this dashboard design as a single HTML file..."},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}", "detail": "high"}}
        ]}
    ],
    "max_tokens": 8192
}
# ... send to https://api.heybossai.com/v1/chat/completions
```
**Cost:** ~$0.05-0.15 per call. Much faster and better quality than manual writing.

## Pitfalls
- Using S4/S5 for trivial tasks = 5-25x unnecessary cost
- Heartbeat every 30min with full context = hundreds of dollars/month
- Letting session context grow past 50% of window = exponential cost increase
- Storing all tool outputs in main session context = context explosion
- No lane separation between agents = blocking + wasted retries
- Running heartbeats before optimizing = guaranteed money burn
- **Model config changes require Hermes restart** - no live-switch yet
- **openrouter/free cannot do Vision** - use SkillBoss GPT-4o for image analysis
- **Duplicate files in inbox are NOT automatically useless** - they may contain improvements/variants
- **Screenshots without code need Vision analysis** - convert them to text specs first

## Daily Model Router Agent

Run daily (6am via cronjob) to keep model landscape up-to-date:

```bash
# Prüft alle APIs, scannt OpenRouter free models
python3 ~/hermes-base/scripts/model-router-check.py

# Output: ~/.hermes/model-router-report.json
```

The report contains:
- API status (Xiaomi, OpenRouter, Venice, etc.)
- Count of newly available free models
- Recommendations for auto-switching thresholds

## Verification
After routing a task:
- [ ] Model tier matches actual task complexity (not defaulted to highest)
- [ ] Session context < 50% of window before call
- [ ] /compact applied to completed sessions
- [ ] Heartbeats configured with lightContext + isolatedSession
- [ ] No tool outputs >1MB stored in main session context
- [ ] Daily router report reviewed for new free models
