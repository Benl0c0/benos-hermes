#!/usr/bin/env python3
"""
BEN//OS Daily Task Scheduler
Plant kostenlose System-Checks über den Tag verteilt.
Kein Cron nötig — Cron-Jobs machen wir später wenn OctoBot steht.
"""
import json
import os
from datetime import datetime

SCHEDULE_DIR = os.path.expanduser("~/benos/scripts")
LOG_DIR = os.path.expanduser("~/benos/logs")

TASKS = {
    "08:00": {
        "name": "Morning System Check",
        "desc": "Disk, RAM, temp files, apt updates verfuegbar?",
        "commands": [
            "df -h / /mnt/c",
            "free -h",
            "du -sh ~/.cache/ /tmp/",
        ],
        "cost": 0.0,
        "needs_api": False,
    },
    "12:00": {
        "name": "Midday Security",
        "desc": "Pruefe ob offene Ports, laufende Prozesse, Login-Versuche",
        "commands": [
            "ss -tlnp 2>/dev/null | head -10",
            "last -n 5 2>/dev/null",
        ],
        "cost": 0.0,
        "needs_api": False,
    },
    "18:00": {
        "name": "Evening Cleanup",
        "desc": "Temp-Files, Logs rotieren, alter Kram entfernen",
        "commands": [
            "find /tmp -type f -atime +1 -delete 2>/dev/null",
            "journalctl --vacuum-time=2d 2>/dev/null",
        ],
        "cost": 0.0,
        "needs_api": False,
    },
    "22:00": {
        "name": "Daily Summary",
        "desc": "Zusammenfassung des Tages: Kosten, Tasks, Systemstatus",
        "commands": [
            "echo 'Daily Summary'",
            "ls -la ~/benos/logs/api_calls_$(date +%Y-%m-%d).jsonl 2>/dev/null",
        ],
        "cost": 0.0,
        "needs_api": False,
    },
}

def generate_crontab():
    """Generiert einen Crontab-Eintrag fuer alle Tasks."""
    entries = []
    for time_str, task in TASKS.items():
        hour, minute = time_str.split(":")
        # Wir koennen nicht einfach Shell-Commands aus Crontab feuern
        # Stattdessen: Ben ruft Hermes zu diesen Zeiten an
        # ODER: Wir nutzen einen echten Cron
        entries.append(f"# {time_str} - {task['name']}")
        if not task['needs_api']:
            for cmd in task['commands']:
                entries.append(f"{minute} {hour} * * * {cmd}")
    return "\n".join(entries)

print("=== BEN//OS TASK SCHEDULE ===")
for time_str, task in TASKS.items():
    api = "API-CALL" if task['needs_api'] else "KOSTENLOS"
    print(f"{time_str} - {task['name']} [{api}]")
    print(f"   {task['desc']}")
    if not task['needs_api']:
        for cmd in task['commands']:
            print(f"   > {cmd}")
    print()

crontab = generate_crontab()
print("\n=== CRONTAB CONTENT (for later) ===")
print(crontab)
