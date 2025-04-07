import json
import os
from datetime import datetime

def generate_report(usb_name, scanned_files, ai_results):
    report = {
        "scan_date": str(datetime.now()),
        "usb_name": usb_name,
        "total_files_scanned": len(scanned_files),
        "malicious_files": [file for file in ai_results if file.get("prediction") == "Malicious"],
        "safe_files": [file for file in ai_results if file.get("prediction") == "Safe"]
    }

    json_report_path = f"{usb_name}_scan_report.json"
    with open(json_report_path, "w", encoding="utf-8") as json_file:
        json.dump(report, json_file, indent=4)

    txt_report_path = f"{usb_name}_scan_report.txt"
    with open(txt_report_path, "w", encoding="utf-8") as txt_file:
        txt_file.write("USB Forensic Scan Report\n")
        txt_file.write(f"Scan Date: {report['scan_date']}\n")
        txt_file.write(f"USB Name: {usb_name}\n")
        txt_file.write(f"Total Files Scanned: {report['total_files_scanned']}\n\n")

        txt_file.write("Malicious Files Detected:\n")
        for file in report["malicious_files"]:
            txt_file.write(f"- {file.get('file_name', 'Unknown')}\n")

        txt_file.write("\nSafe Files:\n")
        for file in report["safe_files"]:
            txt_file.write(f"- {file.get('file_name', 'Unknown')}\n")

    print(f"[INFO] Report generated:\n- {json_report_path}\n- {txt_report_path}")

def extract_usb_name_from_file(file_name):
    return os.path.basename(file_name).split("_")[0] if "_" in file_name else "USB"

if __name__ == "__main__":
    try:
        print(f"[DEBUG] Current Working Directory: {os.getcwd()}")
        print(f"[DEBUG] Files in Directory: {os.listdir()}")

        scanned_file_json = next((f for f in os.listdir() if f.lower().endswith("_files.json")), None)
        if not scanned_file_json:
            raise FileNotFoundError("No *_files.json file found.")

        usb_name = extract_usb_name_from_file(scanned_file_json)
        with open(scanned_file_json, "r", encoding="utf-8") as f:
            scanned_files = json.load(f)

        ai_results_file = next((f for f in os.listdir() if f.lower() == "ai_scan_results.json"), None)
        if not ai_results_file:
            raise FileNotFoundError("'ai_scan_results.json' not found.")

        with open(ai_results_file, "r", encoding="utf-8") as f:
            ai_results = json.load(f)

        if scanned_files and ai_results:
            generate_report(usb_name, scanned_files, ai_results)
        else:
            print("[ERROR] Scan data or AI results missing. Report not generated.")

    except FileNotFoundError as fnf_error:
        print(f"[ERROR] {fnf_error}")
    except json.JSONDecodeError as json_error:
        print(f"[ERROR] JSON format error: {json_error}")
    except Exception as ex:
        print(f"[ERROR] Unexpected issue: {ex}")
