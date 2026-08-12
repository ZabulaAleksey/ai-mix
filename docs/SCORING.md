# Scoring

## Segment
`score = w1*salience + w2*energy + w3*hook + w4*boundary_conf + w5*tonal_stability + w6*rhythmic_stability + w7*loudness_consistency - w8*vocal_overlap_risk`

Weights are configuration, not hard-coded business law.

## Transition
Use a breakdown rather than one magic metric:
- tempo delta
- harmonic/key distance
- beat-phase alignment
- phrase-boundary compatibility
- energy slope
- spectral crowding
- vocal overlap
- time-stretch/pitch processing cost

Store breakdown for “Why?” UI.
