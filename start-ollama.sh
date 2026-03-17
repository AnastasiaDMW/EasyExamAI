#!/bin/bash

echo "[OLLAMA] Starting server..."
ollama serve & 

while ! curl -s http://localhost:11434/v1/models > /dev/null 2>&1; do
  echo "[OLLAMA] Waiting for server..."
  sleep 1
done

echo "[OLLAMA] Server is running."

if ! ollama list | grep -q "mistral"; then
  echo "[OLLAMA] Pulling mistral model..."
  ollama pull mistral
fi

wait