# Исторический source snapshot AI state

Уникальные факты старых `docs/AI_PLAN.md` и `docs/AI_STATUS.md` из GitHub
`main` `913a1bf` сохранены до вывода live owners. SHA-256 исходных bytes:
AI_PLAN `be0544dc664041d31640cdebf041f0ab1c4e5d680225fb464939c4be50f2c6ab`,
AI_STATUS `4f43b608e8feb7009b6747b03a3581660e2bea3488f5af52a0d91ec288c661ff`.
Старый `prompts/STAGES.md` был перенесён с source SHA-256
`6b1774ec008e8a0f94df829954898f1104ac47d4c6bc103206cd6f6b0fec085c`;
его оригинал есть в Git parent. Эти сведения не являются current
plan/status/NEXT; выбранный record находится в `docs/STAGES.md`.

## Из старого AI_PLAN

- Задача на момент записи: governance migration и консолидация прежних
  stage prompts. Следующая product работа выбирается по ROADMAP/SPEC
  с обязательными context-pack проверками.
- Предложенный Stage 02: отдельная branch, ingest/media catalog без
  музыкального анализа. Перед завершением подтверждать scope, tests,
  quality gates, review и status; `DEV_LOG.md`/`LEARNING.md` обновлять
  только при новых фактах.

## Из старого AI_STATUS

- Dependency audit 2026-08-24 признал canonical `uv`,
  `pyproject.toml`, `uv.lock`; migration не требовалась. Clean restore,
  shared cache и safe cleanup contract были документированы,
  product dependencies/runtime state не менялись.
- Governance migration консолидировала подробные prompts в старом
  `prompts/STAGES.md`; context-pack и project validator тогда PASS.
  Dependency audit локально вошёл в `main`; product code/tests не менялись.
  На момент исходной записи repository находился в
  `~/codex-workspace/ai-mix`, branch `chore/full-governance-migration`,
  push не выполнялся. Optional ML/GPU/GUI оставались unverified.
- Product Stage 01 был реализован, локально validated/committed/merged:
  Python/uv foundation, domain models, typed config/logging,
  application port/service, SQLite migration skeleton, CLI info/health.
  Исторические checks: uv sync, Ruff, strict mypy, unit 10,
  integration 4, component 6, console/module entry points,
  повторный health, context pack, diff check. Commits `3461c83`,
  `cd7e841` включали implementation и runtime isolation fix.
- Фраза «no push to origin/main» относится ко времени старой записи;
  оба commits теперь находятся в GitHub default `main` `913a1bf`.
