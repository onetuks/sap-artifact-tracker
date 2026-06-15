from dataclasses import dataclass, field
from enum import Enum


class ArtifactStatus(Enum):
    DEPLOYED = "Deployed"          # design-time O + runtime O
    NOT_DEPLOYED = "Not Deployed"  # design-time O + runtime X
    INACTIVE = "Inactive"          # design-time X + runtime O (런타임만 존재)


@dataclass
class Artifact:
    package_id: str
    package_name: str
    artifact_id: str
    artifact_name: str
    version: str
    runtime_name: str          # 런타임에서의 이름 (INACTIVE이면 design-time 없음)
    status: ArtifactStatus
