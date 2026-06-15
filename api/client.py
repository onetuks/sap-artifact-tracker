import logging
import requests
from requests.auth import HTTPBasicAuth
from models.tenant import Tenant

logger = logging.getLogger(__name__)


class SapClient:
    """Basic Auth 기반 SAP IS API HTTP 클라이언트."""

    def __init__(self, tenant: Tenant):
        self._base = tenant.host
        self._auth = HTTPBasicAuth(tenant.clientid, tenant.clientsecret)
        self._session = requests.Session()
        self._session.auth = self._auth
        self._session.headers.update({"Accept": "application/json"})

    def get(self, path: str, params: dict | None = None) -> dict:
        url = f"{self._base}{path}"
        resp = self._session.get(url, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def post(self, path: str, params: dict | None = None) -> requests.Response:
        url = f"{self._base}{path}"
        print(f"\n>>> POST 요청 시작: {url}")

        # X-CSRF-Token을 받기 위해 먼저 GET 요청
        fetch_headers = {"X-CSRF-Token": "Fetch"}
        fetch_response = self._session.get(url, headers=fetch_headers)

        if fetch_response.status_code not in [200, 201]:
            raise Exception(f"Token fetch failed. Status: {fetch_response.status_code}")

        csrf_token = fetch_response.headers.get("x-csrf-token")
        if not csrf_token:
            raise Exception("Token fetch failed. No X-CSRF-Token header")
        print(f">>> 토큰: {csrf_token}")

        # POST 요청에 토큰 포함
        post_headers = {"X-CSRF-Token": csrf_token}
        print(f">>> POST 헤더: {post_headers}")
        resp = self._session.post(url, params=params, headers=post_headers, timeout=30)
        print(f">>> POST 응답 상태: {resp.status_code}")
        resp.raise_for_status()
        print(f">>> POST 완료: {url}")
        return resp

    def delete(self, path: str) -> requests.Response:
        url = f"{self._base}{path}"
        print(f"\n>>> DELETE 요청 시작: {url}")

        fetch_headers = {"X-CSRF-Token": "Fetch"}
        fetch_response = self._session.get(url, headers=fetch_headers)

        if fetch_response.status_code not in [200, 201]:
            raise Exception(f"Token fetch failed. Status: {fetch_response.status_code}")

        csrf_token = fetch_response.headers.get("x-csrf-token")
        if not csrf_token:
            raise Exception("Token fetch failed. No X-CSRF-Token header")
        print(f">>> 토큰: {csrf_token}")

        delete_headers = {"X-CSRF-Token": csrf_token}
        print(f">>> DELETE 헤더: {delete_headers}")
        resp = self._session.delete(url, headers=delete_headers, timeout=30)
        print(f">>> DELETE 응답 상태: {resp.status_code}")
        resp.raise_for_status()
        print(f">>> DELETE 완료: {url}")
        return resp
