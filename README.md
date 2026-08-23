# AI Mix Assistant

Локальный по умолчанию AI/DSP-ассистент для анализа треков, выбора сильных фрагментов,
планирования совместимых последовательностей и переходов и создания неразрушающего
таймлайна для проверки и финальной обработки в Adobe Audition.

Репозиторий содержит спецификацию и архитектуру проекта, критерии качества,
поэтапные prompts реализации и интеграционный overlay AI Dev Team.
Границы продукта описаны в [SPEC.md](SPEC.md), архитектура — в
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), а текущее состояние реализации —
в [docs/AI_STATUS.md](docs/AI_STATUS.md). Подробные этапы собраны в
[prompts/STAGES.md](prompts/STAGES.md).

## Локальная разработка

Требуется Python 3.12+ и `uv`.

```powershell
uv sync
uv run ai-mix info
uv run ai-mix health
```

`info` только читает состояние локальной SQLite-схемы. `health` при первом запуске
создаёт каталог данных и применяет миграции, затем проверяет доступность SQLite.
Для машинной обработки обе команды поддерживают `--json`.

Параметры окружения:

- `AI_MIX_DATA_DIR` — каталог локального состояния;
- `AI_MIX_DATABASE_PATH` — явный путь к SQLite вместо `<data-dir>/state.sqlite3`;
- `AI_MIX_LOG_LEVEL` — `DEBUG`, `INFO`, `WARNING`, `ERROR` или `CRITICAL`;
- `AI_MIX_BUSY_TIMEOUT_MS` — положительный SQLite busy timeout в миллисекундах.

Проверки этапа 01:

```powershell
uv run ruff format --check src tests
uv run ruff check src tests
uv run mypy src
uv run pytest tests/unit tests/integration tests/component
python tools/validate_context_pack.py
```
