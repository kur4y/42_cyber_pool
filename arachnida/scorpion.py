import os
import time
import argparse
import exifread


# ansi colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
ORANGE = "\033[38;5;208m"
RESET = "\033[0m"

EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

def get_file_info(file_path):
    try:
        stats = os.stat(file_path)

        print(f"{YELLOW}--- System infos ---{RESET}")
        print(f"{CYAN}[INFO] Name:{RESET} {os.path.basename(file_path)}")
        print(f"{CYAN}[INFO] Size:{RESET} {stats.st_size} bytes")

        # Convert timestamp (float) to readable date
        creation_time = time.ctime(stats.st_ctime)
        modif_time = time.ctime(stats.st_mtime)
        print(f"{CYAN}[INFO] Creation:{RESET} {creation_time}")
        print(f"{CYAN}[INFO] Modification time:{RESET} {modif_time}")
        print(f"{CYAN}[INFO] Permissions:{RESET} {oct(stats.st_mode)[-3:]}")

    except Exception as e:
        print(f"{RED}[CRITICAL] Error while reading file:{RESET} {e}")

def get_exif_data(file_path):
    # Extract hidden metadata (EXIF) from the image
    print(f"{YELLOW}--- EXIF Datas ---{RESET}")

    try:
        with open(file_path, 'rb') as f:
            tags = exifread.process_file(f)
            if not tags:
                print(f"{RED}[ERROR] No EXIF data found (image cleaned or unsupported format).{RESET}")
                return
            for tag in tags.keys():
                # data filtrer
                if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                    print(f"{CYAN}{tag}:{RESET} {tags[tag]}")
    
    except Exception as e:
        print(f"{RED}[CRITICAL] Error reading EXIF:{RESET} {e}")

def main():
    parser = argparse.ArgumentParser(description = "Scorpion: metadata analyzer.")

    # one argument required, multiple allowed
    parser.add_argument("files", nargs = '+', help = "[i] List of images to analyze")

    args = parser.parse_args()

    for file_path in args.files:
        print("\n" + "=" * 40)
        print(f"{GREEN}[INFO] Analyzing:{RESET} {file_path}")
        print("=" * 40)

        if os.path.isfile(file_path):
            if file_path.lower().endswith(EXTENSIONS):
                print("")
                get_file_info(file_path)
                print("")
                get_exif_data(file_path)

            else:
                print(f"{RED}[ERROR] Unsupported extension.{RESET}")

        else:
            print(f"{RED}[ERROR] File not found.{RESET}")

if __name__ == "__main__":
    main()
