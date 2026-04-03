# BEN//OS - KIRA Multi-Agent System

## Projektbeschreibung

BEN//OS (operating as KIRA) ist ein Multi-Agent System, das verschiedene spezialisierte Agenten orchestriert, um komplexe Aufgaben in Bereichen wie Intelligence, Content-Erstellung, Trading und technische Umsetzung zu bewältigen. Das System nutzt den Hermes Agenten als zentrale Koordinationsschicht und ermöglicht persistente Kontextübertragung zwischen Sessions.

## Verzeichnisstruktur

- **config/** - Konfigurationsdateien für KIRA, inkl. Model-Routing-Matrix
- **agents/** - Agent-Definitionen (Intel, Content, Trading, CTO)
- **research/** - Research-Ergebnisse und Reports
- **memory/** - Persistierter Kontext zwischen Sessions (langfristiges Gedächtnis)
- **logs/** - Laufprotokolle und Fehler-Logs
- **scripts/** - Automatisierungs-Skripte (Setup, Wartung, Deployment)
- **dashboard/** - Dashboard-Dateien (HTML, JSON) für Visualisierung
- **skills/** - Custom BEN//OS Skills (falls nicht in Hermes Core enthalten)
- **.gitkeep** - Platzhalterdateien für leere Verzeichnisse in Git

## Stand der Dinge

Infrastruktur wurde eingerichtet. Die Basisordner und .gitkeep-Dateien sind angelegt. Die Model-Routing-Konfiguration (config/model-routing.json) wurde erstellt. Custom Skills sind bereits unter ~/.hermes/skills/benos-* verfügbar und werden von diesem System referenziert.

## Nächste Schritte (aus Kontext-Briefing)

1. Skills-Integration prüfen und list-model-routing implementieren
2. Agent-Definitionen in JSON/YAML/TOML erstellen
3. Persistenz-Layer implementieren (SQLite/JSON)
4. Dashboard mit Live-Logs und Status bauen
5. Automatisierungs-Skripte für Setup/Deployment
6. Konfigurations-Management vervollständigen
7. Agent-Orchestrierung testen
8. Monitoring und Error-Handling

---

*Erstellt: 2026-04-03*
*Umgebung: WSL2 auf Windows, Arbeitsverzeichnis: /home/benlo/*
