import ast
from pathlib import Path


def test_core_does_not_import_adapters_or_ui() -> None:
    source_root = Path(__file__).parents[2] / "src" / "ai_mix_assistant" / "core"
    for path in source_root.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imported = [
            node.module or "" for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)
        ]
        assert all("adapters" not in module and ".ui" not in module for module in imported)
