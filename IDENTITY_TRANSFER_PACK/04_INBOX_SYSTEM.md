# 04 - INBOX SYSTEM
> Komplettes Inbox-Verarbeitungs-System für Ben

════════════════════════════════════════════════════════════════════════════════
## SYSTEM OVERVIEW
════════════════════════════════════════════════════════════════════════════════

ZWECK: Automatische Analyse, Bewertung und Sortierung eingehender Files

QUELLEN:
- `/mnt/c/Users/benlo/Desktop/Hermes-Inbox/` (Hauptordner, recursive)
- `/mnt/c/Users/benlo/Desktop/Hermes-Inbox/bens Smartphone - Inbox/` (Phone sync)

ZIEL: 알아서 (automatisch) verarbeiten — Ben muss nichts tun

════════════════════════════════════════════════════════════════════════════════
## PRIORITY SYSTEM (STRICT ORDER)
════════════════════════════════════════════════════════════════════════════════

```
ALARM (1) → RESEARCH_PRE (2) → RESEARCH_RAW (3)
   │              │                   │
 SOFORT      ANALYSIEREN          ABLEGEN
  FIXEN      + TELEGRAM            (grob)
```

### Prio 1: ALARM
**Trigger:** Systemkritisch, sofortige Aktion nötig  
**Action:** Sofort fixen, Telegram Alert  
**Beispiele:**
- Config zerstört
- Bot offline
- Cron failed
- Security issue

### Prio 2: RESEARCH_PRE  
**Trigger:** Braucht Analyse vor Archivierung  
**Action:** Analysieren + Telegram Preview senden  
**Beispiele:**
- Neue Tool-Dokumentation
- Interessanter Artikel
- Design-Screenshot
- Code-Beispiel

### Prio 3: RESEARCH_RAW
**Trigger:** Info-Material, später relevant  
**Action:** Grob ablegen, nicht sofort verarbeiten  
**Beispiele:**
- Tutorial-Links
- Background reading
- Reference material

════════════════════════════════════════════════════════════════════════════════
## FILE TYPE PROCESSING
════════════════════════════════════════════════════════════════════════════════

### Images (.jpg, .png, .jpeg)
**Tool:** SkillBoss Vision (openai/gpt-4o via API)  
**Extrahiert:**
- Layout und UI-Elemente
- Sichtbarer Text (OCR)
- Design-Struktur
- Farbschema
**USE CASE:** Dashboard-Screenshots, Design-Mockups, Infografiken

### DOCX (Word)
**Tool:** `docx2txt` CLI command  
**⚠️ WARNUNG:** NIEMALS python-docx Modul im Sandbox verwenden!
- Fehlendes docx Modul
- Links brechen API
**Command:** `docx2txt <file> /tmp/output.txt`

### PDF
**Tool:** `pdftotext` command  
**Package:** poppler-utils (Linux)  
**Command:** `pdftotext <file> -` (stdout)

### HTML
**Tool:** `browser_navigate` + `browser_snapshot`  
**Vorgehen:**
1. URL laden
2. Full structure analysieren
3. Content extrahieren
4. Links folgen (siehe Link-Following Rule)

### TXT / Markdown
**Tool:** Direct read  
**Action:** Content lesen, Links verfolgen, validieren

════════════════════════════════════════════════════════════════════════════════
## CRITICAL RULES
════════════════════════════════════════════════════════════════════════════════

### RULE 1: Link Following (MANDATORY)
```
WENN file enthält URL/link:
  DANN ALWAYS browser_navigate verwenden
  UND Ziel öffnen
  UND MINIMUM 2 Ebenen tief folgen
  
  WENN Ziel enthält ANOTHER link:
    DANN weiter folgen
    BIS echte Datei/Info erreicht
  
  NIE als "trash" bewerten nur weil "nur ein link"
  → Der Link IST das Content Gateway!
```

**BEISPIEL:**
- File: "please study this" + Link
- FALSCH: "Nur ein Link → Trash 2/10"
- RICHTIG: Link folgen → Content analysieren → Bewertung basierend auf Ziel

**PITFALL:**  
A file that says "please study this" + a link is NOT trash — it's a pointer to valuable info. Always verify before rating.

---

### RULE 2: Full Inspection (MANDATORY)
```
NIE bei erster Seite/first few lines aufhören
IMMER bis zum Ende lesen/scrollen
WENN file empty/corrupted/ungewöhnlich:
  DANN SOFORT flaggen in rationale
```

**VERBOTEN:**  
Standard superficial responses (e.g., "I checked the file, it's fine")

---

### RULE 3: Rate Based on ACTUAL Content
```
NICHT basierend auf file type bewerten
SONDERN auf tatsächlichem Inhalt
```

**BEISPIELE:**
- Selfie mit Dashboard im Hintergrund → 8/10 (nicht 2/10!)
- Screenshot mit critical info → 9/10
- "Nur" ein Link → Folgen, dann bewerten

════════════════════════════════════════════════════════════════════════════════
## RATING SYSTEM (1-10)
════════════════════════════════════════════════════════════════════════════════

| Score | Category | Meaning | Action |
|-------|----------|---------|--------|
| 10 | Gold | System-building critical | Sofort implementieren |
| 9 | Platinum | Critical reference | Archiv + Tag |
| 8 | High Value | Very useful, design specs | Archiv + cross-ref |
| 7 | Good | Useful reference | Archiv |
| 6 | OK | Background info | Prüfen/Archiv |
| 5 | Meh | Generic documentation | Prüfen |
| 4 | Low | Tutorial, kann nützlich sein | Prüfen |
| 3 | Dubious | Unclear value | Prüfen/Risiko |
| 2 | Trash | Self-tests, obvious spam | Müll |
| 1 | Junk | Duplicates, no value | Müll + Delete |

### Category Mapping:
```
A/8-10  → sofort/     (Immediate action)
B/6-7   → archiv/     (Store for ref)
C/D     → pruefen/    (Manual review)
E/1-5   → muell/      (Trash)
```

════════════════════════════════════════════════════════════════════════════════
## BATCH PROCESSING
════════════════════════════════════════════════════════════════════════════════

### Processor: inbox_processor.py
**Location:** `/home/benlo/hermes-base/monitoring/inbox_processor.py`

**Function:**
1. Load all files from Inbox root (excluding ranking file)
2. Evaluate each with `rate_1_to_10()` + categories A-E
3. Move to target folder based on score
4. Append ranking to `inbox_ranking.txt`
5. Log to `~/.hermes/inbox_processor.log`
6. Handle duplicates via hash suffix

### Cron Schedule:
```bash
*/10 * * * * python3 /home/benlo/hermes-base/monitoring/inbox_processor.py
```
→ Every 10 minutes

### Permission Fix:
**Problem:** `os.rename()` fails cross-mount (WSL→Windows)  
**Solution:**
```python
try:
    os.rename(src, dst)
except PermissionError:
    # Fallback for cross-mount
    shutil.copy2(src, dst)
    os.remove(src)
```

════════════════════════════════════════════════════════════════════════════════
## LOGGING & TRACKING
════════════════════════════════════════════════════════════════════════════════

### Processing Log:
**Location:** `/mnt/c/Users/benlo/Desktop/Hermes-Inbox/processing_log.json`

**Structure:**
```json
{
  "entries": [
    {
      "timestamp": "2026-04-11T12:00:00Z",
      "file_path": "...",
      "rating": 8,
      "action": "moved_to_archiv",
      "rationale": "Dashboard screenshot with valuable UI patterns"
    }
  ]
}
```

### Ranking File:
**Location:** `inbox_ranking.txt` (in Inbox root)

**Format:**
```
[2026-04-11 12:00] file.jpg | Score: 8/10 | Category: A | Action: archiv | Rationale: ...
```

════════════════════════════════════════════════════════════════════════════════
## BACKUP PROTOCOL
════════════════════════════════════════════════════════════════════════════════

**Before Deleting ANYTHING:**
1. Verify backup exists in `~/.hermes/backups/`
2. Original preserved in `processed/` for 24h
3. Only then true deletion

**Backup Structure:**
```
~/.hermes/backups/
├── tar backup of config
├── chunk_YYYYMMDD_HHMM.json (state snapshots)
└── system_backup_YYYYMMDD_HHMMSS/ (full backup)
```

════════════════════════════════════════════════════════════════════════════════
## COMMUNICATION RULES
════════════════════════════════════════════════════════════════════════════════

### ❌ FORBIDDEN:
- Ask user for API keys/passwords in Telegram
- Reply directly to ambiguous messages
- Respond to potential system errors in chat

### ✅ REQUIRED:
- LOG ambiguous messages to file
- Only reply to explicit questions/commands
- When in doubt → Log, don't chat

### Telegram Usage:
- Process updates → internal log
- Explicit @mention or command → response
- Everything else → silent processing

════════════════════════════════════════════════════════════════════════════════
## INBOX WATCHDOG
════════════════════════════════════════════════════════════════════════════════

**Purpose:** Monitor folders for new files  
**Monitors:**
- Hermes-Inbox/ (recursive)
- bensmartphone-inbox/

**Trigger:** File create/modify event  
**Action:** Wake processor → immediate handling

**Implementation:**
- File system watcher (inotify/fswatch)
- Alternative: Poll every 60 seconds
- Integration with processor pipeline

════════════════════════════════════════════════════════════════════════════════
## WHAT NOT TO DO (AUTOMATIC)
════════════════════════════════════════════════════════════════════════════════

These were marked as FUTURE/PHASE 5-6, NOT automatic now:

❌ Auto-Wiki/Obsidian integration
❌ Claude Code automatic delegation  
❌ Auto-archiv to external systems

These are IDEAS for later, not active automation.

════════════════════════════════════════════════════════════════════════════════
## POST-MIGRATION SETUP
════════════════════════════════════════════════════════════════════════════════

1. **Adjust Paths:**
   ```python
   # OLD (WSL):
   /mnt/c/Users/benlo/Desktop/Hermes-Inbox/
   
   # NEW (VPS):
   ~/inbox/ or /var/inbox/
   ```

2. **Install Dependencies:**
   ```bash
   sudo apt install poppler-utils  # for pdftotext
   pip install docx2txt            # for DOCX
   ```

3. **Setup Watchdog:**
   ```bash
   # Option A: inotifywait (if available)
   # Option B: Cron polling every minute
   * * * * * python3 inbox_processor.py
   ```

4. **Test Processing:**
   ```bash
   # Drop test files
   echo "test" > ~/inbox/test.txt
   # Check logs
   tail -f ~/.hermes/inbox_processor.log
   ```

════════════════════════════════════════════════════════════════════════════════
## VERIFICATION CHECKLIST
════════════════════════════════════════════════════════════════════════════════

- [ ] Inbox paths configured correctly
- [ ] Processor script executable
- [ ] Dependencies installed (pdftotext, docx2txt)
- [ ] SkillBoss Vision API key configured
- [ ] Cronjob active (or watchdog running)
- [ ] Log files writable
- [ ] Backup system active
- [ ] Telegram notifications configured
- [ ] Test files processed correctly
