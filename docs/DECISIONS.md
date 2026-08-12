# Architectural Decisions

## ADR-001 — Project overlay
Use the global AI Dev Team for generic agents/workflow/security/docs. Keep only AI Mix Assistant domain deltas here.

## ADR-002 — Offline-first
Local analysis and project state are baseline. Cloud/LLM adapters require explicit opt-in.

## ADR-003 — Non-destructive timeline
Never treat rendered intermediate files as canonical editing state. Canonical state is source references + operations.

## ADR-004 — Explainable scoring
Segment/transition ranking must expose component scores/features. No opaque “AI says this is best”.

## ADR-005 — DSP libraries over LLM math
Use established DSP/audio libraries and deterministic algorithms for analysis/rendering; LLM/Codex is orchestration/assistance, not the audio engine.
