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
