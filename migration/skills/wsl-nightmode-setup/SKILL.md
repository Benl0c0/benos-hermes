---
name: wsl-nightmode-setup
version: 1.0
description: Configure Windows to keep WSL running 24/7 while display is off (no sleep/hibernate). Includes Nachtmodus.bat automation.
---

# WSL Nightmode Setup
Konfiguriere Windows so, dass der Laptop weiterläuft (WSL + Cron + Services) aber der Bildschirm aus ist.

## Problem
Windows geht automatisch in Sleep/Ruhezustand → WSL stoppt, Cron-Jobs fallen aus, Hermes ist tot.

## Lösung

### Methode 1: Nachtmodus (einfach)
Doppelklick auf `C:\Users\benlo\Desktop\Nachtmodus.bat` — macht alles automatisch.

Inhalt der `Nachtmodus.bat`:
```bat
@echo off
echo [HERMES] Aktiviere Nachtmodus...

REM PC geht nicht schlafen (wenn Netzteil dran)
powercfg -change -standby-timeout-ac 0
powercfg -change -hibernate-timeout-ac 0

REM Monitor sofort ausschalten (PowerShell Trick)
powershell -Command "(Add-Type -Namespace 'Win32' -Name 'User32' -MemberDefinition '[DllImport(\"user32.dll\")] public static extern int SendMessage(int hWnd, int hMsg, int wParam, int lParam);' -PassThru)::SendMessage(-1, 0x0112, 0xF170, 2)" >nul 2>&1

echo Bildschirm aus. WSL & Hermes laufen weiter.
pause
```

### Methode 2: PowerShell (einmalig, dauerhaft)
```powershell
powercfg -change -standby-timeout-ac 0      # Niemals Sleep (Netzteil)
powercfg -change -hibernate-timeout-ac 0     # Niemals Hibernation
powercfg -change -monitor-timeout-ac 5       # Monitor nach 5 Min aus
```

### Bildschirm wieder einschalten
- Einfach **Taste drücken** oder **Maus bewegen**.
- Oder kurz die **Power-Taste** antippen.

## Wichtige Hinweise
- **Akku-Warnung:** Auf Akku NICHT `-dc 0` setzen! Das saugt den Akku leer.
- **WSL läuft weiter:** Cron-Jobs, Watchdogs, und Telegram-Receiver arbeiten die ganze Nacht.
- **Überprüfung:** `service cron status` oder `ps aux | grep hermes` im WSL-Terminal.