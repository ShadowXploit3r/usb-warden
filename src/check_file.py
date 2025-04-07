import os
import json
import joblib
import pandas as pd
import numpy as np
import sys

# Optional: for Windows console UTF-8 compatibility
try:
    sys.stdout.reconfigure(encoding='utf-8')
except:
    pass

# Load the trained model
try:
    model = joblib.load("ai_usb_malware_model.pkl")
except FileNotFoundError:
    print("[ERROR] AI model file 'ai_usb_malware_model.pkl' not found.")
    sys.exit(1)

# Correct feature extraction for model input
def extract_features(file_path):
    size = os.path.getsize(file_path)

    # Mock entropy: simulate randomness based on file size
    entropy = 3 + 5 * np.random.rand()

    # Mock suspicious string detection
    suspicious_keywords = ["virus", "malware", "keylogger", "trojan", "hack"]
    with open(file_path, "rb") as f:
        try:
            content = f.read(1024).decode(errors="ignore").lower()
        except:
            content = ""
    suspicious = int(any(word in content for word in suspicious_keywords))

    return {
        "file_size": size,
        "entropy": entropy,
        "suspicious_strings": suspicious
    }

# Scan all files in the directory
def scan_files_in_directory(directory):
    results = []
    output_file = "ai_scan_results.json"

    print(f"\n[INFO] Scanning files in: {directory}\n")

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
                    "file_size": features["file_size"],
                    "prediction": "Malicious" if prediction == 1 else "Safe"
                }
                results.append(result)
                print(f"[SCANNED] {file} — {result['prediction']}")
            except Exception as e:
                print(f"[WARNING] Skipping {file}: {e}")

    # Save results
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print(f"\n✅ AI Scan Complete! Results saved to {output_file}")

# Main
if __name__ == "__main__":
    folder_to_scan = "E:\\"  # Set your USB drive path
    if os.path.isdir(folder_to_scan):
        scan_files_in_directory(folder_to_scan)
    else:
        print(f"[ERROR] USB drive path not found: {folder_to_scan}")
