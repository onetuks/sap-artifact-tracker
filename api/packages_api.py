from api.client import SapClient


def fetch_packages(client: SapClient) -> list[dict]:
    """모든 Integration Package 조회."""
    data = client.get("/api/v1/IntegrationPackages")
    return data.get("d", {}).get("results", [])


def fetch_designtime_artifacts(client: SapClient, package_id: str) -> list[dict]:
    """특정 패키지 내 모든 design-time artifact 조회."""
    path = f"/api/v1/IntegrationPackages('{package_id}')/IntegrationDesigntimeArtifacts"
    data = client.get(path)
    return data.get("d", {}).get("results", [])


def deploy_artifact(client: SapClient, artifact_id: str, version: str) -> None:
    """design-time artifact를 런타임에 배포."""
    client.post(
        "/api/v1/DeployIntegrationDesigntimeArtifact",
        params={"Id": f"'{artifact_id}'", "Version": f"'{version}'"},
    )


def delete_designtime_artifact(client: SapClient, artifact_id: str, version: str) -> None:
    """design-time artifact 삭제."""
    path = f"/api/v1/IntegrationDesigntimeArtifacts(Id='{artifact_id}',Version='{version}')"
    client.delete(path)
