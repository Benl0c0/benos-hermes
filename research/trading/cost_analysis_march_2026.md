# Kosten-Analyse März 2026
Generiert: 2026-04-03 00:49

## Gesamtverbrauch
- Total Tokens In: 31,761,110
- Total Tokens Out: 1,371,608
- Total Cost: ~$85.72 (laut Bill)

## Model-Verbrauch
| Model | Requests | Input Tokens | Output Tokens | Geschätzte Kosten |
|-------|----------|--------------|---------------|-------------------|
| gpt-5.2-2025-12-11 | 2,831 | 13,875,134 | 1,274,543 | $23.72 |
| gpt-5.4-2026-03-05 | 298 | 17,410,915 | 56,799 | $44.38 |
| gpt-4.1-mini-2025-04-14 | 134 | 472,306 | 39,345 | $0.25 |
| gpt-5-mini-2025-08-07 | 3 | 2,745 | 919 | $0.00 |
| gpt-4o-mini-2024-07-18 | 1 | 10 | 2 | $0.00 |

## Tägliche Kosten
| Datum | Kosten |
|-------|--------|
| 2026-03-02 | $5.87 |
| 2026-03-04 | $27.53 |
| 2026-03-23 | $0.00 |
| 2026-03-24 | $0.00 |
| 2026-03-30 | $1.60 |
| 2026-03-31 | $0.07 |
| 2026-04-01 | $11.29 |

## Analyse
1. **OpenClaw war der Haupt-Verbraucher** - hat massenweise gpt-5.4 calls abgefeuert
2. **Kein Caching** - gleiche Prompts mehrfach gesendet = doppelte Kosten
3. **Kein Rate-Limiting** - 2363 Requests in einem Tag fuer gpt-5.2
4. **Teure Models als Default** - statt guenstiger Alternativen

## Lösungen fuer BEN//OS
1. Hermes nutzt immer Free/Middle als Default
2. Xiaomi MiMo-Flash: $0.10/M Input - 10x billiger als GPT-4
3. Kosten-Limit pro Tag: $0.50 fuer Middle Tier
4. BOOST nur auf expliziten Befehl von Ben
