#!/bin/bash
#Unbin v3.0
#Jonathan Torres
#Licensed under GNU GPL v3.0 or later.

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check for root privileges
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (sudo ./install.sh)"
  exit 1
fi

echo "Installing Unbin v3.0..."

# Install dependencies if possible
if command -v apt-get >/dev/null; then
    apt-get update
    apt-get install -y python3 python3-tk gnupg
elif command -v dnf >/dev/null; then
    dnf install -y python3 python3-tkinter gnupg
elif command -v pacman >/dev/null; then
    pacman -S --noconfirm python tk gnupg
fi

# Create directories
mkdir -p /usr/local/share/Unbin/docs
mkdir -p /usr/share/pixmaps
mkdir -p /usr/share/man/man1
mkdir -p /usr/share/applications

# Copy files from the script's directory
echo "Copying files..."
cp "$SCRIPT_DIR/Unbin.py" /usr/local/share/Unbin/
chmod +x /usr/local/share/Unbin/Unbin.py

# Copy docs if they exist
if [ -d "$SCRIPT_DIR/docs" ]; then
    cp "$SCRIPT_DIR/docs/"* /usr/local/share/Unbin/docs/ 2>/dev/null || true
elif [ -f "$SCRIPT_DIR/gpl-3.0.txt" ]; then
    cp "$SCRIPT_DIR/gpl-3.0.txt" /usr/local/share/Unbin/docs/
fi

cp "$SCRIPT_DIR/Unbin.tga" /usr/share/pixmaps/ 2>/dev/null || echo "Warning: Unbin.tga not found"
cp "$SCRIPT_DIR/Unbin.1" /usr/share/man/man1/ 2>/dev/null || echo "Warning: Unbin.1 not found"
cp "$SCRIPT_DIR/Unbin.desktop" /usr/share/applications/ 2>/dev/null || echo "Warning: Unbin.desktop not found"

# Create launcher script
echo "Creating launcher..."
cat <<'EOF' > /usr/bin/Unbin
#!/bin/bash
python3 /usr/local/share/Unbin/Unbin.py "$@"
EOF
chmod +x /usr/bin/Unbin

# Compress man page if it's there
if [ -f /usr/share/man/man1/Unbin.1 ]; then
    gzip -f /usr/share/man/man1/Unbin.1
fi

echo "Installation complete! You can now run 'Unbin' from the terminal or your application menu."
