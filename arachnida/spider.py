import os
import sys
import shutil
import requests
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


# ansi colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
ORANGE = "\033[38;5;208m"
RESET = "\033[0m"

EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

def parse_arguments():
    # setup argument parser following required format: ./spider [-rlp] URL
    parser = argparse.ArgumentParser(description="Spider: 42 web image scraper")
    parser.add_argument("-r", "--recursive", action="store_true", help="Enable recursive mode")
    parser.add_argument("-l", "--level", type=int, default=5, help="Recursion depth (default: 5)")
    parser.add_argument("-p", "--path", default="./data/", help="Save path (default: ./data/)")
    parser.add_argument("url", help="target URL")

    args = parser.parse_args()
    if args.level != 5 and not args.recursive:
        parser.error("The -l option requires the -r option.")

    return args

def download_image(img_url, folder_path, download_count):
    try:
        # parse URL to separate path from query parameters (e.g., ?v=1.2)
        parsed_url = urlparse(img_url)
        clean_path = parsed_url.path.lower()

        # validate extension against the clean path
        if not clean_path.endswith(EXTENSIONS):
            return

        # extract the filename from the clean path
        filename = os.path.basename(parsed_url.path)
        if not filename:
            return

        file_path = os.path.join(folder_path, filename)
        response = requests.get(img_url, stream=True, timeout=5)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                response.raw.decode_content = True
                # optimized downloading: streams data to disk
                shutil.copyfileobj(response.raw, f)

            download_count['count'] += 1
            print(f"{GREEN}[INFO] ({download_count['count']}) Image downloaded:{RESET} {filename}")

        else:
            print(f"{RED}[ERROR] HTTP Error {response.status_code}:{RESET} {img_url}")

    except requests.exceptions.RequestException as e:
        print(f"{RED}[ERROR] Network error on {img_url}:{RESET} {e}")
    except Exception as e:
        print(f"{RED}[ERROR] Error on {img_url}:{RESET} {e}")

def crawl(url, folder, max_depth, current_depth=0, visited=None, download_count=None):
    if visited is None:
        visited = set()

    if download_count is None:
        download_count = {'count': 0}

    if current_depth > max_depth:
        return
    
    if url in visited:
        return

    # normalize URL: remove fragments (e.g., #section) to avoid duplicate visits
    parsed_current = urlparse(url)
    clean_url = parsed_current._replace(fragment="").geturl()

    if clean_url in visited:
        return
    
    visited.add(clean_url)

    # visual indentation based on depth
    indent = "  " * current_depth
    print(f"{indent}{CYAN}[INFO] (Level {current_depth}) Analysing:{RESET} {clean_url}")

    try:
        response = requests.get(clean_url, timeout=5)
        if response.status_code != 200:
            print(f"{indent}{RED}[ERROR] Cannot access page (HTTP {response.status_code}):{RESET} {clean_url}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img')

        if images:
            print(f"{indent}{CYAN}[INFO] {len(images)} potential image(s) found...{RESET}")
            for img in images:
                src = img.get('src')
                if src:
                    absolute_url = urljoin(clean_url, src)
                    download_image(absolute_url, folder, download_count)
        else:
            print(f"{indent}{ORANGE}[INFO] No images found on this page.{RESET}")

        # recursivity
        if current_depth < max_depth:
            links = soup.find_all('a')
            for link in links:
                href = link.get('href')
                if href:
                    next_url = urljoin(clean_url, href)
                    parsed_next = urlparse(next_url)

                    # filter out non-HTTP schemes (mailto, javascript, etc.)
                    if parsed_next.scheme not in ['http', 'https']:
                        continue

                    # prevent leaving the base domain
                    if parsed_next.netloc == parsed_current.netloc:
                        # incrementing depth (level)
                        crawl(next_url, folder, max_depth, current_depth + 1, visited, download_count)

    except requests.exceptions.RequestException as e:
        print(f"{indent}{RED}[ERROR] Connection error:{RESET} {e}")
    except Exception as e:
        print(f"{RED}[CRITICAL] Error:{RESET} {e}")

    return download_count

def main():
    args = parse_arguments()

    if not os.path.exists(args.path):
        try:
            os.makedirs(args.path)
            print(f"{GREEN}[INFO] Directory created: {args.path}{RESET}")

        except OSError as e:
            print(f"{RED}[CRITICAL] Error creating Directory: {e}{RESET}")
            sys.exit(1)

    print(f"{CYAN}[INFO] Starting Spider on: {RESET}{args.url}")
    print(f"{CYAN}[INFO] Saves in: {RESET}{args.path}")

    final_dl_image = {'count': 0}

    if args.recursive:
        print(f"{YELLOW}[INFO] Recursive mode enabled (Level {args.level}){RESET}")
        crawl(args.url, args.path, args.level, download_count=final_dl_image)
    else:
        print(f"{YELLOW}[INFO] Simple mode (Level 0){RESET}")
        crawl(args.url, args.path, 0, download_count=final_dl_image)

if __name__ == "__main__":
    main()


