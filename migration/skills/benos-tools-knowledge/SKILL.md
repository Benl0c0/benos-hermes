---
name: benos-tools-knowledge
description: BEN//OS Tools & APIs knowledge base. Quick reference for 25+ tools with ratings, integration steps, and known issues. Covers LLM providers (S1-S5), communication tools, dev tools, search APIs, infrastructure, and audio tools.
version: 1.0.0
author: Hermes Agent (from BEN//OS Wissensbasis)
license: MIT
metadata:
  hermes:
    tags: [BEN//OS, Tools, APIs, Integrations, LLM-Providers, Infrastructure]
    related_skills: [benos-cost-routing, benos-kira-architecture]
    source: /mnt/c/Users/benlo/Desktop/Hermes-Inbox/Good to know/
---

# BEN//OS Tools Knowledge

## Trigger Conditions
- Setting up a new integration or API
- Choosing which tool to use for a task
- Troubleshooting an existing integration
- Comparing alternative tools for cost/feature trade-offs
- Adding tools to TOOLS.md

## LLM Providers (BEN//OS S1-S5) – Live Status April 2026

| Tier | Provider/Model | Cost | Available APIs | Status | Best For |
|------|---------------|------|----------------|--------|----------|
| S1 | Xiaomi MiMo Flash | Free (0$/M) | `api.xiaomimimo.com` | ✅ ACTIVE | Default, fast, cheap, good for 80% tasks |
| S2 | Xiaomi MiMo Omni | $0.40 in / $2.00 out | `api.xiaomimimo.com` | ✅ ACTIVE | Complex analysis, coding, higher quality |
| S3 | Xiaomi MiMo Pro | $1.00 in / $3.00 out | `api.xiaomimimo.com` | ✅ ACTIVE | Only for heavy tasks (S3 tier) |
| S4 | Venice AI | Variable ($0.20-30/M) | `api.venice.ai` | ✅ ACTIVE | Uncensored, 60 models including Claude/GPT/Grok |
| S5 | OpenRouter Free | Free (rate limited) | `openrouter.ai` | ⚠️ KEYS EXHAUSTED | Fallback only – neue Keys nötig |
| S5 | Local Ollama可选 | Free (lokal) | `localhost:11434` | ✅ OPTIONAL | Laptop 2 Worker, qwen2.5-coder, phi3-mini |

**CRITICAL NOTES:**
- ❌ `platform.xiaomimimo.com` existiert nicht! Korrekt: `api.xiaomimimo.com`
- ⚠️ OpenRouter free Keys sind nach intensiver Nutzung alle exhausted (401/402)
- ✅ Xiaomi API hat Guthaben – ist primärer Provider
- ✅ Venice AI hat aktiven Key (VENICE-ADMIN-…)
- 🔧 `.env` Variable: `XIAOMI_API_KEY` (nicht `XIAOMI_MIMO_API_KEY`)
- 🔧 Default Model sollte sein: `xiaomi/flash` (temp 0.3, top_p 0.95)

## Core Agent Frameworks

## Core Agent Frameworks

| Tool | Type | Rating | Status | Setup Notes |
|------|------|--------|--------|-------------|
| OpenClaw | Agent runtime | ★★★★★ | ACTIVE | Always-on, Telegram, skills, cron, sub-agents. Docs: docs.openclaw.ai. Community: Discord. Setup helper: simpleclaw.com |
| Paperclip | Orchestration | ★★★★★ | PENDING | Multi-agent coordination layer. Install after OpenClaw. Repo: github.com/paperclipai/paperclip |
| AnythingLLM | RAG/Wissensbasis | ★★★★☆ | PENDING | Local document knowledge base. Repo: github.com/Mintplex-Labs/anything-llm |
| Agent Zero | Framework fallback | ★★★☆☆ | NOT INSTALLED | github.com/agent0ai/agent-zero |
| Superpowers | Skills | ★★★☆☆ | NOT INSTALLED | github.com/obra/superpowers |
| gstack | Claude workflow | ★★★☆☆ | NOT INSTALLED | github.com/garrytan/gstack |
| Hermes | Self-learning | ★★★☆☆ | ACTIVE (this tool) | github.com/nousresearch/hermes-agent |

## Communication Tools

| Tool | Use | Rating | Notes |
|------|-----|--------|-------|
| Telegram | Primary notifications | ★★★★★ | Native OpenClaw support. BotFather setup. BUG: 8-min polling on some configs |
| Slack | Team workflows | ★★★★☆ | OpenClaw Slack skill. Requires Bot Token |
| WhatsApp | Mobile messages | ★★★☆☆ | Voice message support, alternative to Telegram |

## Task Management

| Tool | Use | Rating | Setup |
|------|-----|--------|-------|
| Asana | Task tracking | ★★★★☆ | Personal Access Token + Workspace-ID in TOOLS.md |
| Google Calendar | Scheduling | ★★★★☆ | OAuth setup required |
| Gmail | Email | ★★★★☆ | OAuth setup required |
| Todoist | Personal tasks | ★★★☆☆ | Available via OpenClaw skill |
| Notion | Docs/notes | ★★★☆☆ | Available via OpenClaw skill |

## Developer Tools

| Tool | Use | Rating | Setup |
|------|-----|--------|-------|
| GitHub | Code hosting | ★★★★★ | GitHub Token in .env. OpenClaw skill available |
| Cursor | Code agent | ★★★★☆ | cursor-agent skill for OpenClaw |
| Sentry | Error monitoring | ★★★☆☆ | OpenClaw Sentry skill. Auto-issue creation |

## Search & Research

| Tool | Use | Rating | Notes |
|------|-----|--------|-------|
| Brave Search API | Web search | ★★★★☆ | Cheaper than Google |
| Exa API | Semantic search | ★★★★☆ | Good for research agents |
| YouTube Data API | Channel analytics | ★★★★☆ | Google Cloud + OAuth |
| xAI/Grok API | X/Twitter data | ★★★☆☆ | Social media intelligence |

## Infrastructure

| Tool | Use | Rating | Notes |
|------|-----|--------|-------|
| DigitalOcean/Hetzner | VPS hosting | ★★★★☆ | $6/mo Droplet, 2GB RAM minimum |
| Cloudflare Tunnel | Remote access | ★★★★★ | Free, no open port needed. SECURITY MUST-HAVE |
| Tailscale | Alternative VPN | ★★★★☆ | More secure alternative to Cloudflare Tunnel |

## Audio Tools

| Tool | Use | Rating | Notes |
|------|-----|--------|-------|
| Whisper.cpp | Local voice transcription | ★★★★☆ | Mobile workflow (voice → text → action) |
| ElevenLabs | Voice synthesis | ★★★☆☆ | Content agents |

## Finance/Trading

| Tool | Use | Rating | Notes |
|------|-----|--------|-------|
| TradingView | Chart analysis | ★★★☆☆ | Via browser automation |
| Quodd | Stock quotes | ★★★☆☆ | Real-time prices |

## Smart Home & Health (Phase 2+)

| Tool | Use | Rating | Notes |
|------|-----|--------|-------|
| Oura Ring | Health data | ★★★☆☆ | Energy-aware scheduling (future) |
| Home Assistant | Smart home | ★★★☆☆ | Available via OpenClaw skill |

## Integration Checklist

When adding any new tool, update TOOLS.md with:
- [x] Tool name and purpose
- [x] API token and storage location (.env, NOT code)
- [x] Required OAuth/credential steps
- [x] OpenClaw skill name (if available)
- [x] Agent(s) that will use this tool
- [x] Cost impact estimate
- [x] Security considerations

## Pitfalls
- API keys in TOOLS.md or code → use .env only
- Missing skill check → install via OpenClaw skill system before use
- Telegram 8-minute polling bug → monitor and reset if needed
- Cloudflare Tunnel vs open port → NEVER expose OpenClaw directly
- YouTube API quota → easy to exhaust, monitor usage
- Cloudflare Tunnel is free and secure → do not use open ports
- **CRITICAL:** Xiaomi MIMO endpoint ist `api.xiaomimimo.com` NICHT `platform.xiaomimimo.com` (gibt 404)
- OpenRouter free Keys erschöpfen sich schnell → Xiaomi/Venice als primäre Provider
- .env Variable muss exakt mit config.yaml übereinstimmen: `XIAOMI_API_KEY` (nicht `XIAOMI_MIMO_API_KEY`)
- `.gitignore` MUSS `.env` enthalten bevor irgendetwas gepusht wird

## Verification
- [x] All active tools documented with ratings
- [x] API keys in .env, not in code or TOOLS.md
- [x] OpenClaw listening on 127.0.0.1 only (not 0.0.0.0)
- [x] .env file permissions set to 600
- [x] Cloudflare Tunnel or Tailscale for remote access
- [x] Auth token enabled and secure
- [x] Tool costs tracked per-agent through CTO Cost Monitor
