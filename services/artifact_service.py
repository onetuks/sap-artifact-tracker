from api.client import SapClient
from api.packages_api import fetch_packages, fetch_designtime_artifacts
from api.runtime_api import fetch_runtime_artifacts
from models.artifact import Artifact, ArtifactStatus


def fetch_all_artifacts(client: SapClient) -> list[Artifact]:
    """
    design-time + runtime 아티팩트를 조회하여 병합한 뒤 Artifact 목록으로 반환.

    병합 기준: artifact Id 일치 여부
    - design-time O + runtime O  → DEPLOYED
    - design-time O + runtime X  → NOT_DEPLOYED
    - design-time X + runtime O  → INACTIVE
    """
    packages = fetch_packages(client)
    runtime_list = fetch_runtime_artifacts(client)

    # 런타임을 Id 기준으로 인덱싱
    runtime_map: dict[str, dict] = {r["Id"]: r for r in runtime_list}

    result: list[Artifact] = []
    seen_runtime_ids: set[str] = set()

    for pkg in packages:
        pkg_id = pkg["Id"]
        pkg_name = pkg.get("Name", pkg_id)
        designtime_list = fetch_designtime_artifacts(client, pkg_id)

        for dt in designtime_list:
            art_id = dt["Id"]
            art_name = dt.get("Name", art_id)
            version = dt.get("Version", "active")

            if art_id in runtime_map:
                rt = runtime_map[art_id]
                status = ArtifactStatus.DEPLOYED
                runtime_name = rt.get("Name", art_id)
                seen_runtime_ids.add(art_id)
            else:
                status = ArtifactStatus.NOT_DEPLOYED
                runtime_name = "-"

            result.append(Artifact(
                package_id=pkg_id,
                package_name=pkg_name,
                artifact_id=art_id,
                artifact_name=art_name,
                version=version,
                runtime_name=runtime_name,
                status=status,
            ))

    # runtime에만 존재하는 아티팩트 (INACTIVE)
    for rt_id, rt in runtime_map.items():
        if rt_id not in seen_runtime_ids:
            result.append(Artifact(
                package_id="-",
                package_name="-",
                artifact_id=rt_id,
                artifact_name="-",
                version="-",
                runtime_name=rt.get("Name", rt_id),
                status=ArtifactStatus.INACTIVE,
            ))

    return result
