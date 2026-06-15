from PyQt6.QtCore import QThread, pyqtSignal
from api.client import SapClient
from models.artifact import Artifact
from models.tenant import Tenant
from services.artifact_service import fetch_all_artifacts


class FetchWorker(QThread):
    """백그라운드에서 SAP IS API를 호출하여 아티팩트 목록을 가져오는 워커."""

    finished = pyqtSignal(list)   # list[Artifact]
    error = pyqtSignal(str)

    def __init__(self, tenant: Tenant, parent=None):
        super().__init__(parent)
        self._tenant = tenant

    def run(self):
        try:
            client = SapClient(self._tenant)
            artifacts = fetch_all_artifacts(client)
            self.finished.emit(artifacts)
        except Exception as e:
            self.error.emit(str(e))


class ActionWorker(QThread):
    """배포/undeploy/삭제 등 일괄 작업을 백그라운드에서 처리하는 워커."""

    progress = pyqtSignal(int, int, str)   # (현재, 전체, 아티팩트명)
    finished = pyqtSignal(list)            # list[str] — 실패 메시지 목록
    error = pyqtSignal(str)

    def __init__(self, tenant: Tenant, action_fn, artifacts: list, parent=None):
        """
        action_fn: (SapClient, Artifact) -> None 형태의 콜백.
        """
        super().__init__(parent)
        self._tenant = tenant
        self._action_fn = action_fn
        self._artifacts = artifacts

    def run(self):
        print("DEBUG: ActionWorker.run() 시작")
        client = SapClient(self._tenant)
        failures: list[str] = []
        total = len(self._artifacts)
        print(f"DEBUG: 처리할 아티팩트 수: {total}")
        for i, artifact in enumerate(self._artifacts, start=1):
            name = artifact.artifact_name if artifact.artifact_name != "-" else artifact.runtime_name
            print(f"DEBUG: 아티팩트 처리 중 ({i}/{total}): {name}")
            self.progress.emit(i, total, name)
            try:
                self._action_fn(client, artifact)
                print(f"DEBUG: {name} 처리 완료")
            except Exception as e:
                print(f"DEBUG: {name} 처리 중 에러: {e}")
                failures.append(f"{name}: {e}")
        print(f"DEBUG: ActionWorker.run() 완료 - 실패 수: {len(failures)}")
        self.finished.emit(failures)
