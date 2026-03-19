#!/bin/bash

# Script này dùng để xóa các file init của project python

SOURCE_DIR="src"
find "$SOURCE_DIR" -type f -name "*.pyc" -delete
find "$SOURCE_DIR" -type d -name "__pycache__" -exec rm -rf {} +
find "$SOURCE_DIR" -type f -name "__init__.py" -delete
echo "Đã xóa các file .pyc và thư mục __pycache__ trong $SOURCE_DIR"