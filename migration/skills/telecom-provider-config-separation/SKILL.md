---
name: telecom-provider-config-separation
description: Clean separation of OpenRouter Free and Xiaomi MiMo V2 Pro as independent AI providers in config.yaml — ensures correct routing, prevents API key/URL confusion.
---

## Trigger Conditions
- `429 Rate Limit` errors from OpenRouter Free
- `Unknown provider 'xiaomi'` errors
- API calls going to wrong endpoint
- Hermes status shows wrong provider
- User wants to switch between providers

## The Core Problem

In April 2026, a critical config error occurred where:
- `model.default.base_url` was set to `https://api.xiaomimimo.com/v1` (Xiaomi URL)
- But `provider` was set to `openrouter`
- Result: All OpenRouter requests went to Xiaomi endpoint with wrong auth → 401 errors

## Correct Config Structure

```yaml
model:
  default: openrouter/free  # or xiaomi/v2_pro
  provider: openrouter      # or xiaomi
  base_url: https://openrouter.ai/api/v1  # MUST match the provider
  api_mode: chat_completions
  max_tokens: 4000
  providers:
    xiaomi:
      base_url: https://api.xiaomimimo.com/v1  # SEPARATE endpoint
      api_key: ${XIAOMI_API_KEY}               # SEPARATE key
      api_mode: chat_completions
      max_tokens: 4000
      models:
        flash:
          model_id: mimo-v2-flash
          # ... settings
        v2_pro:
          model_id: mimo-v2-pro
          # ... settings
        v2_omni:
          model_id: mimo-v2-omni
          # ... settings
    openrouter:
      api_keys:
        - ${OPENROUTER_API_KEY}               # MUST not be empty
```

## Key Rules

1. **NEVER mix provider base URLs:**
   - OpenRouter ALWAYS uses `https://openrouter.ai/api/v1`
   - Xiaomi ALWAYS uses `https://api.xiaomimimo.com/v1`
   - These are SEPARATE companies, SEPARATE APIs, SEPARATE keys

2. **Default provider must match the base_url:**
   - If `provider: openrouter` → `base_url: https://openrouter.ai/api/v1`
   - If `provider: xiaomi` → `base_url: https://api.xiaomimimo.com/v1`

3. **API Keys are separate:**
   - `OPENROUTER_API_KEY` in `.env` → for OpenRouter Free models
   - `XIAOMI_API_KEY` in `.env` → for Xiaomi MiMo V2 Pro
   - They are NEVER interchangeable

4. **Model selection:**
   - OpenRouter model format: `openrouter/free` (uses routing)
   - Xiaomi model format: `xiaomi/v2_pro` or `xiaomi/flash` or `xiaomi/v2_omni`

## Switching Providers

To switch to Xiaomi (current working setup as of 2026-04-06):
```yaml
model:
  default: xiaomi/v2_pro
  provider: xiaomi
  base_url: https://api.xiaomimimo.com/v1
```

To switch back to OpenRouter Free:
```yaml
model:
  default: openrouter/free
  provider: openrouter
  base_url: https://openrouter.ai/api/v1
```

## Configuration Update Process

1. Read current config: `cat ~/.hermes/config.yaml`
2. Check what's currently configured:
   - What's `model.default.provider`?
   - What's `model.default.base_url`?
   - Are they consistent?
3. Update ONLY the three fields: `default`, `provider`, `base_url`
4. Verify: `hermes status` should show the new model/provider
5. Test: Send a simple API request (or for Telegram: send `/start` to bot)

## Pitfalls
- Do NOT update `providers` section when switching default — those are provider definitions, not active config
- Do NOT modify `api_keys` or `base_url` under individual providers when just switching default
- After changing config, the running agent process may need a restart to pick up the new config
- OpenRouter Free has 429 rate limits (both per-minute and per-day) — if rate-limited, cannot use until quota resets or credits are added
- If switching to Xiaomi, verify `XIAOMI_API_KEY` is valid and has credits
- Always backup config.yaml before changes (not critical but good practice)