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
from src.ingestion.ingest_data import ingest_data
from src.retrieval.retrieval import retrieve_similar_documents

# Đảm bảo chạy được từ root: python -m src.main
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.generation.generation import build_prompt_from_retrieve_similar_documents, \
    build_prompt_from_retrive_similar_documents_for_skills_analysis, analyze_skills_file, analyze_package_codes, verify_result

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


def read_package_codes(package_path: str) -> list[str]:
    contents = []

    for root, _, files in os.walk(package_path):
        for file in files:
            if file.endswith((".js", ".json", ".md", ".sh", ".txt", ".yaml", ".yml", ".html", ".css", ".ts", ".tsx", ".jsx")):
                file_path = os.path.join(root, file)
                try:
                    content = Path(file_path).read_text(encoding="utf-8")
                    contents.append({
                        "file_path": file_path,
                        "content": content
                    })
                except Exception as e:
                    print(f"[WARNING] Could not read file '{file_path}': {e}")

def save_report(report: json, output_dir: str, package_name: str) -> None:
    output_path = os.path.join(output_dir, f"{package_name}_report.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    print(f"[INFO] Report saved to: {output_path}")
    print(SEPARATOR)
    

def retrieval_pipeline(input_dir: str, output_dir: str) -> None:
    if not os.path.exists(input_dir):
        print(f"[ERROR] Input directory '{input_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    for package in os.listdir(input_dir):
        print(f"\n[START] Analyzing package: {package}")
        package_path = os.path.join(input_dir, package)
        
        contents = read_package_codes(package_path)

        
        save_report(
            analyze_package_codes(contents, using_large_language_model=False), 
            output_dir, 
            package
        )


    
def ingest_data_pipeline():
    ingest_data()

if __name__ == "__main__":
    try:
        args = parse_args()
        print(BANNER)
    
        if args.ingest_data:
            ingest_data_pipeline()
        else:
            retrieval_pipeline(input_dir="data/test", output_dir="data/reports")
    
    except KeyboardInterrupt:
        print("\n[INFO] Process interrupted by user. Exiting gracefully.")
        sys.exit(0)