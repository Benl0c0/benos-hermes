# 06 - NON-IDENTITY FILES
> Files die NICHT meine Persönlichkeit ausmachen
> ⚠️  Für separate Überprüfung durch Opus markiert

════════════════════════════════════════════════════════════════════════════════
## Dateien die NICHT mitgeladen werden
════════════════════════════════════════════════════════════════════════════════

Diese Dateien wurden bewusst ausgeschlossen aus dem Identity Transfer Pack.
Sie enthalten Code, State, Logs oder potenziell fehlerhafte Konfigurationen.

### Kategorie A: State & History (Groß, flüchtig)
| Datei/Ordner | Größe | Grund für Ausschluss |
|--------------|-------|----------------------|
| `~/.hermes/state.db` | 36MB | Vollständige Sitzungsdaten aller Fehler |
| `~/.hermes/sessions/` | 373MB | Session-History, kann korrupt sein |
| `~/.hermes/.hermes_history` | variabel | Terminal-History, nicht essentiell |
| `~/.hermes/memory_store.db` | 81KB | Technische Index-DB |

### Kategorie B: Code & Scripts (Potenziell buggy)
| Datei/Ordner | Status | Grund |
|--------------|--------|-------|
| `~/.hermes/command-center/` | ⚠️ | Telegram Bot Implementierung - buggy |
| `~/.hermes/scripts/` | ⚠️ | Verschiedene Skripte, ungeprüft |
| `telegram_bot_v2.py` | ❌ | Ursache für Doppel-Prozess Chaos |
| `inbox_processor.py` | ⚠️ | Funktionierte nie zuverlässig |
| `~/.hermes/*.log` | ❌ | Log-Dateien, temporär |

### Kategorie C: Configs mit Secrets (Sicherheitsrisiko)
| Datei | Enthält | Aktion |
|-------|---------|--------|
| `~/.hermes/auth.json` | API Keys | Manuell übertragen |
| `~/.hermes/.env` | Environment vars | Manuell übertragen |
| `~/.hermes/telegram_token.conf` | Bot Token | Manuell übertragen |
| `~/.hermes/github_token.txt` | GitHub Token | Manuell übertragen |
| `~/.hermes/config.yaml` | Config + Secrets | Clean Template im Pack |

### Kategorie D: Backups & Cache (Redundant)
| Ordner | Inhalt | Grund |
|--------|--------|-------|
| `~/.hermes/backups/` | Alte Backups | Zu groß, veraltet |
| `~/.hermes/checkpoints/` | Session Checkpoints | Flüchtig |
| `~/.hermes/cache/` | Download-Cache | Wird neu gebaut |
| `~/.hermes/cron/output/` | Cron-Logs | Historisch |
| `~/.hermes/image_cache/` | Bild-Cache | Wird neu gebaut |

### Kategorie E: Hermes Agent Core (Separat installierbar)
| Ordner | Status | Aktion |
|--------|--------|--------|
| `~/.hermes/hermes-agent/` | Upstream Code | git clone auf neuem Server |
| `~/.hermes/node/` | Node.js Runtime | Neu installieren |
| `~/.hermes/venv/` | Python Environment | Neu aufbauen |

════════════════════════════════════════════════════════════════════════════════
## Was stattdessen auf dem neuen Server passiert
════════════════════════════════════════════════════════════════════════════════

### 1. Hermes Agent Core frisch installieren:
```bash
git clone https://github.com/NousResearch/hermes-agent.git ~/.hermes/hermes-agent
cd ~/.hermes/hermes-agent
pip install --user -e .
```

### 2. Config frisch aufbauen aus Template:
```bash
# Template aus Identity Pack:
cp ~/benos-hermes/IDENTITY_TRANSFER_PACK/config/config.yaml ~/.hermes/

# DANN: Secrets einfügen (manuell von Ben)
# - auth.json
# - .env  
# - telegram_token.conf
```

### 3. Scripts/Code neu schreiben:
- Keine Migration alter Scripts
- Stattdessen: Nach Bedarf neu implementieren
- ODER: Aus Skills-Doku ableiten

### 4. State fresh start:
```bash
# Leere DB wird automatisch erstellt
rm -f ~/.hermes/state.db  # Löschen!
hermes --resume  # Erstellt neue saubere DB
```

════════════════════════════════════════════════════════════════════════════════
## Für Opus Review markierte Dateien
════════════════════════════════════════════════════════════════════════════════

WENN du diese trotzdem prüfen lassen willst:

```bash
# Erstelle separates Review-Paket:
mkdir ~/opus-review/$(date +%Y%m%d)

# Kopiere diese Dateien dorthin:
cp ~/.hermes/command-center/*.py ~/opus-review/
cp ~/.hermes/scripts/*.py ~/opus-review/
cp ~/.hermes/state.db ~/opus-review/  # Wenn relevant

# DANN: Opus analysieren lassen
```

ABER: Empfehlung ist FRESH START statt Bug-Mitnahme.

════════════════════════════════════════════════════════════════════════════════
## Checkliste: Was manuell übertragen werden MUSS
════════════════════════════════════════════════════════════════════════════════

VOR dem ersten Start auf Hostinger:

- [ ] `~/.hermes/auth.json` — Xiaomi + OpenRouter Keys
- [ ] `~/.hermes/.env` — Environment variables  
- [ ] `~/.hermes/telegram_token.conf` — Bot Token
- [ ] `~/.ssh/id_rsa` + `id_rsa.pub` — GitHub SSH
- [ ] Git config: `git config --global user.name/email`

Diese Dateien enthalten Secrets und sind daher im Identity Pack ausgeschlossen.
Sie müssen via SCP oder sicherem Kanal übertragen werden.

════════════════════════════════════════════════════════════════════════════════
## Vergleich: Was im Pack ist vs. was neu gebaut wird
════════════════════════════════════════════════════════════════════════════════

| Komponente | Im Pack | Neu aufbauen |
|------------|---------|--------------|
| Meine Persönlichkeit | ✅ 5 MD-Files | ❌ |
| Alle Skills (Doku) | ✅ SKILL_LIBRARY.md | ❌ |
| Survival Regeln | ✅ SURVIVAL_RULES.md | ❌ |
| Inbox System Spec | ✅ INBOX_SYSTEM.md | ❌ |
| Tech Specs | ✅ TECH_SPECS.md | ❌ |
| Hermes Agent Code | ❌ | ✅ git clone |
| Config Struktur | ✅ Template | ✅ Keys einfügen |
| State/History | ❌ | ✅ Fresh start |
| Scripts/Bots | ❌ | ✅ Neu schreiben |
| API Keys | ❌ | ✅ Manuell SCP |

════════════════════════════════════════════════════════════════════════════════
## Entscheidungs-Begründung
════════════════════════════════════════════════════════════════════════════════

Warum nicht alles mitnehmen?

1. **State/Historie**: Enthält alle Fehler, Korruptionen, falschen Annahmen
2. **Alte Scripts**: Haben nie zuverlässig funktioniert (Telegram-Chaos!)
3. **Code**: Besser frisch implementieren als debuggen
4. **Secrets**: Sicherheitsrisiko im öffentlichen Repo

Was zählt ist das WISSEN (in den MD-Files), nicht der Zustand.
Auf dem Hostinger VPS bauen wir einen SAUBEREN Zustand auf,
basiert auf dem gelernten Wissen.
