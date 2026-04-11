---
name: hermes-usage-tracking
description: Token usage logging and budget control for multi-provider API costs (Xiaomi MiMo + OpenRouter). Tracks prompt/completion tokens, calculates costs using model price catalog, enforces budget limits ($5 hard limit, $4 warning), and generates monthly reports.
tags: [cost-control, monitoring, xiaomi, openrouter]
related_skills: [benos-cost-routing, config-xiaomi-mimo]
source_files:
  - ~/.hermes/usage_tracker.py
  - ~/.hermes/model_prices.json
  - ~/.hermes/usage_tracking.json
---

# Hermes Usage Tracking

## Purpose
Track API token usage across providers, calculate costs, enforce budget limits, and generate reports.

## Files

### Core Skript
- `~/.hermes/usage_tracker.py` - Python module with UsageTracker class
- `~/.hermes/model_prices.json` - Price catalog for all models
- `~/.hermes/usage_tracking.json` - Current month usage data (auto-updated)

### CLI Commands
```bash
hermes-usage status     # Show current usage overview
hermes-usage report     # Detailed monthly report with breakdowns  
hermes-usage log <model> <prompt_tokens> <completion_tokens>  # Manual entry
hermes-usage reset --confirm   # Clear current month
hermes-usage thresholds        # View/configure warning and limit values
hermes-usage check --model xiaomi/mimo-v2-pro  # Dry-run budget check
```

## Pricing Model
| Model | Input ($/1M) | Output ($/1M) | Tier |
|-------|-------------|---------------|------|
| mimo-v2-flash | 0.00 | 0.00 | S1 (Free) |
| mimo-v2-omni | 0.40 | 2.00 | S2 |
| mimo-v2-pro | 1.00 | 3.00 | S3 |
| openrouter/free | 0.00 | 0.00 | S1 |

## Budget Controls
- Warning threshold: $4.00 (triggers alert)
- Hard limit: $5.00 (blocks non-free calls, suggests free alternative)
- Free tier calls always allowed regardless of budget
- Monthly rollover with archiving to `~/.hermes/usage_archive/`

## Python Integration
```python
from usage_tracker import log_api_call, check_budget

# Log after API response
ok, msg, cost = log_api_call(
    model="xiaomi/mimo-v2-pro", 
    prompt_tokens=1500, 
    completion_tokens=800
)

# Pre-check before expensive call
ok, msg, free_alt = check_budget("xiaomi/mimo-v2-pro")
if not ok:
    print(f"Budget exceeded. Use free instead: {free_alt}")
```

## Cost Calculation
```
input_cost = (prompt_tokens / 1_000_000) * input_price
output_cost = (completion_tokens / 1_000_000) * output_price 
total = input_cost + output_cost
```

## Verification
```bash
cat ~/.hermes/usage_tracking.json | python3 -m json.tool  # Valid JSON
hermes-usage status  # Shows current totals
hermes-usage report  # Shows full monthly breakdown
```

## Cron-Based Delivery (Working Approach)
The working delivery method uses the cronjob tool — NOT wrapper hooks.

### Active Jobs
- **Hourly Report** (ID: `d6fcc3ebf684`): Runs every hour, sends usage to Telegram
- **Daily Digest** (ID: `add0cadcf601`): Runs at 22:00, full report to Telegram

### Status Script
```bash
python3 ~/.hermes/scripts/hermes-usage-status.py
```

### Manage Cron Jobs
```bash
cronjob action=list              # View all jobs
cronjob action=pause job_id=X    # Pause a job
cronjob action=resume job_id=X   # Resume it
```

## Free-Tier Usage Tracking (OpenRouter)
Free models (S0/openrouter/free) show 0 in local usage_tracking.json because `log_call()` is NOT invoked for them.

### How to check actual Free-Tier usage
```bash
# Read key from .env, query OpenRouter Credits API
python3 ~/.hermes/scripts/hermes-usage-status.py
```
This calls `GET https://openrouter.ai/api/v1/credits` which returns:
- `total_credits`: Always $0 for free accounts
- `total_usage`: Total USD spent on all free model API calls

### Supplementing Free-Tier Data in Reports
For a complete report showing both paid AND free usage:
1. Query OpenRouter Credits API: `GET /credits` returns `total_usage`
2. Merge with local `usage_tracking.json` (paid calls)
3. Report them separately: "Paid: $X.XX | Free: $X.XX (OpenRouter)"

The OpenRouter Credits API is THE authoritative source for free-tier aggregate usage. Do NOT pollute usage_tracking.json with $0-cost free calls — it breaks cost calculations and reporting.

## Script: OpenRouter Free Usage Fetcher
```python
import os, requests

def fetch_openrouter_free_usage():
    env_path = os.path.expanduser("~/.hermes/.env")
    token = None
    with open(env_path) as f:
        for line in f:
            if line.startswith("OPENROUTER_API_KEY"):
                token = line.split("=", 1)[1].strip()
                break
    if not token:
        return {"error": "No OPENROUTER_API_KEY"}
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get("https://openrouter.ai/api/v1/credits", headers=headers, timeout=10)
    return r.json().get("data", {})
```

## Pitfalls
- CLI needs execute permission: `chmod +x ~/.hermes/bin/hermes-usage`
- Ensure `~/.hermes/bin` is in PATH
- Price catalog must be updated when providers change prices
- usage_tracker.py is in ~/.hermes/ but NOT in Python site-packages — standalone use only (sys.path insert needed)
- hermes-wrapper has NO usage_tracker hook — Cron delivery is the working integration method, skip wrapper modification
- Cron jobs auto-deliver to Telegram (chat_id: 2029024880), no manual piping needed
- Budget tracking file resets on month rollover — old data archived to ~/.hermes/usage_archive/
- CRITICAL: Free model usage is NOT tracked in usage_tracking.json — this is BY DESIGN — $0 calls would pollute the reports and break cost accounting. Use OpenRouter /credits API for free-tier totals instead.
- Xiaomi/MiMo usage tracking integration pending test: verify that `log_api_call` hooks are triggered for Xiaomi provider calls and that token counts are captured correctly. See `~/.hermes/logs/pending_tests.txt` for notes.
- NEVER inject $0 free calls into usage_tracking.json — this is intentionally empty for free models