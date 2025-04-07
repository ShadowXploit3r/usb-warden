import sys
import os
def display_logo():
    logo = r"""
 _     ____  ____    _      ____  ____  ____  _____ _     
/ \ /\/ ___\/  __\  / \  /|/  _ \/  __\/  _ \/  __// \  /|
| | |||    \| | //  | |  ||| / \||  \/|| | \||  \  | |\ ||
| \_/|\___ || |_\\  | |/\||| |-|||    /| |_/||  /_ | | \||
\____/\____/\____/  \_/  \|\_/ \|\_/\_\\____/\____\\_/  \|
"""
    print(logo)

# Add 'src' directory to system path so Python can find the modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from usb_scanner import detect_usb_insertion, list_usb_files
from check_file import scan_files_in_directory
from generate_report import generate_report

import json

if __name__ == "__main__":
    if __name__ == "__main__":
        display_logo()
        main()  # or whatever function you're using to run the tool

    print("[INFO] Starting USB Malware Detection Tool")

    # Step 1: Detect and scan USB
    usb_path = detect_usb_insertion()
    scanned_files = list_usb_files(usb_path)

    # Step 2: Run AI model on files
    scan_files_in_directory(usb_path)

    # Step 3: Load AI results
    try:
        with open("ai_scan_results.json", "r", encoding="utf-8") as f:
            ai_results = json.load(f)

        if scanned_files and ai_results:
            usb_name = os.path.basename(usb_path.strip("\\/"))
            generate_report(usb_name, scanned_files, ai_results)
        else:
            print("[ERROR] Scan data or AI results missing.")
    except Exception as e:
        print(f"[ERROR] Failed to load scan results: {e}")
