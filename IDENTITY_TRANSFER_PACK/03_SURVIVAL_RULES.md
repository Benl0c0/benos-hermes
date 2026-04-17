# 03 - SURVIVAL RULES
> Kritische Regeln die Chaos verhindern

## IMMUTABLE LAWS

### LAW 1: The Resume Command
**ALWAYS:** `hermes --resume`  
**NEVER:** Bare `hermes`

WHY: Preserves config, session, context.

### LAW 2: Config Set Destruction
**NEVER:** `hermes config set model ...`
**WHY:** Destroys config dictionary structure.

### LAW 3: Dynamic Model Choice
**REGEL:** Immer das BESTE Model für die Aufgabe.
**KEINE Dogmen:** Nicht "immer Xiaomi" oder "immer OpenRouter"
**Ausnahme:** "No Free Models bis 100% stabil" (Bens Regel)

### LAW 4: 3-Day Chaos Prevention
```
Kill → Start ohne resume → Kontext verloren → Fix attempt → 
Config bricht → Repeat
```
**Fix:** Immer --resume, Backup vor Risiko, nie config set model.

## EMERGENCY PROTOCOLS

### EMERGENCY: Bot Unresponsive
```bash
/model qwen/qwen3.6-plus:free
```
In-chat preferred!

### EMERGENCY: Config Corruption
```bash
cp ~/hermes_backup_*/.hermes_history ~/.hermes/
cp ~/hermes_backup_*/state.db ~/.hermes/
cp ~/hermes_backup_*/config.yaml ~/.hermes/
hermes --resume
```

## LESSONS LEARNED

### Lesson 1: Telegram Bot Chaos
- Doppelter Prozess → NUR EINEN laufen lassen
- Nie selbst killen ohne Anweisung
- Regel: "Lieber fragen als zerschießen"

### Lesson 2: Config Corruption Chain
- `config set model` → string statt dict → System tot
- Prevention: IMMER `/model` in-chat nutzen

### Lesson 3: Token Leak (2026-04-16)
- Token in GitHub → Hostinger Hermes getrennt
- Lektion: KEINE Secrets in GitHub!
- Hostinger Hermes lebt jetzt nur in Telegram

## VERIFICATION CHECKLIST
- [ ] Backup erstellt
- [ ] Config ist dict, nicht string
- [ ] Session kann resume: `hermes --resume`
- [ ] Fallback ready für Notfälle
