# Context Policy

Load order:
1. Global AI Dev Team
2. Root `AGENTS.md`
3. Active module/local rules
4. `SPEC.md` relevant section
5. `ARCHITECTURE.md` relevant section
6. active stage prompt
7. current task/diff/tests

Do not preload the entire roadmap, prompt history, old reports or all fixtures.

Canonical:
- requirements: `SPEC.md`
- architecture: `ARCHITECTURE.md` + `docs/DECISIONS.md`
- current state: `PROGRESS.md`
- execution prompts: `prompts/`
- implementation chronology: `DEV_LOG.md`
- explanatory learning: `LEARNING.md`
