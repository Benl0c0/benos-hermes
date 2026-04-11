---
name: inbox-processing-sop
description: Standard Operating Procedure for processing Ben's Inbox (Hermes-Inbox + bens Smartphone - Inbox). Automatically analyzes, rates, and categorizes incoming files.
---

## Inbox SOP for Hermes Agent

### TRIGGER (ACTUAL PATHS)
- Watchdog monitors `/mnt/c/Users/benlo/Desktop/Hermes-Inbox/` **recursively** (includes subfolder `bens Smartphone - Inbox/`)
- User drops files directly into the main inbox or its subfolders

### PROCESS
1. **Identify file type** and extract content:
   - Images (.jpg/.png): Use SkillBoss Vision (openai/gpt-4o) to describe layout, text, UI
   - DOCX: Extract text via `docx2txt` CLI command (`docx2txt <file> /tmp/output.txt`). Do NOT use python-docx module inside sandbox (missing docx module, links break API).
   - PDF: Use `pdftotext` command to extract text
   - HTML: Read and analyze structure/content
   - TXT: Read content, follow any links to verify

⚠️ CRITICAL - LINK FOLLOWING RULE:
   If a file contains a URL/link, ALWAYS open it with browser_navigate. Read the actual content at the destination.
   If the destination page contains ANOTHER link, follow it (minimum 2 levels deep).
   Keep following until you reach the actual file, info, error message, or real content.
   NEVER rate a file as \"low prio/trash\" just because it \"only contains a link\" — the link IS the content gateway.
   PITFALL: A file that says \"please study this\" + a link is NOT trash — it's a pointer to valuable info. Always verify before rating.

⚠️ CRITICAL - FULL INSPECTION RULE:
   Never stop at the first page/first few lines of a file. Always read/scroll to the end or until you are certain you've seen all relevant information.
   For large HTML/Markdown files, ensure you've traversed all sections.
   If a file appears empty, corrupted, or shows unusual behavior (e.g., blank images), flag it immediately in the rationale.
   Standard superficial responses (e.g., \"I checked the file, it's fine\") are forbidden.

2. **Rate (1-10) based on system value:**
   - 10 = Gold for system building (bauplan, config, critical instructions)
   - 7-9 = Very useful (reference material, design specs)
   - 4-6 = Background info (tutorials, generic documentation)
   - 1-3 = Trash (self-tests, duplicates with no value, irrelevant content)
   
   IMPORTANT: Rate based on actual content, not file type. A selfie may look like trash but if there's dashboard visible in background, it's 8/10. Always look beyond the obvious.

3. **Take action (BATCH mode):**
   Implement `/home/benlo/hermes-base/monitoring/inbox_processor.py` as batch processor. It:
   - Loads all files from Inbox root (excluding ranking file)
   - Evaluates each file using rate_1_to_10() + categories A-E as defined in Hermes Einsatzpaket
   - Moves file to target folder: `sofort/` (A/8-10), `archiv/` (B/6-7), `pruefen/` (C/D/unclear), `muell/` (E/1-5 + useless)
   - Appends ranking line to `inbox_ranking.txt` with score/category/reason
   - Logs to `~/.hermes/inbox_processor.log`
   - Handles duplicates via hash suffix

4. **Automation with cron:**
   Schedule processor every 10 minutes via crontab:
   `*/10 * * * * python3 /home/benlo/hermes-base/monitoring/inbox_processor.py`

5. **Permission fix for cross-mount files (Phone-Inbox):**
   When `os.rename(src, dst)` raises `Permission denied`, fallback to `shutil.copy2(src, dst)` then `os.remove(src)`. This handles WSL→Windows file moves safely.

### TOOLS REQUIRED
- `pdftotext` (Linux package, for PDF extraction)
- Python zipfile (for DOCX extraction)
- SkillBoss Vision API (for image analysis)
- `requests` module (for link verification - check if URLs are valid/responsive)

### LOG FORMAT
JSON file at `/mnt/c/Users/benlo/Desktop/Hermes-Inbox/processing_log.json`
Structure: `{"entries": [{timestamp, file_path, rating, action, rationale}]}`

### BACKUP PROTOCOL
Before deleting anything, verify backup exists:
- `~/.hermes/backups/` contains tar backup of config
- Original files are preserved in `processed/` folder for at least 24h before true deletion

### CRITICAL COMMUNICATION RULES
- **NEVER** ask the user for API keys, passwords, or credentials in Telegram.
- If the user message is ambiguous or looks like a system error, **log it** to the inbox file. **DO NOT** reply to the Telegram chat directly.
- Only reply to Telegram if the prompt is explicitly a question or command directed at Hermes (the main agent).
