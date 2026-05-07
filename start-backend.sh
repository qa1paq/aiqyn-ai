#!/bin/bash
cd /home/inosuke/aiqyn/backend
source venv/bin/activate
echo "Starting AIQYN AI Backend..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
