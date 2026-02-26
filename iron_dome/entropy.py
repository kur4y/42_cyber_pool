import os
import math
from collections import Counter


# ansi colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
ORANGE = "\033[38;5;208m"
RESET = "\033[0m"

# compute the shannon entropy of a file (0.0 to 8.0)
def calculate_entropy(file_path):
    try:
        # reading in binary mode
        with open(file_path, "rb") as f:
            byte_arr = f.read()
        
        file_size = len(byte_arr)
        if file_size == 0:
            return 0.0

        entropy = 0.0

        # counting the frequency of each byte (0-255)
        freqs = Counter(byte_arr)

        # shannon formula
        for count in freqs.values():
            probability = count / file_size
            entropy -= probability * math.log2(probability)

        return entropy
    
    except Exception as e:
        print(f"{RED}[CRITICAL] Error reading on {file_path}: {RESET}{e}")
        return 0.0

if __name__ == "__main__":
    normal_file = "test.txt.ft"
    score_normal = calculate_entropy(normal_file)
    print(f"{CYAN}[INFO] Entropy of a clean file ({normal_file}): {RESET}{score_normal:.2f}/8.0")
