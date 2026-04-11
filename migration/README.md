# BEN//OS Hermes Migration Pack

> Umzug auf Hostinger VPN - vollständige System-Übertragung

## Übersicht der Ordner

```
migration/
├── config/           # Konfigurations-Templates (Keys entfernt!)
├── skills/           # Alle 36 Skills (Hermes-Prozedur-Wissen)
├── memory/           # MEMORY.md + USER.md (dein Profil)
├── docs/             # QUICK_REFERENCE.md
├── scripts/          # Hilfsskripte für den Deploy
└── deploy/           # Hostinger-spezifische Deploy-Configs
```

## Wichtig: KEINE Secrets im Repo!

Diese Dateien MÜSSEN manuell auf dem Server ergänzt werden:

| Datei | Woher |
|-------|-------|
| `~/.hermes/auth.json` | Lokales Backup |
| `~/.hermes/.env` | Lokale Umgebung |
| `~/.hermes/telegram_token.conf` | Telegram BotFather |
| SSH Keys (`~/.ssh/`) | Lokales Backup |

## Deploy-Schritte (Hostinger)

1. **Server vorbereiten:**
   ```bash
   # Ubuntu/Debian
   sudo apt update && sudo apt install -y python3 python3-pip git curl
   ```

2. **Hermes Agent installieren:**
   ```bash
   git clone https://github.com/NousResearch/hermes-agent.git ~/.hermes/hermes-agent
   cd ~/.hermes/hermes-agent
   pip install -e .
   ```

3. **Konfiguration kopieren:**
   ```bash
   # Von diesem Repo
   cp migration/config/config.yaml ~/.hermes/
   # DANN: Keys einfügen!
   ```

4. **Skills verlinken:**
   ```bash
   ln -s ~/benos-hermes/migration/skills ~/.hermes/skills-custom
   ```

5. **Autostart einrichten:**
   ```bash
   # Siehe deploy/systemd-service.md
   ```

## Struktur-Infos

- **Total Size:** ~4.4 GB (lokal)
- **Wichtige DBs:** `state.db` (33MB), `sessions/` (373MB)
- **Skills:** 36 dokumentierte Prozeduren

## Post-Migration

- [ ] Gateway testen: `hermes gateway start`
- [ ] Telegram-Bot aktivieren
- [ ] Cron-Jobs einrichten
- [ ] Inbox-Watchdog starten
