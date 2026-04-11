---
name: hermes-survival-guide-lessons-learned
description: "Critical survival rules for Hermes operation: never use config set, always use resume, custom provider config pitfalls, and emergency reset commands."
---

# Hermes: Survival Guide & Lessons Learned

## CRITICAL RULES (DO NOT IGNORE)

### 1. The Golden Rule of Restarting
- **NEVER** start a new session with just `hermes` if we were in the middle of complex debugging.
- **ALWAYS** use `hermes --resume` or `hermes -c` to continue.
- **Why:** Restarting via `hermes` creates a blank slate. The new session will load the `config.yaml` file (which might still be broken from a previous failed fix), but it will NOT have the RAM state or memory of the debugging context. It will likely fall back to OpenRouter Free and hit 429 errors immediately, repeating the cycle.

### 2. The "Config Set" Destruction Hazard
- **NEVER** use `hermes config set model "custom/xiaomi"` (or similar) for custom providers.
- **Why:** This command writes a simple string into `config.yaml` (e.g., `model: custom/xiaomi`), DELETING the entire dictionary structure required for custom providers (which needs `base_url`, `api_key`, `providers`, etc.).
- **Result:** The system loses the URL and Key for Xiaomi and falls back to OpenRouter immediately.

### 3. The ":free" Normalization Bug
- Hermes `model_normalize.py` has a quirk where `:free` in OpenRouter model IDs (like `qwen/qwen3.6-plus:free`) can trigger API errors.
- **Fix:** The `model_normalize.py` file has been patched to catch this, but be careful with manual entry of OpenRouter models.

## EMERGENCY PROTOCOLS

### Emergency Reset (If the Bot/AI becomes unresponsive or crashes)
If `/model` fails and the chat is dead, use this command in the CLI input:
```
/model qwen/qwen3.6-plus:free
```

If that doesn't work via CLI, use this from the command line (Terminal):
```bash
hermes config set model qwen/qwen3.6-plus:free
hermes --resume
```

### The "Multi-KI" Check Rule
Before trusting a major config change or fix from a single AI:
1. **GPT** writes the fix.
2. **Claude** checks and edits the fix.
3. **Grok** analyzes if it actually changes the root cause.

## XIAOMI PROVIDER SETUP
To successfully switch to Xiaomi MiMo V2 Pro:
1.  **Config.yaml**: Must have `model` as a Dictionary:
    ```yaml
    model:
      default: mimo-v2-pro
      provider: custom:xiaomi
      base_url: https://api.xiaomimimo.com/v1
    ```
2.  **Custom Providers**: Must exist in the config:
    ```yaml
    custom_providers:
      - name: xiaomi
        base_url: https://api.xiaomimimo.com/v1
        api_key: sk-ejgyeew8nffbd310f2p0fe0u2agvpt54hkr3jxqx4k6nvz8u
        model: mimo-v2-pro
    ```
3.  **Auth Pool**: `auth.json` must have the Xiaomi key in `credential_pool` with key `custom:xiaomi` and status "ok" or "active".
4.  **Activation**: User must type `/model mimo-v2-pro --provider custom:xiaomi` in the chat.
