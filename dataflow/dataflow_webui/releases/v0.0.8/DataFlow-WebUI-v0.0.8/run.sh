#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

# 后端依赖
cd backend

uvicorn app.main:app --reload --port 8000  --reload-dir app --host=0.0.0.0
