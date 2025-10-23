import hashlib
import os

def hash_file(filepath):
    """Return the SHA256 hash of the file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        # Read the file in small chunks to handle large files
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def save_baseline(directory):
    """Generate hashes for all files in a directory and save to baseline.txt"""
    with open("baseline.txt", "w") as baseline:
        for root, _, files in os.walk(directory):
            for file in files:
                path = os.path.join(root, file)
                file_hash = hash_file(path)
                baseline.write(f"{path}|{file_hash}\n")
    print("✅ Baseline created successfully (baseline.txt)")

def check_integrity(directory):
    """Compare current file hashes with the baseline"""
    if not os.path.exists("baseline.txt"):
        print("❌ No baseline found. Run 'save_baseline' first.")
        return

    with open("baseline.txt", "r") as baseline:
        baseline_data = dict(line.strip().split("|") for line in baseline)

    print("🔍 Checking file integrity...\n")
    for root, _, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            current_hash = hash_file(path)

            if path not in baseline_data:
                print(f"⚠️ New file detected: {path}")
            elif baseline_data[path] != current_hash:
                print(f"🚨 File changed: {path}")
            else:
                print(f"✅ File unchanged: {path}")

def main():
    print("=== File Integrity Checker ===")
    print("1️⃣ Create baseline (first-time setup)")
    print("2️⃣ Check integrity against baseline")
    choice = input("Choose (1 or 2): ")

    directory = input("Enter folder path to scan: ").strip()

    if choice == "1":
        save_baseline(directory)
    elif choice == "2":
        check_integrity(directory)
    else:
        print("Invalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    main()
