---
name: config-xiaomi-mimo
description: Safely add or update Xiaomi MiMo (mimo v2 pro) provider in ~/.hermes/config.yaml for Hermes Agent. Includes steps to locate provider block, insert Xiaomi provider with API key placeholder, validate syntax, and backup config. Reusable for future updates.
author: Hermes Agent
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [hermes, config, provider, xiaomi, mimo, setup]
    homepage: https://github.com/NousResearch/hermes-agent
    related_skills: [hermes-agent]
---

# Update Xiaomi MiMo (mimo v2 pro) Provider in Hermes Config

This skill documents a reliable workflow for adding or updating the Xiaomi MiMo provider (used for `mimo v2 pro` model) in the Hermes Agent configuration file at `~/.hermes/config.yaml`. The process includes:

- Locating the provider section safely
- Inserting the Xiaomi provider with API key placeholder
- Preserving YAML indentation and validity
- Backing up the original config
## Step‑by‑Step Procedure

1. **Backup the current config**
   ```bash
   cp ~/.hermes/config.yaml ~/.hermes/config.yaml.bak.$(date +%Y%m%d_%H%M%S)
   ```

2. **View current config to locate the provider block**
   ```bash
   # Print first 100 lines to see structure
   head -n 100 ~/.hermes/config.yaml
   ```

3. **Identify the model.providers structure**\
   In modern Hermes config, providers are nested under `model:` as `model.providers`. Look for this structure:\
   ```yaml\
   model:\
     default: openrouter/free\
     providers:\
       openrouter:\
         base_url: https://openrouter.ai/api/v1\
         api_mode: chat_completions\
   ```\
   The config may have a single top‑level `provider:` key but that format is deprecated – best to convert to `model.providers` syntax.

**IMPORTANT: Hermes version compatibility:** Some Hermes versions (observed 2026-04) use the FLAT model config format:
```yaml
model:
  default: xiaomi/v2_pro
  provider: xiaomi
  base_url: https://api.xiaomimimo.com/v1
  api_mode: chat_completions
  max_tokens: 4000
providers:
  xiaomi:
    api_key: ${XIAOMI_API_KEY}
    api_mode: chat_completions
    max_tokens: 4000
    models:
      flash:
        model_id: mimo-v2-flash
        ...
```
In this format, `model.default` = `"xiaomi/v2_pro"`, `model.provider` = `"xiaomi"`, AND `model.base_url` are all at the `model:` top level (NOT nested under `model.providers`). The `providers:` dict at root level holds the full provider config including models/hyperparameters.

4. **Add the Xiaomi provider block with hyperparameters**
   Insert the following block **inside** the `model.providers:` section, before any `fallback_providers:` entry:

   ```yaml
     xiaomi:
       base_url: https://api.xiaomimimo.com/v1
       api_key: ${XIAOMI_API_KEY}
       api_mode: chat_completions
       max_tokens: 4000
       models:
         flash:
           model_id: mimo-v2-flash
           temperature: 0.3
           top_p: 0.95
           price_input_usd_per_1m: 0.0
           price_output_usd_per_1m: 0.0
           note: Default model - guenstig & schnell
         v2_pro:
           model_id: mimo-v2-pro
           temperature: 1.0
           top_p: 0.95
           price_input_usd_per_1m: 1.0
           price_output_usd_per_1m: 3.0
           note: Nur bei Bedarf/komplexen Tasks (auf Anfrage nutzen)
         v2_omni:
           model_id: mimo-v2-omni
           temperature: 1.0
           top_p: 0.95
           price_input_usd_per_1m: 0.4
           price_output_usd_per_1m: 2.0
           note: Alternative zu Pro
   ```

   **CRITICAL:** The correct base URL is `https://api.xiaomimimo.com/v1`. The URL `platform.xiaomimimo.com` returns 404. This is a common pitfall.

**API Key Naming:** The config expects `${XIAOMI_API_KEY}`. Do NOT use `XIAOMI_MIMO_API_KEY` in `.env` — they must match exactly. Mismatch causes "API key not found" errors.

5. **Set the API key**
   - The config expects `${XIAOMI_API_KEY}` (not `XIAOMI_MIMO_API_KEY`). Ensure `.env` uses the same name:
     ```bash
     echo "XIAOMI_API_KEY=sk-..." >> ~/.hermes/.env
     ```
   - Restart Hermes to pick up the new environment variable.

6. **Recommended model defaults:**
   - `flash` (temp 0.3, top_p 0.95) – cost-efficient, routine tasks
   - `v2_pro`/`v2_omni` (temp 1.0, top_p 0.95) – complex tasks only
   - Set `model.default: xiaomi/flash`

7. **Validate**
   ```bash
   hermes doctor
   # Or test connectivity:
   curl -s https://api.xiaomimimo.com/v1/models -H "Authorization: Bearer $XIAOMI_API_KEY"
   ```

## CRITICAL: Known Hermes System Limitations

### Provider Registry Gap
**`xiaomi` ist NICHT im PROVIDER_REGISTRY** von Hermes (`hermes_cli/auth.py`).
Das bedeutet: Auch wenn `config.yaml` `provider: xiaomi` sagt, erkennt das System es nicht als bekannten Provider und fällt auf OpenRouter zurück.

In `runtime_provider.py` Zeile 727-732 ist der finale Fallback immer `_resolve_openrouter_runtime()` – wenn ein Provider nicht im Registry ist, landet er hier.

### Auto-Reset durch Config Migration
Bei `hermes update` oder Config-Migration (v11→v12 in `hermes_cli/config.py`) wird das `model:` Feld zurückgesetzt.
- **Vorher:** `model:` als Dictionary mit `default`, `provider`, `base_url` → wird auf einfachen String zurückgesetzt
- **Nachher:** `model: qwen/qwen3.6-plus:free` oder ähnlich → Xiaomi-Konfiguration ist WEG
- Die Migration erkennt nur Standard-Schema-Felder und verwirft alles andere

### Workaround für Provider-Registry Gap
Da `xiaomi` nicht im Registry ist, nutze einen der bekannten Provider als Basis und override die URL:
- Option A: Nutze `provider: custom` mit `base_url: https://api.xiaomimimo.com/v1` in `config.yaml`
- Option B: Trage Xiaomi als `custom_provider` in der Config ein (Format: `custom_providers: [{name: "xiaomi", base_url: "https://api.xiaomimimo.com/v1", api_key: "${XIAOMI_API_KEY}"}]`)
- Option C: Setze Umgebungsvariable `HERMES_INFERENCE_PROVIDER=custom` und `OPENAI_BASE_URL=https://api.xiaomimimo.com/v1`

## Common Pitfalls & Fixes

| Symptom | Likely Cause | Fix |
|--------|--------------|-----|
| `YAML syntax error` | Incorrect indentation or missing colon | Ensure 4‑space indentation for nested keys; trailing colon after key name |
| Auto-Reset auf OpenRouter nach Update | Config Migration hat Dictionary-`model` zurückgesetzt | Siehe "Workaround für Provider-Registry Gap" – nutze `custom_provider` statt `provider: xiaomi` |
| Provider nicht erkannt | `xiaomi` nicht im PROVIDER_REGISTRY | Nutze `custom:` prefix oder Umgebungsvariable |
| `hermes doctor` reports missing provider | Provider block not saved or not within `provider:` section | Re‑open config, verify block is inside `provider:` and before `fallback_providers:` |
| `API key not found` | Placeholder `${XIAOMI_API_KEY}` not exported **or** environment variable name mismatch | Ensure consistent variable name in `.env` and `config.yaml`. |
| `Default model not using Xiaomi` | `model.default` still points to OpenRouter or another provider | Set `model.default: custom:xiaomi` oder verwende `custom_providers` Format |
| Changes not taking effect | Hermes session still using old config | Restart Hermes with `/reset` or close/reopen the session |
| Duplicate `provider:` keys | Multiple `provider:` sections merged incorrectly | Keep only one top‑level `provider:` entry |

## Verifying the Update

1. **Check the Xiaomi block and default model**
   ```bash
   grep -A20 "model:" ~/.hermes/config.yaml | head -30
   ```

2. **Test API connectivity**
   ```bash
   curl -s https://platform.xiaomimimo.com/v1/models -H "Authorization: Bearer $XIAOMI_API_KEY" | head -20
   ```
   Should list `mimo-v2-flash`, `mimo-v2-pro`, `mimo-v2-omni`, `mimo-v2-tts`.

3. **Run a quick test query (default model should respond)**
   ```bash
   hermes chat -q "Echo test: 42"
   ```

4. **Run the health check**
   ```bash
   hermes doctor
   ```

If all checks pass, the Xiaomi MiMo provider is correctly configured and ready for use. Default: flash; use `--model xiaomi/v2_pro` or `xiaomi/v2_omni` on demand for complex tasks.

## Updating the Skill

Whenever you discover a new nuance (e.g., a different base URL, additional provider options, or a new validation step), edit this skill:

```bash
skill_manage(action='patch', name='config-xiaomi-mimo', old_string='base_url: https://api.xiaomimomo.com/v1', new_string='base_url: https://api.xiaomimimo.com/v1')
```

Keep the script and steps current with any upstream changes to the Hermes configuration schema.