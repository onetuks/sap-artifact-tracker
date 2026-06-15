from api.client import SapClient


def fetch_runtime_artifacts(client: SapClient) -> list[dict]:
    """배포된 모든 runtime artifact 조회."""
    data = client.get("/api/v1/IntegrationRuntimeArtifacts")
    return data.get("d", {}).get("results", [])


def undeploy_artifact(client: SapClient, artifact_id: str) -> None:
    """런타임 artifact undeploy."""
    client.delete(f"/api/v1/IntegrationRuntimeArtifacts('{artifact_id}')")
