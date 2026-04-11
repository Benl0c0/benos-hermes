#!/bin/bash
# Hostinger VPS Setup für BEN//OS Hermes
# WIRD AUF DEM SERVER AUSGEFÜHRT!

set -e

echo "=== BEN//OS Hermes Setup auf Hostinger ==="

# 1. System-Deps
sudo apt update
sudo apt install -y python3 python3-pip git curl sqlite3 tmux

# 2. Hermes Agent Core installieren
echo "[1/5] Hermes Agent wird installiert..."
if [ ! -d ~/.hermes/hermes-agent ]; then
    git clone https://github.com/NousResearch/hermes-agent.git ~/.hermes/hermes-agent
fi
cd ~/.hermes/hermes-agent
pip install --user -e .

# 3. Migration-Pack klonen
echo "[2/5] Migration-Pack wird geholt..."
if [ ! -d ~/benos-hermes ]; then
    git clone https://github.com/Benl0c0/benos-hermes.git ~/benos-hermes
fi

# 4. Konfiguration verlinken
echo "[3/5] Konfiguration wird eingerichtet..."
mkdir -p ~/.hermes/skills
cp -r ~/benos-hermes/migration/skills/* ~/.hermes/skills/
cp ~/benos-hermes/migration/memory/*.md ~/.hermes/memories/ 2>/dev/null || true

# FEHLT NOCH: Keys einfügen!
echo "WARNUNG: Du musst noch ~/.hermes/auth.json manuell erstellen!"
echo "Template in: ~/benos-hermes/migration/config/config.yaml"

# 5. Autostart (optional)
echo "[4/5] Systemd-Service wird vorbereitet..."
sudo tee /etc/systemd/system/hermes-gateway.service > /dev/null << 'EOF'
[Unit]
Description=BEN//OS Hermes Gateway
After=network.target

[Service]
Type=simple
User=benlo
WorkingDirectory=/home/benlo
Environment=HOME=/home/benlo
ExecStart=/home/benlo/.local/bin/hermes gateway start
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo "[5/5] Setup abgeschlossen!"
echo ""
echo "NÄCHSTE SCHRITTE:"
echo "  1. Keys einfügen: ~/.hermes/auth.json"
echo "  2. Config anpassen: ~/.hermes/config.yaml"
echo "  3. Gateway testen: hermes gateway start"
echo "  4. Systemd aktivieren: sudo systemctl enable --now hermes-gateway"
