#!/bin/bash
#Unbin v3.0
#Jonathan Torres
#Licensed under GNU GPL v3.0 or later.
# Check for root privileges
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (sudo ./uninstall.sh)"
  exit 1
fi

echo "Uninstalling Unbin..."

# Remove installed files
rm -f /usr/bin/Unbin
rm -rf /usr/local/share/Unbin
rm -f /usr/share/pixmaps/Unbin.tga
rm -f /usr/share/man/man1/Unbin.1.gz
rm -f /usr/share/applications/Unbin.desktop

echo "Uninstallation complete."
