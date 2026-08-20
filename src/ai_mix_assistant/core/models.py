"""Immutable, dependency-free domain value objects."""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Any

_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


@dataclass(frozen=True, slots=True)
class TrackId:
    """Stable identifier for a track in the local catalog."""

    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str) or not self.value.strip():
            raise ValueError("track id must be a non-empty string")
        object.__setattr__(self, "value", self.value.strip())

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class Track:
    """A source media reference; the source itself is never modified."""

    track_id: TrackId
    path: Path
    title: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.track_id, TrackId):
            raise TypeError("track_id must be a TrackId")
        if isinstance(self.path, str) and not self.path.strip():
            raise ValueError("track path must not be empty")
        path = Path(self.path).expanduser()
        if path == Path("."):
            raise ValueError("track path must not be empty")
        object.__setattr__(self, "path", path)
        if self.title is not None and not self.title.strip():
            raise ValueError("track title must not be blank")


@dataclass(frozen=True, slots=True)
class MediaFingerprint:
    """Canonical SHA-256 digest of media content."""

    sha256: str

    def __post_init__(self) -> None:
        if not isinstance(self.sha256, str) or not _SHA256_RE.fullmatch(self.sha256):
            raise ValueError("sha256 must be exactly 64 hexadecimal characters")
        object.__setattr__(self, "sha256", self.sha256.lower())

    @property
    def value(self) -> str:
        return self.sha256

    @classmethod
    def from_bytes(cls, content: bytes) -> MediaFingerprint:
        return cls(hashlib.sha256(content).hexdigest())


@dataclass(frozen=True, slots=True)
class AnalysisProfile:
    """Versioned, deterministic analyzer configuration."""

    analyzer_id: str
    analyzer_version: str
    configuration: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.analyzer_id, str) or not self.analyzer_id.strip():
            raise ValueError("analyzer_id must be a non-empty string")
        if not isinstance(self.analyzer_version, str) or not self.analyzer_version.strip():
            raise ValueError("analyzer_version must be a non-empty string")
        normalized = _freeze_mapping(self.configuration)
        object.__setattr__(self, "analyzer_id", self.analyzer_id.strip())
        object.__setattr__(self, "analyzer_version", self.analyzer_version.strip())
        object.__setattr__(self, "configuration", normalized)

    @property
    def version(self) -> str:
        return self.analyzer_version

    @property
    def configuration_hash(self) -> str:
        payload = json.dumps(
            _plain_json(self.configuration),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class AnalysisCacheKey:
    """Identity for a cached analysis result."""

    fingerprint: MediaFingerprint
    track_id: TrackId
    analyzer_id: str
    analyzer_version: str
    configuration_hash: str

    def __post_init__(self) -> None:
        if not isinstance(self.fingerprint, MediaFingerprint):
            raise TypeError("fingerprint must be a MediaFingerprint")
        if not isinstance(self.track_id, TrackId):
            raise TypeError("track_id must be a TrackId")
        if not self.analyzer_id.strip():
            raise ValueError("analyzer_id must be a non-empty string")
        if not self.analyzer_version.strip():
            raise ValueError("analyzer_version must be a non-empty string")
        if not _SHA256_RE.fullmatch(self.configuration_hash):
            raise ValueError("configuration_hash must be a SHA-256 hexadecimal digest")
        object.__setattr__(self, "analyzer_id", self.analyzer_id.strip())
        object.__setattr__(self, "analyzer_version", self.analyzer_version.strip())
        object.__setattr__(self, "configuration_hash", self.configuration_hash.lower())

    @classmethod
    def for_profile(
        cls, track_id: TrackId, fingerprint: MediaFingerprint, profile: AnalysisProfile
    ) -> AnalysisCacheKey:
        return cls(
            fingerprint,
            track_id,
            profile.analyzer_id,
            profile.analyzer_version,
            profile.configuration_hash,
        )


def _freeze_mapping(values: Mapping[str, Any]) -> Mapping[str, Any]:
    if not isinstance(values, Mapping):
        raise TypeError("configuration must be a mapping")
    if not all(isinstance(key, str) for key in values):
        raise TypeError("configuration keys must be strings")
    frozen = MappingProxyType({key: _freeze_json(value) for key, value in values.items()})
    # Canonical serialization rejects unsupported values and NaN/Infinity.
    json.dumps(
        _plain_json(frozen),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )
    return frozen


def _freeze_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        if not all(isinstance(key, str) for key in value):
            raise TypeError("configuration keys must be strings")
        return MappingProxyType({key: _freeze_json(item) for key, item in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_json(item) for item in value)
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise TypeError(f"unsupported configuration value: {type(value).__name__}")


def _plain_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _plain_json(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_plain_json(item) for item in value]
    return value
