import json
import os
from pathlib import Path
from models.tenant import Tenant

_STORAGE_PATH = Path.home() / ".sap-artifact-tracker" / "tenants.json"


def _ensure_dir() -> None:
    _STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)


def load_tenants() -> list[Tenant]:
    if not _STORAGE_PATH.exists():
        return []
    with open(_STORAGE_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return [Tenant.from_dict(d) for d in data]


def save_tenant(tenant: Tenant) -> None:
    _ensure_dir()
    tenants = load_tenants()
    # 동일 name이면 덮어쓰기
    tenants = [t for t in tenants if t.name != tenant.name]
    tenants.append(tenant)
    _write(tenants)


def remove_tenant(name: str) -> None:
    tenants = load_tenants()
    tenants = [t for t in tenants if t.name != name]
    _ensure_dir()
    _write(tenants)


def _write(tenants: list[Tenant]) -> None:
    with open(_STORAGE_PATH, "w", encoding="utf-8") as f:
        json.dump([t.to_dict() for t in tenants], f, indent=2, ensure_ascii=False)
