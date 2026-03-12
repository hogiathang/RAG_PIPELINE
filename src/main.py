"""
Main entry point cho RAG System
──────────────────────────────────────────
Pipeline:
  1. Nhận code snippet từ user (stdin, CLI arg, hoặc file)
  2. Embed code → tìm kiếm tài liệu tương tự trong Qdrant + web search
  3. Tổng hợp ngữ cảnh → Gemini sinh báo cáo Threat Intelligence
  4. In báo cáo markdown ra stdout
"""

import sys, os, json
import argparse
from pathlib import Path

# Đảm bảo chạy được từ root: python -m src.main
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.generation.generation import build_prompt_from_retrieve_similar_documents, build_prompt_from_retrive_similar_documents_for_skills_analysis

BANNER = r"""
╔══════════════════════════════════════════════════════╗
║          RAG-based Malware Analysis System           ║
║      JavaScript / Node.js Threat Intelligence        ║
╚══════════════════════════════════════════════════════╝

Default: Retrieval Mode.
To Switch to ingest-data mode, use the --ingest-data flag.

User Guide:
    + Arguments:
        --ingest-data        Ingest sample data into Qdrant (for testing purposes)
        --analyze-skills       Analyze agent's skills behavior
"""

SEPARATOR = "=" * 60


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        "prog=rag-malware-analyzer",
        description="RAG-based JavaScript / Node.js malware threat analysis",
    )

    input_group = parser.add_mutually_exclusive_group()


    input_group.add_argument(
        "--analyze-skills",
        action="store_true",
        help="Analyze agent's skills behavior"
    )

    input_group.add_argument(
        "--ingest-data",
        action="store_true",
        help="Ingest sample data into Qdrant (for testing purposes)"
    )

    return parser.parse_args()


def run_pipeline(code: str, is_analyzing_skills: bool = True) -> json:
    """
    Thực thi toàn bộ RAG pipeline:
      Retrieve (Qdrant + Web Search) → Generate (Gemini)
    Trả về báo cáo dạng Markdown string.

    """

    print("[STEP 1/2] Run RAG Pipeline...")

    report = build_prompt_from_retrieve_similar_documents(code) if \
        not is_analyzing_skills else build_prompt_from_retrive_similar_documents_for_skills_analysis(code)

    if report is None:
        print("[ERROR] Pipeline returned no result. Check your API tokens and services.", file=sys.stderr)
        sys.exit(1)

    print("[STEP 2/2] Report generation complete.\n")
    return report

def save_report(report: str, output_path: str) -> None:
    """Lưu báo cáo ra file markdown."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report, encoding="utf-8")
    print(f"[INFO] Report saved to: {path.resolve()}")


def read_package(package_path: str) -> str:
    contents = []
    for file in os.listdir(package_path):
        # Chỉ đọc file .js, .json, .md, .sh,

        if not file.endswith((".js", ".json", ".md", ".sh", ".txt", ".yaml", ".yml", ".html", ".css", ".ts", ".tsx", ".jsx")):
            continue

        content = Path(os.path.join(package_path, file)).read_text(encoding="utf-8")
        contents.append(f"[FILE: {file}]\n{content}")

    return contents

def retrieval_pipeline(args) -> None:

    INPUT_DIR = input("Please enter the input directory path (containing JavaScript/Node.js packages): ").strip()
    OUTPUT_DIR = input("Please enter the output directory path (to save markdown reports): ").strip()

    if not os.path.exists(INPUT_DIR):
        print(f"[ERROR] Input directory '{INPUT_DIR}' does not exist.", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    analyzed_packages = []
    for file in os.listdir(OUTPUT_DIR):
        if file.endswith("_report.md"):
            analyzed_packages.append(file.replace("_report.md", ""))

    for package in os.listdir(INPUT_DIR):

        if package in analyzed_packages:
            print(f"[SKIP] Package '{package}' already analyzed. Skipping...")
            continue

        package_path = os.path.join(INPUT_DIR, package)

        contents =  read_package(package_path)

        report = run_pipeline("\n\n".join(contents), is_analyzing_skills=args.analyze_skills)

        output_path = os.path.join(OUTPUT_DIR, f"{package}_report.json")
        save_report(report, output_path)

    
def ingest_data_pipeline():
    pass

if __name__ == "__main__":
    args = parse_args()
    print(BANNER)
    
    if args.ingest_data:
        ingest_data_pipeline()
    else:
        if args.analyze_skills:
            print("[INFO] Running in Skills Analysis Mode...")
        else:
            print("[INFO] Running in Retrieval Mode...")

        retrieval_pipeline(args)