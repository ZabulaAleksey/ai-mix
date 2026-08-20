# Модель данных

Основные сущности:
- `Track`
- `MediaFingerprint`
- `AnalysisProfile`
- `AnalysisResult`
- `StructureSection`
- `PhraseBoundary`
- `CandidateSegment`
- `SegmentScoreBreakdown`
- `CompatibilityEdge`
- `TransitionPlan`
- `Timeline`
- `TimelineClip`
- `AutomationEnvelope`
- `RenderJob`
- `ExportArtifact`

Все кэшированные результаты анализа содержат версию анализатора и хеш конфигурации.

## Состояние реализации

На этапе 01 реализованы только фундаментальные value objects: `TrackId`, `Track`,
`MediaFingerprint`, `AnalysisProfile` и `AnalysisCacheKey`. Остальные перечисленные
сущности являются запланированными контрактами своих этапов и пока не реализованы.
SQLite-схема v1 намеренно не содержит доменных таблиц.
