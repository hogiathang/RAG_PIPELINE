#!/bin/bash

# RAG System - Run Main Application
set -e

echo "=============================="
echo " RAG Malware Analysis System"
echo "=============================="

# Chuyển về root của project
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

# Truyền tất cả arguments vào main
python -m src.main "$@"
