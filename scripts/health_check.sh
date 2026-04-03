#!/bin/bash
# BEN//OS System Health Check
# Kostenlos - kein API Call nötig

echo "=== BEN//OS SYSTEM STATUS ==="
echo "Zeit: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

echo "--- SYSTEM ---"
echo "OS: $(uname -r)"
echo "Uptime: $(uptime -p)"
echo "Load: $(uptime | awk -F'load average:' '{print $2}')"
echo ""

echo "--- MEMORY ---"
free -h | head -2
echo ""

echo "--- DISK ---"
df -h / /mnt/c 2>/dev/null | grep -E '^/'
echo ""

echo "--- CACHE USAGE ---"
du -sh ~/.cache/ 2>/dev/null || echo "Kein Cache"
echo "---"
du -sh /tmp/ 2>/dev/null || echo "Kein /tmp"
echo ""

echo "--- NETWORK ---"
curl -s --connect-timeout 3 https://api.heybossai.com/v1/models > /dev/null 2>&1 && echo "Internet: OK" || echo "Internet: DOWN"
echo ""

echo "--- APT UPDATES ---"
apt list --upgradable 2>/dev/null | grep -c "upgradable" || echo "0"
echo "Updates verfuegbar"
