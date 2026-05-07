#!/bin/bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

echo "Node version: $(node --version)"

# Get current Windows WiFi IP automatically
WIN_IP=$(powershell.exe -Command "ipconfig" 2>/dev/null \
  | iconv -f cp866 -t utf-8 2>/dev/null \
  | grep "IPv4" \
  | grep -v "169.254" \
  | grep -v "172.29" \
  | grep -oP '[\d]+\.[\d]+\.[\d]+\.[\d]+' \
  | head -1)

if [ -z "$WIN_IP" ]; then
  WIN_IP="192.168.0.125"
  echo "Could not detect IP, using: $WIN_IP"
else
  echo "Detected Windows IP: $WIN_IP"
fi

# Update client.ts with current IP
sed -i "s|const BASE_URL = 'http://[^']*';|const BASE_URL = 'http://$WIN_IP:8000/api/v1';|" \
  /home/inosuke/aiqyn/mobile/src/api/client.ts
echo "Updated client.ts: $WIN_IP"

cd /home/inosuke/aiqyn/mobile
REACT_NATIVE_PACKAGER_HOSTNAME=$WIN_IP npx expo start --clear
