# AI Mix Assistant — Project Overlay

This repository inherits the globally installed **AI Dev Team Codex**.

## Project law
- `project = overlay`: do not duplicate generic Architect / QA / Security / Git / Docs agents or a second Git workflow.
- Read `SPEC.md`, `ARCHITECTURE.md`, `docs/DECISIONS.md`, `PROGRESS.md`, and the active stage prompt before implementation.
- Business/DSP logic belongs in Core/Application; UI, CLI, future MCP and Adobe integration are adapters.
- CPU/reference DSP path must remain available when experimental ML/GPU components are added.
- Experimental features require: feature flag → fallback → tests → benchmark → docs/ADR.
- Preserve user media locally by default. Never commit raw tracks, stems, exports, secrets, or user datasets.
- Make minimal verifiable changes; update tests and `PROGRESS.md`.
- A stage is complete only after its DoD/tests pass and review/merge criteria are satisfied.

## Context loading
Load only the relevant spec section, module docs, active prompt and required skill. Do not preload the whole prompt library or old reports.

## Required project docs
- `SPEC.md`
- `ARCHITECTURE.md`
- `DESIGN.md`
- `PROGRESS.md`
- `DEV_LOG.md`
- `LEARNING.md`
- `docs/DECISIONS.md`
- `docs/CONTEXT_POLICY.md`
- `docs/AI_DEV_TEAM_INTEGRATION.md`
- `prompts/README.md`
