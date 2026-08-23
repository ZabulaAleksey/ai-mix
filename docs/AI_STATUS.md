# Статус AI

## Governance migration — 2026-08-24

- Репозиторий находится в `~/codex-workspace/ai-mix`; подробные legacy prompts объединены в `prompts/STAGES.md`.
- `python tools/validate_context_pack.py` и глобальный project overlay validator — PASS.
- Продуктовый код и tests не изменялись; push/merge не выполнялись.

- Состояние: overlay консолидирован; продуктовый код не изменён.
- Ветка: `chore/full-governance-migration`.
- Проверки: `python tools/validate_context_pack.py` и проектные pytest-наборы.
- Риск: optional ML/GPU и GUI не являются подтверждёнными требованиями без отдельного решения.
