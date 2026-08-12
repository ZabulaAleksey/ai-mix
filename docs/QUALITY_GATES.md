# Quality Gates

## DSP correctness
- deterministic fixtures
- tolerance-based numeric assertions
- no NaN/Inf propagation
- reproducible analysis config/version

## Segment/transition ranking
- golden fixtures
- component-score inspection
- regression tests
- manual listening set for qualitative evaluation

## Rendering
- duration and sample-rate checks
- clipping detection
- loudness/peak checks
- no source overwrite
- cancel/retry/resume where long-running

## Performance
Profile before optimise. Benchmark decode, analysis, segmentation, scoring and render separately.

## Privacy/security
- no raw media committed
- paths/logs redact sensitive data where appropriate
- external processing requires explicit opt-in
