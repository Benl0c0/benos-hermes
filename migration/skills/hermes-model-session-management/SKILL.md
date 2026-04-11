---
name: hermes-model-session-management
description: Safe model switching and session management for Hermes Agent
category: hermes
---

# Hermes Model Switching and Session Management

## Purpose
Safe and effective model switching in Hermes Agent, understanding the difference between fresh and resumed sessions, and avoiding common configuration pitfalls.

## Key Insights from Experience

### 1. Fresh Sessions vs Resumed Sessions
- **Fresh Session**: `hermes` or `hermes --resume NEW` 
  - Loads configuration from `config.yaml` 
  - Model changes in config.yaml take effect immediately
- **Resumed Session**: `hermes --resume <existing-session-id>`
  - Continues with the model and settings from the saved session state
  - **Ignores** current `config.yaml` model settings
  - Useful for continuing work but not for testing config changes

### 2. Safe Model Switching Practices
**DO:**
- Use `/model <model-name>` to switch at runtime in any session (session-only)
- Use `/model <model-name> --global` to persist model choice to config.yaml
- Edit `config.yaml` directly for permanent changes, then start a **fresh session**
- Use `/provider` to see available models and current provider
- Verify active model by checking API calls or session status
- Use `/usage` to monitor token consumption and costs

**DO NOT:**
- Use `hermes config set model` - this can corrupt the YAML configuration
- Assume config changes take effect in resumed sessions
- Rely on free models for complex reasoning or extended tool use
- Switch models frequently without checking rate limits

### 3. Configuration Safety
- Never use `hermes config set model` - it breaks config.yaml structure
- To change default model permanently:
  1. Edit `~/.hermes/config.yaml` directly: set `default:` under `model:` section
  2. Start a **fresh session**: `hermes` or `hermes --resume NEW`
  3. Verify with `/model` command
- The `.env` file should contain API keys (OPENAI_API_KEY, OPENROUTER_API_KEY, etc.)
- Never commit API keys to git

### 4. Verification Techniques
- Check actual API calls being made (not just what config says)
- Use `/model` command to see current model
- Use `/provider` to see available providers
- Monitor `/usage` for token consumption and costs
- Check running processes: `ps aux | grep hermes`
- For deep inspection: examine session files in `~/.hermes/sessions/`

### 5. Troubleshooting Workflow
When model isn't behaving as expected:
1. **Check session type**: Are you in fresh or resumed session?
2. **Verify model**: What does `/model` show?
3. **Check config**: Is config.yaml set correctly?
4. **Look at errors**: Are you hitting rate limits (429) or context limits?
5. **Consider fresh start**: If in doubt, exit and start `hermes` (fresh session)
6. **Test with /model**: Try switching models at runtime to isolate issues

### 6. Model Recommendations by Use Case
- **Quick testing / simple queries**: Free models (qwen, gemini, minimax) 
- **Coding / debugging**: Xiaomi Flash (fast, cheap, good for code)
- **Complex reasoning**: Xiaomi Pro or OpenAI Abo (if configured)
- **Vision tasks**: Xiaomi Omni
- **Fallback**: OpenRouter Free (when others fail or for cost control)

### 7. Session Management Best Practices
- Use `/new` or `/reset` frequently to start clean sessions
- Only use `--resume` when you need to continue specific work
- Exit unused sessions to free resources
- Monitor session files size in `~/.hermes/sessions/` (large files indicate problems)
- Consider periodic cleanup of old sessions

## Common Issues and Fixes

**Issue**: Model change in config.yaml not taking effect
**Fix**: You're likely in a resumed session. Exit and start fresh session.

**Issue**: "/model command not working" 
**Fix**: You may be in a broken session state. Try `/new` to start fresh.

**Issue**: Getting rate limit errors (429)
**Fix**: Switch to a different model, wait, or check your free tier limits.
Consider using Xiaomi Flash for sustained low-cost work.

**Issue**: Context limit errors
**Fix**: Switch to a model with larger context window (Xiaomi models have 1M context)
Or use context compression if available.

## Quick Reference Commands

| Command | Purpose |
|---------|---------|
| `/model` | See current model |
| `/model <model>` | Change model for current session |
| `/model <model> --global` | Change model persistently |
| `/provider` | See available providers |
| `/usage` | Check token usage and costs |
| `/new` or `/reset` | Start fresh session |
| `ps aux \| grep hermes` | Check running Hermes processes |
| `hermes --help` | See all available commands |

## When to Use Each Approach

- **Testing a model change**: Use `/model <model>` in current session
- **Making a model change permanent**: Edit config.yaml + `/new` 
- **Troubleshooting model issues**: Start fresh session (`/new`) and test
- **Continuing important work**: Use `--resume <session-id>`
- **Checking costs**: Use `/usage` command
- **Seeing what's available**: Use `/provider`

## Safety Notes
- Free models have strict rate limits (often 50 requests/day)
- Free models may have reduced reasoning capabilities
- Always verify which model is actually making API calls
- Config.yaml edits are safer than `hermes config set model`
- Free tier models are subject to change and deprecation