---
name: telegram-bot-xiaomi-provider-setup
description: Configure Hermes Telegram Bot to use Xiaomi MiMo V2 Pro provider instead of OpenRouter, ensuring clean separation and verification.
tags:
  - telegram
  - provider
  - xiaomi
---

## Trigger Conditions
- You need to switch the Telegram bot from OpenRouter Free to Xiaomi MiMo V2 Pro.
- The bot code (`telegram_bot_v2.py`) already supports provider selection via config.yaml.
- You want to avoid mixing OpenRouter and Xiaomi endpoints.
- You need to verify the active provider with a real API request.

## Prerequisites
- `telegram_bot_v2.py` exists and is functional (syntax OK).
- Xiaomi API key is available (`sk-...`).
- Telegram bot token is valid (stored in `~/.hermes/telegram_token.conf` or `.env`).
- Only one bot process will run (duplicate processes cause issues).

## Steps

### 1. Update config.yaml for strict Xiaomi separation
Edit `~/.hermes/config.yaml` and ensure the `model` section is exactly:

```yaml
model:
  provider: xiaomi
  base_url: https://api.xiaomimimo.com/v1
  default: mimo-v2-pro   # or mimo-v2-flash / mimo-v2-omni
  max_tokens: 4000
  providers:
    xiaomi:
      api_key: ${XIAOMI_API_KEY}
      base_url: https://api.xiaomimimo.com/v1
      models:
        v2_pro:
          model_id: mimo-v2-pro
          # ... other model params if needed
    openrouter:
      api_keys:
        - ${OPENROUTER_API_KEY}
```

**Critical:** Do NOT set `provider: openrouter` while using Xiaomi `base_url`. That mix causes the bot to use OpenRouter auth headers on the Xiaomi endpoint → 401/403 errors. Keep OpenRouter and Xiaomi completely separate.

### 2. Set Xiaomi API Key in .env
Add or update `~/.hermes/.env`:
```bash
echo "XIAOMI_API_KEY=sk-..." >> ~/.hermes/.env
```
If `.env` is readonly, you may need to adjust permissions or store the key in an alternative location that the bot reads (the bot reads `.env` directly).

### 3. Stop any existing bot processes
```bash
pkill -f telegram_bot_v2.py
```
Verify none remain: `pgrep -f telegram_bot_v2.py` should return nothing.

### 4. Start the bot fresh
```bash
nohup python3 -u ~/.hermes/scripts/telegram_bot_v2.py > /tmp/tg_bot.log 2>&1 &
```
Check startup log: `tail -5 /tmp/tg_bot.log`. Should show token loaded and "Listening...".

### 5. Verify with a real Xiaomi API request (not just config read)
The bot's `_query_agent()` reads config.yaml and uses the provider to route requests. To confirm the configuration is active, make an actual API call to Xiaomi using the same credentials the bot would use.

**Using curl:**
```bash
API_KEY=$(grep '^XIAOMI_API_KEY=' ~/.hermes/.env | cut -d= -f2)
curl -s -X POST https://api.xiaomimimo.com/v1/chat/completions \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"mimo-v2-pro","messages":[{"role":"user","content":"Test"}],"max_tokens":10}'
```
Expected response: HTTP 200 with JSON containing `choices[0].message.content` (non-empty).

**Using Python (execute_code):**
```python
import subprocess, json, os
api_key = os.getenv('XIAOMI_API_KEY') or from .env
# ... same as above
```

If this request fails with 401/403, the API key is wrong or not set. If 429, rate-limited – wait or add credits. If 200, the Xiaomi provider is reachable and configured correctly.

### 6. End-to-end Telegram test
- In Telegram, send `/start` to your bot (if first use).
- Send a text message like `test`.
- Check bot log: it should show receiving the message and sending a reply.
- Verify the reply appears in Telegram.

Success criteria: Text roundtrip works with Xiaomi backend.

## Pitfalls
- **Mixed provider config:** `model.provider=openrouter` but `model.base_url` set to Xiaomi URL → bot uses OpenRouter headers on Xiaomi endpoint → auth fails. Always set `provider: xiaomi` when using Xiaomi URL.
- **Incorrect model name:** Xiaomi expects `mimo-v2-pro`, `mimo-v2-flash`, or `mimo-v2-omni`. Using `v2_pro` only will fail.
- **Missing API key:** Bot will reply with error message `Kein Xiaomi API Key (XIAOMI_API_KEY).` Ensure `.env` line is present and not masked by file permissions.
- **Multiple bot processes:** More than one `telegram_bot_v2.py` causes duplicate offset handling and missed updates. Kill all before restart.
- **Stale state:** If bot receives 0 updates after starting, delete `~/.hermes/.telegram_bot_state.json` and `~/.hermes/telegram_queue.db` then restart.
- **Rate limits:** Xiaomi may have per-minute or daily limits. Handle 429 by backing off or adding credits.
- **OpenRouter still referenced:** The bot code may have hardcoded fallbacks; `_query_agent()` in `telegram_bot_v2.py` respects config, but older versions might not. Ensure you are using the version that contains the provider selection logic (the one with `if provider == 'xiaomi'`).

## Verification Checklist
- [ ] `config.yaml`: `model.provider=xiaomi`, `model.base_url=https://api.xiaomimimo.com/v1`, `model.default=mimo-v2-pro`
- [ ] `.env` contains `XIAOMI_API_KEY=sk-...`
- [ ] Only one `telegram_bot_v2.py` process (`pgrep -fc telegram_bot_v2` returns 1)
- [ ] Real curl request to Xiaomi endpoint returns 200 and non-empty content
- [ ] Bot receives Telegram text and replies successfully

## Outcome
Telegram bot operates fully on Xiaomi MiMo V2 Pro, with verified API connectivity and working message roundtrip.
