# Architecture

## Layers
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

## Invariants
1. Core does not depend on GUI.
2. Audio files are immutable source assets.
3. Analyses are cacheable by content fingerprint + analyzer version/config.
4. Timeline is non-destructive and versioned.
5. Every recommendation exposes features/scores used.
6. Reference CPU path remains available.
7. Heavy optional models are lazy-loaded and bounded by memory benchmark.

## Suggested repository
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
