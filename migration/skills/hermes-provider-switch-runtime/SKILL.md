---
name: hermes-provider-switch-runtime
description: Safe, non-destructive provider switching (e.g. Xiaomi, OpenRouter) without corrupting config or crashing the running agent.
---
# Hermes Provider Switch (Runtime / Non-Destructive)

Safely switch the inference provider/model during a running session (e.g., OpenRouter -> Xiaomi) without crashing the agent or corrupting the configuration.

## TRIGGERS
- User requests model/provider switch.
- Agent detects "402/429 Rate Limit" or "Provider exhausted".
- Config needs to move from OpenRouter to Custom Provider (Xiaomi/Claude).

## DANGEROUS TRAPS ⚠️
- **NEVER use `hermes config set model <value>`**: This command flattens the `model` dictionary in `config.yaml` into a simple string, destroying the provider configuration. Use `write_file` or `patch`.
- **Dictionary Requirement**: The `model` key in `config.yaml` **MUST** be a dictionary with keys: `default`, `provider`, `base_url`, `api_mode`. If it is a string, the system defaults to OpenRouter and fails.
- **:free -> /free BUG**: The `/model` command and `normalize_model_for_provider()` can accidentally convert `:free` to `/free` (e.g. `qwen/qwen3.6-plus:free` -> `qwen/qwen3.6-plus/free`), causing HTTP 400. Check `model_normalize.py` to ensure the `:free` suffix is preserved for aggregator providers.
- **Auth.json is key**: The runtime resolver checks the `credential_pool` in `auth.json`. If it contains "exhausted" OpenRouter keys but NO entry for the new provider, it will fail to switch. Always update BOTH files.
- **File updates are not enough**: Updating YAML/JSON on disk does NOT update the running Python process. The agent needs a trigger (`/model` or `switch_model`) to reload credentials.

## STEP-BY-STEP PROCEDURE

### 1. Verify `~/.hermes/config.yaml`
Ensure `model` is a **Dictionary**, NOT a string:
```yaml
_config_version: 12
model:
  default: mimo-v2-pro
  provider: custom:xiaomi
  base_url: https://api.xiaomimimo.com/v1
  api_mode: chat_completions
  max_tokens: 4000
custom_providers:
  - name: xiaomi
    base_url: https://api.xiaomimimo.com/v1
    api_key: sk-... # Full key
    api_mode: chat_completions
# fallback_providers: [openrouter]
```

### 2. Update `~/.hermes/auth.json`
Add a new array entry for `custom:xiaomi` in `credential_pool`. If you don't, the system uses the old (exhausted) OpenRouter keys:
*   `id`: unique string (e.g., "xiaomi-001")
*   `label`: "XIAOMI_API_KEY"
*   `base_url`: "https://api.xiaomimimo.com/v1"
*   `access_token`: The actual API Key.
*   `priority`: 0 (highest)
*   `last_status`: "ok"

### 3. Patch `model_normalize.py` (If needed)
If you see `:free` becoming `/free`, ensure the `normalize_model_for_provider` function in `hermes_cli/model_normalize.py` does not inadvertently replace colons.

### 4. Trigger the Switch
Use `/model custom:xiaomi` in the chat, or in code:
```python
agent.switch_model(
    new_model="mimo-v2-pro",
    new_provider="custom:xiaomi",
    api_key="...",
    base_url="https://api.xiaomimimo.com/v1",
    api_mode="chat_completions"
)
```
