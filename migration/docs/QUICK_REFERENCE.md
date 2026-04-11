# Ben's Hermes Quick Reference

## Alles Wichtige auf einen Blick

### Telegram Befehle (Chat)
/status                 - Systemstatus abfragen
/help                   - Diese Hilfe im Chat
/check inbox            - Manuelle Inbox-Prüfung

### Terminal Befehle (WSL)

#### System & Health
hermes health           - Kompletter System-Check
hermes memory           - Speicherstatus & Backups
hermes backup           - Backup erstellen
hermes sessions         - Sessions auflisten

#### Inbox Control
hermes-watchdog start   - Watchdog AN (Auto-Poll alle 10min)
hermes-watchdog stop    - Watchdog AUS (manuell)
hermes-watchdog status  - Status checken
hermes-watchdog restart - Stopp + Start

**WICHTIG:** Standardmässig AUS. Telegram liefert Echtzeit. Watchdog nur für Backup/Offline.

#### Mit Tastatur-Shortcuts
- Strg+C          - Aktuellen Prozess stoppen
- Strg+Z          - Prozess pausieren (fg zum fortsetzen)
- Strg+D          - Terminal schliessen

### Dateien & Pfade
MEMORY:       ~/.hermes/memories/MEMORY.md     (Deine Präferenzen)
State DB:     ~/.hermes/state.db               (Läuft)
Logs:         ~/.hermes/logs/                  (Logs)
Inbox:        ~/.hermes/inbox/                 (Dateien für Hermes)
Desktop Sync: /mnt/c/Users/benlo/OneDrive/Desktop (Windows Desktop)

### Tägliches Workflow
1. `hermes-watchdog status` - wenn Aus, bleibt Aus (Telegram reicht)
2. Bei Problemen: `hermes health` für Diagnose
3. Neue Präferenzen: Einfach in Chat schreiben, ich speicher sie
4. Files in ~/.hermes/inbox/ legen, Hermes verarbeitet sie

### Emergency Stopps
"in bett" oder "kein bock mehr" → SOFORT alles stoppen
Nicht neu starten, einfach liegen lassen.

### Tipps
- Kurze Sätze bevorzugt
- "erst fertig dann weiter" – ich arbeite tasks komplett ab
- Bei System-relevanten Änderungen frag ich vorher
- Trust-Level: "Apply Always" – ich entscheide autonom
- Du bist der Architekt (51%), ich bin der Bauarbeiter (49%)

---

Erstellt: 2026-04-05
Letzte Änderung: Phase 6 Testsuite + Watchdog Control
