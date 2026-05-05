#!/usr/bin/env bash
set -e

if [ ! -f .env ]; then
  echo "ERROR: .env file not found. Copy .env.example and fill in your credentials."
  exit 1
fi

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
