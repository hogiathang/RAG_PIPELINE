"""Main entry point for the RAG skill-analysis pipeline."""

import argparse
import json
import os
import sys
from pathlib import Path

from src.ingestion.ingest_data import ingest_data

# Đảm bảo chạy được từ root: python -m src.main
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.generation.generation import run_map_reduce_extraction

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


ALLOWED_SOURCE_EXTENSIONS = (
    ".js",
    ".json",
    ".md",
    ".sh",
    ".txt",
    ".yaml",
    ".yml",
    ".html",
    ".css",
    ".ts",
    ".tsx",
    ".jsx",
    ".py",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        "prog=rag-malware-analyzer",
        description="RAG-based JavaScript / Node.js malware threat analysis",
    )

    input_group = parser.add_mutually_exclusive_group()

    input_group.add_argument(
        "--analyze-skills",
        action="store_true",
        help="Analyze agent's skills behavior",
    )

    input_group.add_argument(
        "--ingest-data",
        action="store_true",
        help="Ingest sample data into Qdrant (for testing purposes)",
    )

    return parser.parse_args()

def read_package_codes(package_path: str) -> list[dict[str, str]]:
    contents: list[dict[str, str]] = []

    for root, _, files in os.walk(package_path):
        for file in files:
            if file.endswith(ALLOWED_SOURCE_EXTENSIONS):
                file_path = os.path.join(root, file)
                try:
                    content = Path(file_path).read_text(encoding="utf-8")
                    contents.append({
                        "file_path": os.path.relpath(file_path, package_path),
                        "content": content
                    })
                except Exception as e:
                    print(f"[WARNING] Could not read file '{file_path}': {e}")

    return contents

def save_report(report: dict, output_dir: str, package_name: str) -> None:
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

    for package in sorted(os.listdir(input_dir)):
        print(f"\n[START] Analyzing package: {package}")
        package_path = os.path.join(input_dir, package)

        if not os.path.isdir(package_path):
            print(f"[INFO] Skipping non-directory entry: {package}")
            continue
        
        contents = read_package_codes(package_path)
        if not contents:
            print(f"[WARNING] No readable source files found in '{package_path}'.")
            continue

        extractor_result = run_map_reduce_extraction(
            package_path=package_path,
            files_data=contents,
            use_local_agent=False,
            max_workers=8,
        )

        save_report(extractor_result, output_dir=output_dir, package_name=package)

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