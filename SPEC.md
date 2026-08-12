# AI Mix Assistant — SPEC v0.1

## Goal
Offline-first AI/DSP assistant for analysing tracks, selecting strong 20–60 second fragments, planning compatible sequences/transitions and producing a non-destructive timeline that can be reviewed and finished in Adobe Audition 2025.

## Core pipeline
`Ingest → Fingerprint/Metadata → Music Analysis → Structure/Phrase Segmentation → Candidate Segments → Segment Scoring → Compatibility Graph → Sequence Optimizer → Transition Planner → Non-destructive Timeline → Preview/Manual Edit → WAV/FLAC Render`

## Required analysis
- BPM / beat grid / downbeats
- key / chroma / harmonic confidence
- loudness / peak / dynamics
- energy curve
- spectral features
- structure / sections / phrase boundaries
- vocal density proxy
- fingerprints / duplicate detection

## SegmentScore
Candidate 20–60 s windows may combine:
- structural salience
- energy
- novelty/hook score
- phrase-boundary confidence
- tonal stability
- rhythmic stability
- loudness consistency
- vocal density / vocal-overlap risk

Scores must be inspectable and explainable.

## TransitionScore
- tempo compatibility
- key/harmonic compatibility
- beat-phase compatibility
- phrase compatibility
- energy-flow compatibility
- spectral density
- vocal overlap
- required processing cost / time-stretch amount

## Non-destructive editing
The engine must store source references, in/out points, fades, gain/envelopes, time-stretch/pitch operations and transition parameters without destructively rewriting originals.

## UI
Professional dark audio-workstation layout:
- Library
- Analysis/inspector
- Timeline
- Transition inspector
- Preview
- “Why?” explanation for segment and transition choices

Semantic accents:
- cyan = analysis / compatible / technical
- amber = warning / risky transition
- violet = AI/recommendation

## Integration
Adobe Audition 2025 is a finishing/editing target. Codex orchestrates development; DSP/analysis is implemented by specialised libraries, not “LLM-generated audio math”.

## Stack
Baseline:
- Python
- `uv`
- librosa
- Essentia where licensing/packaging permits
- FFmpeg/FFprobe
- Rubber Band for high-quality time stretch/pitch shift where available
- aubio where useful
- NumPy/SciPy
- SQLite for local project state

Optional adapters:
- Demucs for stem separation
- Whisper for speech/vocal metadata experiments
- ONNX Runtime / GPU inference when justified by benchmark

## Privacy
Local-first. Network/LLM services are optional adapters and must be explicit opt-in.

## Export
- WAV/FLAC render
- project/timeline JSON
- interchange format where feasible
- future Audition-friendly handoff

## Non-goals v0.1
- fully autonomous final mastering
- replacing Adobe Audition
- mandatory cloud processing
- black-box transitions without explanations
