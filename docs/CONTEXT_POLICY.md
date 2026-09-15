# Политика контекста

Порядок загрузки:
1. Глобальная AI Dev Team.
2. Корневой `AGENTS.md`.
3. Активные модульные или локальные правила.
4. Относящийся к задаче раздел `SPEC.md`.
5. Относящийся к задаче раздел `docs/ARCHITECTURE.md`.
6. Только выбранный record `docs/STAGES.md`.
7. Текущая задача, diff и тесты.

Не загружай заранее всю дорожную карту, историю prompts, старые отчёты или все fixtures.

Канонические источники:
- требования: `SPEC.md`;
- архитектура: `docs/ARCHITECTURE.md` + `docs/DECISIONS.md`;
- текущее состояние и stage execution: выбранный record `docs/STAGES.md`;
- historical launchers: `docs/STAGES.md` ниже текущего record и
  `docs/notes/stage-launchers.md` (без самостоятельного current state);
- хронология реализации: `DEV_LOG.md`;
- учебные объяснения: `LEARNING.md`.
