#!/bin/bash
set -e

echo "Starting System 1 (internal A2A server)..."
uvicorn system1_manager.main:app --host 127.0.0.1 --port 8000 &
SYS1_PID=$!

PUBLIC_PORT="${PORT:-8001}"
echo "Starting System 2 (public REST /chat) on port $PUBLIC_PORT..."
uvicorn system2_support.main:app --host 0.0.0.0 --port "$PUBLIC_PORT" &
SYS2_PID=$!

echo "Starting System 3 (REST /supervise, not yet externally exposed)..."
uvicorn system3_supervisor.main:app --host 0.0.0.0 --port 8002 &
SYS3_PID=$!

wait -n "$SYS1_PID" "$SYS2_PID" "$SYS3_PID"
exit $?