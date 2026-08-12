# MCP

На начальных этапах проектный MCP не требуется.

Будущий MCP допускается только в том случае, если само приложение предоставляет полезные семантические операции, например:
- analyse_track
- propose_segments
- explain_segment_score
- rank_transitions
- build_timeline
- render_preview

MCP должен вызывать Application Services, а не дублировать бизнес-логику.
