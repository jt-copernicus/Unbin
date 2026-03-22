# Unbin v3.0

Unbin is a simple tool to convert text to/from binary, hexadecimal, or to reverse strings. It features a Tkinter GUI and a full-featured CLI.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

## Features
- **Binary Conversion:** Convert text to 8-bit grouped binary and back.
- **Hexadecimal Conversion:** Convert text to 2-character grouped hex and back.
- **Reverse Text:** Quickly reverse strings.
- **GPG Support:** Encrypt and decrypt files during conversion (GUI only).
- **GUI & CLI:** Automatic fallback to CLI if a graphical environment is not available.

## Installation

### Dependencies
- Python 3
- Tkinter (`python3-tk`)
- GnuPG (`gnupg`)

### Install Script
To install Unbin on your system, run:
```bash
chmod +x install.sh
sudo ./install.sh
```

## Usage

### GUI
Simply launch `Unbin` from your application menu or type `Unbin` in the terminal without arguments.

### CLI
You can use flags for quick conversions:
- `Unbin -b "Message"` - Convert to Binary
- `Unbin -bt "01001000 01100101"` - Convert from Binary to Text
- `Unbin -h "Message"` - Convert to Hexadecimal
- `Unbin -ht "48 65"` - Convert from Hex to Text
- `Unbin -r "Message"` - Reverse string
- `Unbin -t` - Force interactive terminal mode

For more options, see `man Unbin`.

## Uninstallation
To remove Unbin from your system, run:
```bash
chmod +x uninstall.sh
sudo ./uninstall.sh
```

## License
Licensed under GNU GPL v3.0 or later.

