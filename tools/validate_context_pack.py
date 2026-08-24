from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]
required = [
    "AGENTS.md", "SPEC.md", "DESIGN.md", "DEV_LOG.md", "LEARNING.md",
    "docs/ARCHITECTURE.md", "docs/DECISIONS.md", "docs/AI_PLAN.md",
    "docs/AI_STATUS.md", "docs/ROADMAP.md", "docs/LEARNING_LOG.md",
    "docs/project-context.md", "prompts/README.md", "prompts/STAGES.md",
    "PACK_MANIFEST.json",
]
missing = [p for p in required if not (root/p).exists()]
if missing:
    raise SystemExit("Missing: " + ", ".join(missing))
json.loads((root/"PACK_MANIFEST.json").read_text(encoding="utf-8"))
print("Context pack OK")
