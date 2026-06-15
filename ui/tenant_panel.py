from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QComboBox,
    QPushButton, QMessageBox,
)
from PyQt6.QtCore import pyqtSignal
from models.tenant import Tenant
from services.tenant_service import load_tenants, remove_tenant


class TenantPanel(QWidget):
    """테넌트 선택 콤보박스, 추가/제거 버튼, Search 버튼을 제공하는 상단 패널."""

    tenant_selected = pyqtSignal(object)   # Tenant | None
    search_requested = pyqtSignal(object)  # Tenant

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(QLabel("Tenant:"))

        self._combo = QComboBox()
        self._combo.setMinimumWidth(220)
        self._combo.currentIndexChanged.connect(self._on_combo_changed)
        layout.addWidget(self._combo)

        self._add_btn = QPushButton("+ Add")
        self._add_btn.setFixedWidth(70)
        layout.addWidget(self._add_btn)

        self._remove_btn = QPushButton("- Remove")
        self._remove_btn.setFixedWidth(80)
        self._remove_btn.clicked.connect(self._on_remove)
        layout.addWidget(self._remove_btn)

        layout.addStretch()

        self._search_btn = QPushButton("Search")
        self._search_btn.setFixedWidth(80)
        self._search_btn.clicked.connect(self._on_search)
        layout.addWidget(self._search_btn)

        self.refresh()

    def add_button(self) -> QPushButton:
        return self._add_btn

    def refresh(self):
        """저장된 테넌트 목록을 다시 로드하여 콤보박스 갱신."""
        self._combo.blockSignals(True)
        current_name = self._combo.currentText()
        self._combo.clear()
        for t in load_tenants():
            self._combo.addItem(t.name, t)
        # 이전 선택 복원
        idx = self._combo.findText(current_name)
        if idx >= 0:
            self._combo.setCurrentIndex(idx)
        self._combo.blockSignals(False)
        self._update_remove_btn()

    def current_tenant(self) -> Tenant | None:
        if self._combo.count() == 0:
            return None
        return self._combo.currentData()

    def _on_combo_changed(self, _idx: int):
        self.tenant_selected.emit(self.current_tenant())
        self._update_remove_btn()

    def _on_remove(self):
        tenant = self.current_tenant()
        if tenant is None:
            return
        reply = QMessageBox.question(
            self,
            "테넌트 제거",
            f"'{tenant.name}' 테넌트를 제거하시겠습니까?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            remove_tenant(tenant.name)
            self.refresh()

    def _on_search(self):
        tenant = self.current_tenant()
        if tenant is None:
            QMessageBox.warning(self, "테넌트 없음", "등록된 테넌트가 없습니다.\n테넌트를 먼저 추가해주세요.")
            return
        self.search_requested.emit(tenant)

    def _update_remove_btn(self):
        self._remove_btn.setEnabled(self._combo.count() > 0)
