---
name: generate-system-blueprint
description: Create structured technical system blueprints for AI Architect agents (Opus, GPT-5.4, Grok). Defines hardware constraints, architecture patterns, and deliverables.
tags:
  - architecture
  - planning
  - multi-agent
  - benos
related_skills:
  - benos-setup
  - benos-cost-routing
---

# SYSTEM BLUEPRINT GENERATION

**TRIGGER:** User needs a comprehensive technical plan/specification to be executed by AI coding agents (Claude Code, etc.), especially when hardware constraints or complex architectural decisions are involved.

## PROCESS

### 1. Assess Constraints
- **Hardware:** CPU (cores), RAM (tightness?), GPU (VRAM availability), Storage type (SSD/NVMe).
- **Software:** OS (Ubuntu/WSL/Windows), Containerization (Docker vs Native/Systemd), Python version.
- **Network:** Local only, Webhooks needed, SSH access.

### 2. Define Architecture Layers
Structure the output in these distinct sections:
- **Infrastructure:** OS, Services (Docker vs Native venvs), Security (SSH/UFW).
- **Memory Layer:** Database choice (SQLite for simple, Postgres for scale), Vector DB, Filesystem paths.
- **Local Intelligence:** Ollama/Local LLM strategy, Model selection, Memory offloading (`keep_alive: 30s`).
- **Agent Architecture:** Process orchestration, Task Queues (Redis vs File-based JSONL).
- **Connectivity:** API Endpoints, Telegram integration, Dashboard ports.
- **Cost Control:** Budget tracking logic, API routing matrix.

### 3. Define Deliverables
List exactly what the executing agent must build:
- `setup.sh` / installation scripts
- `docker-compose.yml` (if applicable) or `systemd` service definitions
- Directory structure (e.g., `mkdir -p ~/benos/{memory,logs,scripts}`)
- Configuration templates (`.env.example`, `config.yaml`)

### 4. Special "Slim Mode" Rules (Low RAM < 8GB)
- Avoid heavy Docker daemons if possible; use native Systemd services.
- Force local LLMs to unload after use (`keep_alive: 30s`).
- Use SQLite and simple file queues (JSONL) instead of Redis/RabbitMQ.

### 5. Formatting
- Output as a clean Markdown document (`BLUEPRINT.md`).
- Use clear hierarchy, code blocks for config snippets or directory trees.
- Keep it "Agent-Ready": unambiguous instructions.

### PITFALLS
- **Assumptions:** Don't assume tools (Docker/Python) are installed; include setup steps.
- **Secrets:** Never hardcode real keys; use `.env` or `${VAR}` placeholders.
- **Permissions:** Ensure service users have correct ownership of directories (`User=hermes`).

### VERIFICATION
- Ask the user to pass the blueprint to the Architect/AI Board for review.
- Confirm hardware constraints match the target machine.
