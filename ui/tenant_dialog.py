import json
import requests
from requests.auth import HTTPBasicAuth

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QTextEdit, QPushButton, QMessageBox,
    QTabWidget, QWidget,
)
from models.tenant import Tenant
from services.tenant_service import save_tenant


class TenantDialog(QDialog):
    """테넌트 추가 다이얼로그.

    credential JSON 붙여넣기 탭과 수동 입력 탭을 제공.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("테넌트 추가")
        self.setMinimumWidth(480)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        self._tabs = QTabWidget()
        self._tabs.addTab(self._build_json_tab(), "JSON 붙여넣기")
        self._tabs.addTab(self._build_manual_tab(), "직접 입력")
        layout.addWidget(self._tabs)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self._save_btn = QPushButton("저장")
        self._save_btn.clicked.connect(self._on_save)
        cancel_btn = QPushButton("취소")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(self._save_btn)
        btn_row.addWidget(cancel_btn)
        layout.addLayout(btn_row)

    def _build_json_tab(self) -> QWidget:
        w = QWidget()
        v = QVBoxLayout(w)
        v.addWidget(QLabel("SAP BTP service credential JSON을 붙여넣으세요:"))
        self._json_edit = QTextEdit()
        self._json_edit.setPlaceholderText('{\n  "url": "https://...",\n  "clientid": "...",\n  "clientsecret": "..."\n}')
        v.addWidget(self._json_edit)

        name_row = QHBoxLayout()
        name_row.addWidget(QLabel("표시명:"))
        self._json_name_edit = QLineEdit()
        self._json_name_edit.setPlaceholderText("my-tenant")
        name_row.addWidget(self._json_name_edit)
        v.addLayout(name_row)
        return w

    def _build_manual_tab(self) -> QWidget:
        w = QWidget()
        v = QVBoxLayout(w)
        fields = [
            ("표시명", "_m_name", "my-tenant"),
            ("Host URL", "_m_host", "https://xxxxx.cfapps.hana.ondemand.com"),
            ("Client ID", "_m_clientid", ""),
            ("Client Secret", "_m_clientsecret", ""),
        ]
        for label, attr, placeholder in fields:
            row = QHBoxLayout()
            row.addWidget(QLabel(f"{label}:"))
            edit = QLineEdit()
            edit.setPlaceholderText(placeholder)
            if "secret" in attr.lower():
                edit.setEchoMode(QLineEdit.EchoMode.Password)
            setattr(self, attr, edit)
            row.addWidget(edit)
            v.addLayout(row)
        v.addStretch()
        return w

    def _on_save(self):
        try:
            tenant = self._build_tenant()
        except ValueError as e:
            QMessageBox.warning(self, "입력 오류", str(e))
            return

        # 연결 테스트
        try:
            self._test_connection(tenant)
        except Exception as e:
            QMessageBox.critical(
                self,
                "연결 실패",
                f"테넌트 연결에 실패했습니다.\n\n{e}",
            )
            return

        save_tenant(tenant)
        self.accept()

    def _build_tenant(self) -> Tenant:
        if self._tabs.currentIndex() == 0:
            return self._parse_json_tab()
        return self._parse_manual_tab()

    def _parse_json_tab(self) -> Tenant:
        raw = self._json_edit.toPlainText().strip()
        name = self._json_name_edit.text().strip()
        if not raw:
            raise ValueError("JSON을 입력해주세요.")
        if not name:
            raise ValueError("표시명을 입력해주세요.")
        try:
            cred = json.loads(raw)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON 파싱 오류: {e}")

        # oauth 객체 안에 필드가 있을 수 있으므로 먼저 확인
        oauth = cred.get("oauth", {})
        host = cred.get("url") or oauth.get("url") or cred.get("host") or oauth.get("host", "")
        clientid = cred.get("clientid") or oauth.get("clientid", "")
        clientsecret = cred.get("clientsecret") or oauth.get("clientsecret", "")

        if not host or not clientid or not clientsecret:
            raise ValueError("JSON에 'url', 'clientid', 'clientsecret' 필드가 필요합니다.\n(최상위 또는 'oauth' 객체 내부)")
        return Tenant(name=name, host=host.rstrip("/"), clientid=clientid, clientsecret=clientsecret)

    def _parse_manual_tab(self) -> Tenant:
        name = self._m_name.text().strip()
        host = self._m_host.text().strip()
        clientid = self._m_clientid.text().strip()
        clientsecret = self._m_clientsecret.text().strip()
        if not all([name, host, clientid, clientsecret]):
            raise ValueError("모든 필드를 입력해주세요.")
        return Tenant(name=name, host=host.rstrip("/"), clientid=clientid, clientsecret=clientsecret)

    @staticmethod
    def _test_connection(tenant: Tenant):
        """패키지 목록 API 호출로 연결 테스트."""
        url = f"{tenant.host}/api/v1/IntegrationPackages"
        resp = requests.get(
            url,
            auth=HTTPBasicAuth(tenant.clientid, tenant.clientsecret),
            headers={"Accept": "application/json"},
            timeout=10,
        )
        resp.raise_for_status()
