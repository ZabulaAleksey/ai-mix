from pathlib import Path

import pytest

from ai_mix_assistant.core import (
    AnalysisCacheKey,
    AnalysisProfile,
    MediaFingerprint,
    Track,
    TrackId,
)


def test_domain_models_are_immutable_and_cache_key_is_deterministic() -> None:
    track_id = TrackId("track-1")
    fingerprint = MediaFingerprint("A" * 64)
    profile_a = AnalysisProfile("reference", "1.0", {"sample_rate": 48000, "channels": 2})
    profile_b = AnalysisProfile("reference", "1.0", {"channels": 2, "sample_rate": 48000})

    assert Track(track_id, Path("song.wav")).track_id == track_id
    assert profile_a.configuration_hash == profile_b.configuration_hash
    assert AnalysisCacheKey.for_profile(
        track_id, fingerprint, profile_a
    ) == AnalysisCacheKey.for_profile(track_id, fingerprint, profile_b)
    with pytest.raises((AttributeError, TypeError)):
        track_id.value = "changed"  # type: ignore[misc]


def test_fingerprint_requires_sha256() -> None:
    with pytest.raises(ValueError):
        MediaFingerprint("not-a-digest")

    assert MediaFingerprint.from_bytes(b"hello").sha256 == (
        "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    )


def test_track_rejects_an_empty_source_path() -> None:
    with pytest.raises(ValueError):
        Track(TrackId("track-1"), Path("."))
    with pytest.raises(ValueError):
        Track(TrackId("track-1"), "")  # type: ignore[arg-type]


def test_configuration_rejects_invalid_profile_values() -> None:
    with pytest.raises(ValueError):
        TrackId(" ")
    with pytest.raises(ValueError):
        AnalysisProfile("", "1.0")
    with pytest.raises(ValueError):
        AnalysisProfile("reference", "")


def test_analysis_profile_deeply_freezes_configuration() -> None:
    original = {"channels": ["left", "right"], "nested": {"enabled": True}}
    profile = AnalysisProfile("reference", "1.0", original)
    original["channels"].append("center")

    assert profile.configuration["channels"] == ("left", "right")
    with pytest.raises(TypeError):
        profile.configuration["nested"]["enabled"] = False  # type: ignore[index]
