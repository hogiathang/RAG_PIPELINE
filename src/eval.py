import os, re
from src.logging.log_manager import AppLogger

all_files = 0
malware_file = 0

logger = AppLogger.get_logger(__name__)

def is_malware(file_path:str) -> bool:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

        match = re.search(r"\s*(BENIGN|MALICIOUS)\s*", content, re.IGNORECASE)

        if match:
            classification = match.group(1).upper()
            return classification == "MALICIOUS"
        else:
            logger.warning(f"Could not find classification in file: {file_path}")
            return False

for file in os.listdir("./data/skills/outputs"):
    all_files += 1
    if file.endswith(".md"):
        if is_malware(os.path.join("./data/skills/outputs", file)):
            malware_file += 1

logger.info(f"Total files: {all_files}")
logger.info(f"Malware files: {malware_file}")
logger.info(f"Malware detection rate: {malware_file / all_files * 100:.2f}%")