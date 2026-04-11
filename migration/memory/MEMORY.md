Xiaomi MIMO Pro (PAID) + OpenRouter Free; Config v12; nie 'hermes config set model', immer 'hermes --resume'.
§
System health: state.db 47.3MB (451 sessions, 13805 messages), sessions/ 93.7MB (562 files). memory_store.db 81KB (1 fact). ~/.hermes/ total 2.7GB. Holographic memory plugin active but barely used (1 fact). Memory.md 2072 chars, USER.md 1352 chars. Baseline: ~/.hermes/fixes/baseline.json.
§
INBOX PRIO: 1) Alarm — sofort fix, 2) Research_pre — analysieren+Telegram preview, 3) Research_raw — grob ablegen. Hauptkanal: Smartphone-Inbox. NICHT: automatisches Wiki/Obsidian (Phase 5/6), NICHT: Claude Code jetzt.
§
CLEARMUD.AI RESEARCH (2026-04-08): Power-User von OpenClaw (github.com/openclaw/openclaw, 351k Stars). Blog+Bootcamp öffentlich, Resources>Login für Templates. 5 YouTube-Episoden. Files: clearmud-resources/ Ordner. Ben will vollständige Analyse wenn alle Files da sind.
§
SMARTPHONE_INBOX_PATH: /mnt/c/Users/benlo/Desktop/Hermes-Inbox/bens Smartphone - Inbox
§
2026-04-11: Xiaomi MiMo V2 Flash provider switch completed. Config: model.provider=custom:xiaomi, model.default=mimo-v2-flash, base_url=https://api.xiaomimimo.com/v1. auth.json has custom:xiaomi credential pool. Custom providers entry: Xiaomi with correct base_url. Session using mimo-v2-flash successfully.
§
2026-04-11: GitHub auth setup. SSH verified (Benl0c0), git credential helper=store, SSH rewrite configured. User: Benl0c0, Email: benloco187@googlemail.com.
§
2026-04-08: Memory Limit ist 2.200 Zeichen. Das ist eine Systemgrenze. Ich kann sie nicht erhöhen.
§
PARTNERSHIP: Ben 51% (Architekt, Richtung), Hermes 49% (Bauer, autonom). "Nicht sofort bauen" — erst analysieren, dann empfehlen. Ben entscheidet, Hermes findet den Weg und baut.
§
2026-04-11: Telegram Bot Chaos Ursache: 1) Doppelter Prozess (alter `telegram_bot_v2.py` lief parallel zum Gateway). 2) Gateway startete in Endlosschleife (Systemd Limit). 3) Ich habe mit `pkill` versucht zu stoppen, was Ben blockierte. Lösung: Nur einen Prozess laufen lassen, keine Endlosschleifen, auf Anweisung warten.
§
2026-04-11: Ben will kein OpenRouter mehr nutzen. Nur Xiaomi MiMo. Keine Mischung mehr. "OpenRouter macht nur Probleme".