---
name: wsl-pc-maintenance
description: Guide for maintaining, cleaning, and organizing Ben's WSL2/Windows hybrid PC. Covers cache management, file organization via WSL, update procedures, and known pitfalls.
last_updated: 2026-04-02
---

# WSL PC Maintenance Guide

## Environment Context
- **Host**: Windows (User: `benlo`)
- **Guest**: WSL2 Ubuntu 24.04
- **Key Paths**: WSL home is `/home/benlo/`, Windows C: is `/mnt/c/`
- **OneDrive Active**: Many standard Windows folders are redirected to OneDrive.
  - Desktop: `/mnt/c/Users/benlo/OneDrive/Desktop/` (NOT `/Desktop`)
  - Downloads: `/mnt/c/Users/benlo/Downloads/`

## Cleaning Procedures

### 1. WSL/Linux Caches (Safe to nuke, ~3.4GB)
Dev tools leave massive caches. Always clear these when asked to clean up.
```bash
rm -rf ~/.cache/camoufox      # ~1.4GB (Browser fonts/cache)
rm -rf ~/.cache/uv            # ~668MB (Python builds)
rm -rf ~/.cache/ms-playwright # ~631MB (Browser binaries)
rm -rf /tmp/camoufox-*        # ~680MB (Orphaned temp files)
npm cache clean --force
```

### 2. Windows File Organization (via WSL)
Instead of clicking in Explorer, use WSL `mv`/`mkdir` to quickly organize the PC.
Standard structure to create on Desktop or Downloads:
- `_Archiv/` -> ZIP/RAR files
- `_Dokumente/` -> PDFs, HTMLs, images
- `_Install_Dateien/` -> .exe installers (safe to delete)
- `Zu_Loeschen/` -> Candidates for deletion (review with user first)

- **Tools**: `uv self update`, `npm update -g`.

### 4. Scanning Windows Folders (Avoid Timeouts)
- **PITFALL**: `du -sh /mnt/c/Users/.../AppData/*` often hangs/times out due to Windows file locks.
- **Solution**: Use `ls` with `head` limits, or run analysis via PowerShell:
  `powershell.exe -Command "Get-ChildItem ..."`
- **PITFALL**: AppData/Local/Temp can be 2GB+. Use Windows Disk Cleanup for best results.

## SkillBoss Integration
- **Ubuntu**: `apt-get update && apt-get upgrade` requires `sudo`.
- **PITFALL**: `sudo` will fail in non-interactive execute_code blocks ("a terminal is required").
- **Solution**: Tell user to run `sudo apt-get upgrade -y` manually, or pass password via `echo PASS | sudo -S` if available in `.env`.
- **Tools**: `uv self update`, `npm update -g`.

## SkillBoss Integration
- **Status**: CLI `setup` command is broken/missing in `@skillboss/cli`.
- **Workaround**: Use API directly via `curl` with the stored API key.
- **Validated Endpoints**:
  - Chat: `https://api.heybossai.com/v1/chat/completions`
  - Run: `https://api.heybossai.com/v1/run`
- **Models**: Qwen free via OpenRouter (S1), MiMo V2 Pro (Good/cheap), Claude/GPT (Paid).
