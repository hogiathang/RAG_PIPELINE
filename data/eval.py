import os
import json
import shutil


def ensure_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def has_error_result(content: dict) -> bool:
    """
    Check if SARIF file contains any result with level == 'error'
    """
    runs = content.get("runs", [])
    if not runs:
        return False

    results = runs[0].get("results", [])
    return any(r.get("level") == "error" for r in results)


# Ensure output folders exist
ensure_dir("./fp")
ensure_dir("./fn")


# Confusion matrix counters
false_pst = 0  # FP
true_pst = 0   # TP
false_ngt = 0  # FN
true_ngt = 0   # TN

benign_count = 0
malware_count = 0


# =========================
# Process BENIGN files
# =========================

for file in os.listdir("./benign"):

    path = os.path.join("./benign", file)

    if not os.path.isfile(path):
        continue

    benign_count += 1

    with open(path, "r", encoding="utf-8") as f:
        content = json.load(f)

    has_error = has_error_result(content)

    if has_error:
        print(f"[FP] Benign file flagged as malicious: {file}")
        false_pst += 1

        shutil.copy2(path, os.path.join("./fp", file))
    else:
        true_ngt += 1


# =========================
# Process MALWARE files
# =========================

for file in os.listdir("./malware"):

    path = os.path.join("./malware", file)

    if not os.path.isfile(path):
        continue

    malware_count += 1

    with open(path, "r", encoding="utf-8") as f:
        content = json.load(f)

    has_error = has_error_result(content)

    if has_error:
        true_pst += 1
    else:
        print(f"[FN] Malware file NOT detected: {file}")
        false_ngt += 1

        shutil.copy2(path, os.path.join("./fn", file))


# =========================
# Metrics calculation
# =========================

TP = true_pst
TN = true_ngt
FP = false_pst
FN = false_ngt

total = TP + TN + FP + FN


def safe_div(a, b):
    return a / b if b != 0 else 0


TPR = safe_div(TP, TP + FN)   # Recall / Sensitivity
FNR = safe_div(FN, TP + FN)

FPR = safe_div(FP, FP + TN)
TNR = safe_div(TN, FP + TN)   # Specificity

precision = safe_div(TP, TP + FP)
recall = TPR

accuracy = safe_div(TP + TN, total)

f1_score = safe_div(2 * TP, (2 * TP + FP + FN))


# =========================
# Print results
# =========================

print("\n========== DATASET ==========")
print(f"Total benign files: {benign_count}")
print(f"Total malicious files: {malware_count}")
print(f"Total samples: {total}")

print("\n========== CONFUSION MATRIX ==========")
print(f"TP (Malware detected): {TP}")
print(f"TN (Benign correct): {TN}")
print(f"FP (Benign flagged malware): {FP}")
print(f"FN (Missed malware): {FN}")

print("\n========== METRICS ==========")
print(f"True Positive Rate (Recall): {TPR:.2%}")
print(f"False Negative Rate: {FNR:.2%}")

print(f"False Positive Rate: {FPR:.2%}")
print(f"True Negative Rate: {TNR:.2%}")

print(f"Precision: {precision:.2%}")
print(f"Accuracy: {accuracy:.2%}")
print(f"F1 Score: {f1_score:.2%}")