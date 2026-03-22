#Unbin v3.0
#by Jonathan Torres

import sys
import os
import binascii
import argparse
import subprocess

# Version and Metadata
VERSION = "3.0 (Python Refactor)"
LICENSE = """Unbin is free software distributed under the terms of the GNU General Public License, version 3,
or any later version published by the Free Software Foundation.
You have the freedom to use, study, modify, and redistribute this software.
Any derivative work must also be under GPLv3.
See /usr/share/Unbin/docs/gpl-3.0.txt for full details."""

# Core Logic Functions

def text_to_binary(text):
    return ' '.join(format(ord(c), '08b') for c in text)

def binary_to_text(binary):
    binary = binary.strip().replace(' ', '').replace('\n', '').replace('\r', '')
    if not binary: return ""
    try:
        # Handle cases where multiple bytes are present
        n = int(binary, 2)
        return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode('utf-8')
    except Exception as e:
        return f"Error: {e}"

def text_to_hex(text):
    h = binascii.hexlify(text.encode('utf-8')).decode('utf-8')
    return ' '.join(h[i:i+2] for i in range(0, len(h), 2))

def hex_to_text(hex_str):
    hex_str = hex_str.strip().replace(' ', '').replace('\n', '').replace('\r', '')
    if not hex_str: return ""
    try:
        return binascii.unhexlify(hex_str).decode('utf-8')
    except Exception as e:
        return f"Error: {e}"

def reverse_text(text):
    return text[::-1]

# File Operations (CLI)

def read_file_cli(path):
    try:
        if path.endswith(".gpg"):
             print(f"Decryption of {path} requires GUI or manual gpg command in CLI mode for now.")
             return None
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# GUI implementation

class UnbinGUI:
    def __init__(self, root, tk, messagebox, filedialog, simpledialog):
        self.root = root
        self.tk = tk
        self.messagebox = messagebox
        self.filedialog = filedialog
        self.simpledialog = simpledialog
        
        self.root.title(f"Unbin v{VERSION}")
        self.root.geometry("400x300")
        
        tk.Label(root, text="Choose encoding type:").pack(pady=10)
        
        self.mode = tk.StringVar(value="Binary")
        modes = ["Binary", "Hexadecimal", "Reverse"]
        for m in modes:
            tk.Radiobutton(root, text=m, variable=self.mode, value=m).pack()

        tk.Button(root, text="Process Text", command=self.process_text_dialog).pack(pady=10)
        tk.Button(root, text="Process File", command=self.process_file_dialog).pack(pady=5)
        tk.Button(root, text="License", command=lambda: messagebox.showinfo("License", LICENSE)).pack(pady=5)

    def process_text_dialog(self):
        msg = self.simpledialog.askstring("Input", f"Enter message to {self.mode.get()}:")
        if msg is None: return
        
        mode = self.mode.get()
        if mode == "Binary":
            action = self.messagebox.askquestion("Action", "Convert TO binary? (No = FROM binary)")
            res = text_to_binary(msg) if action == 'yes' else binary_to_text(msg)
        elif mode == "Hexadecimal":
            action = self.messagebox.askquestion("Action", "Convert TO hex? (No = FROM hex)")
            res = text_to_hex(msg) if action == 'yes' else hex_to_text(msg)
        else:
            res = reverse_text(msg)
            
        self.show_result(res)

    def process_file_dialog(self):
        path = self.filedialog.askopenfilename()
        if not path: return
        
        content = self.gui_read_file(path)
        if content is None: return
        
        mode = self.mode.get()
        if mode == "Binary":
            action = self.messagebox.askquestion("Action", "Convert TO binary? (No = FROM binary)")
            res = text_to_binary(content) if action == 'yes' else binary_to_text(content)
        elif mode == "Hexadecimal":
            action = self.messagebox.askquestion("Action", "Convert TO hex? (No = FROM hex)")
            res = text_to_hex(content) if action == 'yes' else hex_to_text(content)
        else:
            res = reverse_text(content)
            
        if self.messagebox.askyesno("Save", "Save result to file?"):
            save_path = self.filedialog.asksaveasfilename()
            if save_path:
                encrypt = self.messagebox.askyesno("Encrypt", "Encrypt with GPG?")
                self.gui_save_file(res, save_path, encrypt)
        else:
            self.show_result(res)

    def gui_read_file(self, path):
        try:
            if path.endswith(".gpg"):
                passphrase = self.simpledialog.askstring("GPG", "Enter passphrase:", show='*')
                if not passphrase: return None
                cmd = ["gpg", "--batch", "--passphrase", passphrase, "-d", path]
                res = subprocess.run(cmd, capture_output=True, text=True)
                if res.returncode != 0:
                    self.messagebox.showerror("Error", f"GPG Decryption failed: {res.stderr}")
                    return None
                return res.stdout
            else:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
        except Exception as e:
            self.messagebox.showerror("Error", f"Could not read file: {e}")
            return None

    def gui_save_file(self, content, path, encrypt=False):
        try:
            temp_path = path
            if encrypt:
                temp_path = path + ".tmp"
            
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            if encrypt:
                passphrase = self.simpledialog.askstring("GPG", "Enter new passphrase:", show='*')
                if not passphrase:
                    os.remove(temp_path)
                    return False
                cmd = ["gpg", "--batch", "--passphrase", passphrase, "-c", temp_path]
                res = subprocess.run(cmd, capture_output=True)
                os.remove(temp_path)
                if res.returncode != 0:
                    self.messagebox.showerror("Error", "GPG Encryption failed.")
                    return False
                final_path = temp_path + ".gpg"
                if os.path.exists(path + ".gpg"):
                     os.replace(final_path, path + ".gpg")
                else:
                     os.rename(final_path, path + ".gpg")
            return True
        except Exception as e:
            self.messagebox.showerror("Error", f"Could not save file: {e}")
            return False

    def show_result(self, result):
        top = self.tk.Toplevel(self.root)
        top.title("Result")
        text_widget = self.tk.Text(top, wrap='word')
        text_widget.insert('1.0', result)
        text_widget.pack(expand=True, fill='both')
        self.tk.Button(top, text="Close", command=top.destroy).pack()

# CLI Mode

def cli_mode(args):
    if args.l:
        print(LICENSE)
        return
    
    input_data = ""
    if args.f:
        input_data = read_file_cli(args.f)
        if input_data is None: return
    elif args.text:
        input_data = " ".join(args.text)
    else:
        # Interactive CLI
        print("Choose encoding: (b)in, (h)ex, (r)ev")
        choice = input("> ").strip().lower()
        if choice not in ['b', 'h', 'r']:
             print("Invalid choice")
             return
        print("Enter message:")
        input_data = input("> ")
        if choice == 'b': args.b = True
        elif choice == 'h': args.h = True
        elif choice == 'r': args.r = True

    result = ""
    if args.b: result = text_to_binary(input_data)
    elif args.bt: result = binary_to_text(input_data)
    elif args.h: result = text_to_hex(input_data)
    elif args.ht: result = hex_to_text(input_data)
    elif args.r or args.rt: result = reverse_text(input_data)
    
    print(result)

# Main

def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-b", action="store_true")
    parser.add_argument("-bt", action="store_true")
    parser.add_argument("-h", action="store_true")
    parser.add_argument("-ht", action="store_true")
    parser.add_argument("-r", action="store_true")
    parser.add_argument("-rt", action="store_true")
    parser.add_argument("-f", type=str)
    parser.add_argument("-l", action="store_true")
    parser.add_argument("-t", "--terminal", action="store_true")
    parser.add_argument("-nogui", action="store_true")
    parser.add_argument("-help", "--help", action="store_true")
    parser.add_argument("-moo", action="store_true")
    parser.add_argument("text", nargs='*', default=None)

    args, unknown = parser.parse_known_args()

    if args.help:
        print("Unbin v3.0 Usage:")
        print("  Unbin [-b|-bt|-h|-ht|-r|-rt] [-f file] [text]")
        print("  -t / -nogui : Terminal mode")
        print("  -l          : Show license")
        return

    if args.moo:
        print("There's no easter in these eggs... @~@")
        return

    use_terminal = args.terminal or args.nogui or args.b or args.bt or args.h or args.ht or args.r or args.rt or args.f or args.l or (args.text and len(args.text) > 0)

    if use_terminal:
        cli_mode(args)
    else:
        try:
            import tkinter as tk
            from tkinter import messagebox, filedialog, simpledialog
            root = tk.Tk()
            app = UnbinGUI(root, tk, messagebox, filedialog, simpledialog)
            root.mainloop()
        except ImportError:
            print("Tkinter not found. Falling back to terminal mode.")
            cli_mode(args)
        except Exception as e:
            print(f"Could not start GUI: {e}")
            print("Falling back to terminal mode.")
            cli_mode(args)

if __name__ == "__main__":
    main()
