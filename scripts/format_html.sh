#!/bin/bash

find frontend/templates -name "*.html" -type f | while read -r file; do
    echo "Formatting $file"
    djhtml "$file"
done

python3 scripts/process_html.py
