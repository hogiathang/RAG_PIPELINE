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
from src.logging.log_manager import AppLogger

# Đảm bảo chạy được từ root: python -m src.main
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

logger = AppLogger.get_logger(__name__)

from src.generation.generation import generate_report_from_skill_package

SUPPORTED_FILE_TYPES = (".js", ".json", ".md", ".sh", ".txt", ".yaml", ".yml", ".html", ".css", ".ts", ".tsx", ".jsx")

BANNER = r"""
╔══════════════════════════════════════════════════════╗
║          RAG-based Malware Analysis System           ║
║           Agent Skills Threat Intelligence           ║
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
        description="RAG-based Malware Analysis System with Agent Skills Threat Intelligence",
        formatter_class=argparse.RawTextHelpFormatter
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
    Running the RAG pipeline
    """
    logger.info(f"{SEPARATOR}\n[STEP 1/2] Starting RAG Pipeline...\n{SEPARATOR}")
    report = generate_report_from_skill_package(code)

    if report is None:
        logger.error("Failed to generate report.")
        return None

    logger.info(f"{SEPARATOR}\n[STEP 2/2] RAG Pipeline Completed.\n{SEPARATOR}")
    return report

def read_package(package_path: str) -> str:
    contents = []
    for file in os.listdir(package_path):

        if not file.endswith(SUPPORTED_FILE_TYPES):
            continue

        content = Path(os.path.join(package_path, file)).read_text(encoding="utf-8")
        contents.append(f"[FILE: {file}]\n{content}")

    return 
    
def parse_directory():
    input_dir  = input("Please enter the input directory path (containing JavaScript/Node.js packages): ").strip()
    output_dir = input("Please enter the output directory path (to save markdown reports): ").strip()

    if not os.path.exists(input_dir):
        logger.error(f"Input directory '{input_dir}' does not exist. Please provide a valid path.")
        sys.exit(1)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    return input_dir, output_dir

def get_analyzed_packages(output_dir: str) -> list:
    analyzed_packages = []
    for file in os.listdir(output_dir):
        if file.endswith("_report.json"):
            analyzed_packages.append(file.replace("_report.json", ""))
    return analyzed_packages

def save_report(report: json, output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)


def retrieval_pipeline(args) -> None:
    input_dir, output_dir = parse_directory()

    analyzed_packages = get_analyzed_packages(output_dir)
    logger.info(f"Found {len(analyzed_packages)} already analyzed packages. They will be skipped in this run.")

    for package in os.listdir(input_dir):

        if package in analyzed_packages:
            logger.info(f"Package '{package}' already analyzed. Skipping...")
            continue

        package_path = os.path.join(input_dir, package)
        contents =  read_package(package_path)
        
        report = run_pipeline(f"PACKAGE NAME: {package}\n\n" + "\n\n".join(contents), is_analyzing_skills=args.analyze_skills)
        output_path = os.path.join(output_dir, f"{package}_report.json")

        save_report(report, output_path)

        logger.info(f"Report for package '{package}' saved to: {output_path}")


if __name__ == "__main__":
    try:
        args = parse_args()
        logger.info(BANNER)
    
        if args.ingest_data:
            ingest_data()
        
        else:
            logger.info("Running in Retrieval Mode...")
            retrieval_pipeline(args)
    
    except KeyboardInterrupt:
        logger.warning("Process interrupted by user. Exiting...")
        sys.exit(0)