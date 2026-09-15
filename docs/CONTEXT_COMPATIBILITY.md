# Совместимость контекста

| Слой | Классификация | Решение |
|---|---|---|
| `tools/validate_context_pack.py` | PROJECT_ONLY | Сохраняется как локальная проверка AI Mix и не дублирует глобальный validator. |
| `context/` | PROJECT_ONLY | Содержит только проектный MCP/hooks-контекст; общие правила наследуются из `~/.codex`. |

## STAGES location migration — 2026-09-15

Read-only `reconcile_project_framework.py`: `prompts/STAGES.md`,
`docs/AI_PLAN.md`, `docs/AI_STATUS.md` получили `MERGE`; product code,
accepted tests, lockfile, `docs/LEARNING_LOG.md` и `SPEC.md` сохранены.
Локальный `tools/validate_context_pack.py` — `FORBIDDEN_TO_OVERWRITE`
для framework generator, но его существующая required-path логика
минимально адаптирована по прямому требованию пользователя.

| Поверхность | Legacy conflict | Fact-based resolution | Итог |
| --- | --- | --- | --- |
| Current stage | Старый STAGES — каталог launchers без selector; AI_PLAN предлагает Stage 02, AI_STATUS утверждает Stage 01 локально | Оба Stage 01 commits входят в GitHub `main`; 20 accepted tests, mypy, product Ruff, CLI info/health и context-pack PASS | `ADAPT`: `AM-INGEST-02`, `planned` |
| NEXT | Legacy prompt — ingest/media catalog, но `SPEC.md` не задаёт Stage 02 behavior contract | Сначала создать behavior SPEC/consumer scenario, затем implementation | `ADAPT`: `AM-INGEST-02-SPEC` |
| Historical facts | AI pair хранит uv audit, Stage 01 evidence и устаревшее «no push» | Сохранить past facts/hashes в `docs/notes`; current GitHub commit подтвердить отдельно | `MERGE` разрешён |
| Unique launcher bytes | `prompts/STAGES.md` содержит прежние stage prompts, `prompts/README.md` — workflow | Сохранить STAGES текст ниже selected record и README в `docs/notes/stage-launchers.md` | `PRESERVE` |

Structured DEV bridge не добавлялся; path задан прямым указанием
пользователя. Source Git parent — recoverable rollback point.
