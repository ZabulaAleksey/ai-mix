from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]
required = [
    "AGENTS.md","SPEC.md","ARCHITECTURE.md","DESIGN.md","PROGRESS.md",
    "DEV_LOG.md","LEARNING.md","docs/DECISIONS.md","prompts/README.md",
    "prompts/PROMPT_00_CONTEXT_AUDIT.md","PACK_MANIFEST.json"
]
missing = [p for p in required if not (root/p).exists()]
if missing:
    raise SystemExit("Missing: " + ", ".join(missing))
json.loads((root/"PACK_MANIFEST.json").read_text(encoding="utf-8"))
print("Context pack OK")
