# Архитектура

## Слои
```text
UI / CLI / Future MCP / Adobe adapters
                ↓
          Application Services
                ↓
              Core
 ├─ Media Catalog
 ├─ Analysis
 ├─ Segmentation
 ├─ Scoring
 ├─ Compatibility Graph
 ├─ Sequence Optimizer
 ├─ Transition Planner
 ├─ Timeline Model
 └─ Render Plan
                ↓
Infrastructure adapters
FFmpeg / Essentia / librosa / Rubber Band / Demucs / SQLite
```

## Инварианты
1. Core не зависит от GUI.
2. Аудиофайлы являются неизменяемыми исходными ресурсами.
3. Результаты анализа кэшируются по отпечатку содержимого, версии и конфигурации анализатора.
4. Таймлайн является неразрушающим и версионируемым.
5. Каждая рекомендация показывает использованные признаки и оценки.
6. Эталонный путь на CPU остаётся доступным.
7. Тяжёлые необязательные модели загружаются лениво, а использование памяти ограничивается на основании benchmark.

## Предлагаемая структура репозитория
```text
src/ai_mix_assistant/
  core/
  application/
  adapters/
    audio/
    storage/
    render/
    audition/
    cli/
  ui/
tests/
fixtures/
docs/
prompts/
.codex/agents/
.agents/skills/
```

## Реализованная основа этапа 01

```text
CLI (`ai-mix`, `python -m ai_mix_assistant`)
                ↓
        SystemStatusService
                ↓
          StateStore port
                ↓
        SQLiteStateStore
```

- `core` содержит неизменяемые модели идентичности трека и кэша анализа и не зависит от adapters/UI.
- `application` содержит типизированную конфигурацию, port локального состояния и сервис `info`/`health`.
- `adapters` содержит composition root CLI и SQLite-реализацию с connection-per-operation.
- `info` является read-only; `health` — явная инициализирующая операция.
- схема v1 содержит только `schema_migrations`; доменные таблицы принадлежат следующим этапам.

## Контракт зависимостей

- Источник истины (Source of truth): `pyproject.toml` и единственный lock-файл `uv.lock`; канонический менеджер — uv.
- Чистое восстановление (Clean restore): удалить только disposable `.venv`, затем выполнить `uv sync --locked`.
- Общий machine-level uv cache разрешён; локальная `.venv` является воспроизводимой проекцией и не коммитится.
- Build/test caches и `.venv` можно очищать после подтверждённого restore; пользовательские media, SQLite state и другие runtime-данные в dependency cleanup не входят.
- Локальные и CI-проверки должны использовать locked environment; baseline-команды — `uv run ruff format --check src tests`, `uv run ruff check src tests`, `uv run mypy src` и `uv run pytest tests/unit tests/integration tests/component`.
