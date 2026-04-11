---
name: wsl-desktop-sync
version: 1.0.0
description: "Create folders or files that are visible on a Windows Desktop from within WSL (Windows Subsystem for Linux)."
homepage: https://learn.microsoft.com/en-us/windows/wsl/filesystems
last_updated: 2026-04-02
---

# WSL2 to Windows Desktop Ordner erstellen

Wenn der User keine Ahnung von WSL hat und einen Ordner "direkt auf dem Desktop" will:

## Wichtiger Hinweis
Der User ist im WSL2-Terminal, der Ordner soll aber im Windows-Explorer unter `C:\Users\<username>\Desktop\` auftauchen.

## Schritt 1: Windows-Usernamen finden

```bash
ls /mnt/c/Users/ | head -20
```
Der erste Ordnername (außer "Public") ist der Windows-Username (meist gleich dem Linux-User).

## Schritt 2: Ordner erstellen

```bash
mkdir -p "/mnt/c/Users/<username>/Desktop/<Ordnername>"
echo "Inhalt" > "/mnt/c/Users/<username>/Desktop/<Ordnername>/README.txt"
```

## Schritt 3: Pfad für den User

Wenn der User den Ordner im Windows-Explorer sucht:
- `\\wsl.localhost\<Distro>\home\<user>\<Ordner>`
- Oder: `\\wsl$\Ubuntu\home\<user>\<Ordner>`

Alternativ: PowerShell-Befehl `explorer.exe wsl:\home\<user>\<Ordner>`

## Troubleshooting

| Problem | Lösung |
|---------|--------|
| Ordner nicht sichtbar | `/mnt/c/Users` hat keinen Schreibzugriff -- prüfe `ls -la /mnt/c/Users/` |
| Permission denied | Führe als root aus (`sudo`) oder prüfe NTFS-Berechtigungen |
| Explorer öffnet nicht | Pfad enthält Umlaute oder Sonderzeichen -- umgehe sie |
| Desktop-Pfad leer | Windows-Benutzername != Linux-Username -- prübe mit `ls /mnt/c/Users/` |