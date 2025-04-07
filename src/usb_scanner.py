import os
import json
import time
import psutil

def list_usb_files(drive_letter):
    """
    Lists all files on the specified USB drive and saves file details to a JSON file.
    """
    file_list = []
    for root, dirs, files in os.walk(drive_letter):
        for file in files:
            if file.startswith('.'):
                continue  # Skip hidden files
            file_path = os.path.join(root, file)
            try:
                file_info = {
                    "file_name": file,
                    "file_path": file_path,
                    "file_size": os.path.getsize(file_path),
                    "last_modified": time.ctime(os.path.getmtime(file_path))
                }
                file_list.append(file_info)
            except Exception as e:
                print(f"[WARNING] Skipping {file}: {e}")

    # Generate the JSON file name based on the USB drive letter
    usb_name = drive_letter.strip(":\\")
    output_file = f"{usb_name}_files.json"

    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(file_list, json_file, indent=4)

    print(f"[INFO] File details saved to {output_file}")
    return file_list

def get_removable_drive():
    """
    Detects and returns the first removable USB drive letter.
    """
    for part in psutil.disk_partitions():
        if 'removable' in part.opts.lower():
            drive_letter = part.device
            if os.path.exists(drive_letter):
                return drive_letter
    return None

def detect_usb_insertion():
    """
    Continuously checks for USB insertion and returns the drive letter once detected.
    """
    print("[INFO] Waiting for USB insertion...")
    usb_drive = get_removable_drive()
    while not usb_drive:
        time.sleep(2)
        usb_drive = get_removable_drive()

    print(f"[USB DETECTED] USB device found at: {usb_drive}")
    return usb_drive

if __name__ == "__main__":
    usb_drive = detect_usb_insertion()
    if usb_drive:
        list_usb_files(usb_drive)
