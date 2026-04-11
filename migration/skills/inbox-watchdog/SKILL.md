---
name: inbox-watchdog
version: 2.1
description: Watchfolders (Hermes-Inbox, bensmartphone-inbox) for new files, categorize, rank, and trigger actions. Includes Telegram alert integration.
---

# Inbox Watchdog Workflow

## Ordnerstruktur
- **Haupt-Ordner:** `/mnt/c/Users/benlo/Desktop/Hermes-Inbox/`
- **Sub-Ordner:**
  - `bens Smartphone - Inbox/` (Telefon Transfer)
  - `sofort/` (Score 8-10: direkt einbeziehen)
  - `archiv/` (Score 6-7: für später)
  - `pruefen/` (Score 4-5: unklar/Review)
  - `muell/` (Score 1-3: verwerfen)

## Pfade
- **Basis:** `/mnt/c/Users/benlo/Desktop/Hermes-Inbox` (NICHT OneDrive!)
- **Ranking-File:** `/mnt/c/Users/benlo/Desktop/Hermes-Inbox/inbox_ranking.txt`
- **Config/Token:** Telegram Bot Token in `~/.hermes/.env` (`TELEGRAM_BOT_TOKEN=...`)

## Automatisierung
1. **Cron-Job:** `inbox_processor.py` läuft alle 10 Minuten. Bewertet Dateien, verschiebt sie, sendet Telegram-Alert.
2. **Background Watcher:** `inbox_watcher.py` via `run_inbox_watcher.sh` (nur als Fallback, wenn Cron mal spinnt).
3. **Telegram Alert:** Bei jeder sortierten Datei sendet der Bot eine Nachricht an Ben (Chat ID: `2029024880`).

### Watchdog Start/Stop Steuerung
Der Inbox-Watchdog kann manuell ein- und ausgeschaltet werden. Standardmässig ist er **AUS**, Telegram-Empfang läuft aber weiterhin in Echtzeit über den Bot-Daemon.

**Befehle:**
- **Watchdog starten:** `python3 /home/benlo/.hermes/scripts/watchdog/watchdog.py start` (oder Alias: `hermes-watchdog start`)
- **Watchdog stoppen:** `python3 /home/benlo/.hermes/scripts/watchdog/watchdog.py stop` (oder Alias: `hermes-watchdog stop`)
- **Status prüfen:** `python3 /home/benlo/.hermes/scripts/watchdog/watchdog.py status` (oder Alias: `hermes-watchdog status`)

**Wann aktivieren:**
- Wenn du offline warst und einen Sync-Check brauchst
- Wenn du manuell mehrere Dateien in der Inbox hast
- Wenn du den Bot-Daemon mal neu startest und der Poller aus war

**Wann stoppen:**
- Wenn du den Watchdog nicht brauchst (Standard)
- Bei Systemwartung
- Wenn du manuell pollst (spart Ressourcen)

**Wichtig:** Der Telegram-Bot empfängt Nachrichten immer in Echtzeit, unabhängig vom Watchdog-Status. Der Watchdog pollt nur alle 10-15 Minuten die Inbox-Ordner auf neue Dateien und verarbeitet sie automatisch.

## Wichtige Fixes & Lessons Learned
- **WSL PERMISSION ISSUE:** Wenn `os.rename` \"Permission denied\" gegeben (weil Windows Datei blockiert), nutze `shutil.copy2` und ignoriere den Delete-Fehler wenn nötig.
- **WATCHDOG ZOMBIES:** Vor Neustart IMMER `pkill -f inbox_watcher` ausführen. Watchdogs häufen sich sonst (27 Prozesse = RAM Kill).
- **FEEDBACK SCHLEIFE:** Benutzer MUSS eine Nachricht bekommen, wenn Dateien verarbeitet werden. Sonst denkt er, das System sei tot.

### Non-Trivial Control Pattern
Der Watchdog lief ursprünglich ständig per Cron (alle 10-15 Min). Nach Integration mit Telegram-Echtzeit-Empfang war das zu viel und redundant. Lösung: **Manuelle Kontrolle mit Alias-Befehlen** statt automatischem Dauerbetrieb.
- Watchdog ist standardmässig AUS
- Telegram-Bot empfängt Echtzeit (kein Polling nötig)
- Watchdog nur als Offline-Fallback oder bei manuellem Bedarf startbar
- Implementiert als `watchdog.py` mit `start/stop/status` und Cron-Toggle
- Alias in `.bashrc` und `.zshrc` für einfachen Zugriff
- Ben hat damit die volle Kontrolle über den Ressourcenverbrauch

Diese Pattern (Manuelle Steuerung + Alias + Cron-Toggle) ist wiederverwendbar für andere Dienste.
