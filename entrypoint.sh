#!/bin/bash
set -e

echo "Starting System 1 (internal A2A server)..."
uvicorn system1_manager.main:app --host 127.0.0.1 --port 8000 &
SYS1_PID=$!

echo "Starting System 2 (public REST /chat)..."
uvicorn system2_support.main:app --host 0.0.0.0 --port 8001 &
SYS2_PID=$!

echo "Starting System 3 (REST /supervise, not yet externally exposed)..."
uvicorn system3_supervisor.main:app --host 0.0.0.0 --port 8002 &
SYS3_PID=$!

# If ANY of the three dies, exit so Koyeb restarts the whole container
wait -n "$SYS1_PID" "$SYS2_PID" "$SYS3_PID"
exit $?