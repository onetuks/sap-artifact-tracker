import requests
from requests.auth import HTTPBasicAuth
from models.tenant import Tenant


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
        resp = self._session.post(url, params=params, timeout=30)
        resp.raise_for_status()
        return resp

    def delete(self, path: str) -> requests.Response:
        url = f"{self._base}{path}"
        resp = self._session.delete(url, timeout=30)
        resp.raise_for_status()
        return resp
