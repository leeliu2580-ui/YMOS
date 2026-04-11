#!/usr/bin/env python3
import subprocess, sys, json

result = subprocess.run(
    ["C:\\Python311\\python.exe", "skills/grok-search/scripts/grok_search.py",
     "--mode", "research",
     "--query", "CoreWeave IPO filing 2026 NVIDIA H100 Blackwell contracts revenue investors"],
    capture_output=True, text=True,
    cwd="D:\\0_workspace\\trae_2601\\ymos\\YMOS"
)
print("STDOUT:", result.stdout[:10000])
print("STDERR:", result.stderr[:3000])
print("RC:", result.returncode)
