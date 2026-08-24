# Статус AI

## Governance migration — 2026-08-24

- Репозиторий находится в `~/codex-workspace/ai-mix`; подробные legacy prompts объединены в `prompts/STAGES.md`.
- `python tools/validate_context_pack.py` и глобальный project overlay validator — PASS.
- Продуктовый код и tests не изменялись; push/merge не выполнялись.

- Состояние: overlay консолидирован; продуктовый код не изменён.
- Ветка: `chore/full-governance-migration`.
- Проверки: `python tools/validate_context_pack.py` и проектные pytest-наборы.
- Риск: optional ML/GPU и GUI не являются подтверждёнными требованиями без отдельного решения.

## Product baseline — stage 01

- Context overlay stage 00 is preserved and passes `python tools/validate_context_pack.py`.
- Stage 01 is implemented, validated, committed, and locally fast-forwarded into `main`.
- Delivered baseline: Python/uv package, core domain models, typed configuration, logging, application port/service, SQLite migration skeleton, and CLI `info`/`health`.
- Evidence: `uv sync`, Ruff format/lint, strict mypy, unit (10), integration (4), component (6), console/module entry points, `info`, repeated `health`, context-pack validation, and `git diff --check` passed.
- Commits `3461c83` and `cd7e841` contain the stage 01 implementation and runtime-isolation fix; no push to `origin/main` has been performed.
