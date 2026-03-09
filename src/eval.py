import os, re

all_files = 0
malware_file = 0


def is_malware(file_path:str) -> bool:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

        match = re.search(r"\s*(BENIGN|MALICIOUS)\s*", content, re.IGNORECASE)

        if match:
            classification = match.group(1).upper()
            return classification == "MALICIOUS"
        else:
            print(f"[WARNING] No classification found in {file_path}. Skipping.")
            return False

for file in os.listdir("./data/skills/outputs"):
    all_files += 1
    if file.endswith(".md"):
        if is_malware(os.path.join("./data/skills/outputs", file)):
            malware_file += 1

print(f"Total files: {all_files}")
print(f"Malware files: {malware_file}")
print(f"Malware percentage: {malware_file / all_files * 100:.2f}%")