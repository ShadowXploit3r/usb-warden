import os
import json
import joblib
import pandas as pd
import sys

# Ensure proper output encoding
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# Load the trained AI model
try:
    model = joblib.load("ai_usb_malware_model.pkl")
except FileNotFoundError:
    print("[ERROR] AI model file 'ai_usb_malware_model.pkl' not found.")
    sys.exit(1)

# Feature extraction from a file
def extract_features(file_path):
    size = os.path.getsize(file_path)
    name = os.path.basename(file_path).lower()
    suspicious_keywords = ['hack', 'exploit', 'keylog', 'rat', 'malware']
    has_suspicious = any(keyword in name for keyword in suspicious_keywords)
    entropy = round(size % 100 / 12.5 + 3.5, 2)  # Placeholder entropy

    return {
        "file_size": size,
        "entropy": entropy,
        "suspicious_strings": int(has_suspicious)
    }

# Scan files in a directory
def scan_files_in_directory(directory):
    results = []
    output_file = "ai_scan_results.json"

    print(f"\n[INFO] Scanning directory: {directory}\n")

    for root, dirs, files in os.walk(directory):
        for file in files:
            try:
                file_path = os.path.join(root, file)
                features = extract_features(file_path)
                df_features = pd.DataFrame([features])
                prediction = model.predict(df_features)[0]

                result = {
                    "file_name": file,
                    "file_path": file_path,
                    "prediction": "Malicious" if prediction == 1 else "Safe"
                }
                results.append(result)
                print(f"[SCANNED] {file}: {result['prediction']}")
            except Exception as e:
                print(f"[WARNING] Skipping {file}: {e}")

    # Save results to JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print(f"\n[INFO] Scan complete. Results saved to {output_file}")

# Auto-set USB path (E:\) if no input
if __name__ == "__main__":
    default_path = "E:\\"
    folder_to_scan = input(f"Enter folder path to scan [default: {default_path}]: ").strip() or default_path

    if os.path.isdir(folder_to_scan):
        scan_files_in_directory(folder_to_scan)
    else:
        print("[ERROR] Invalid folder path.")
