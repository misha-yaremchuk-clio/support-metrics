#!/bin/bash
cd "$(dirname "$0")"
echo "Starting Dashboard Server at http://localhost:8000/dashboard.html"
python3 -m http.server 8000
