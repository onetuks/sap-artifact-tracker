from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QListWidget, QProgressDialog,
)
from PyQt6.QtCore import Qt
from models.artifact import Artifact


class ConfirmDialog(QDialog):
    """일괄 작업 실행 전 사용자 확인 모달."""

    def __init__(self, action_label: str, artifacts: list[Artifact], parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"작업 확인 — {action_label}")
        self.setMinimumWidth(420)
        self._build_ui(action_label, artifacts)

    def _build_ui(self, action_label: str, artifacts: list[Artifact]):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"<b>{len(artifacts)}개</b>의 아티팩트에 대해 <b>{action_label}</b> 작업을 수행합니다."))

        lst = QListWidget()
        for art in artifacts:
            name = art.artifact_name if art.artifact_name != "-" else art.runtime_name
            lst.addItem(f"  {art.package_name}  /  {name}")
        lst.setMaximumHeight(200)
        layout.addWidget(lst)

        layout.addWidget(QLabel("계속 진행하시겠습니까?"))

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        ok_btn = QPushButton("확인")
        ok_btn.setDefault(True)
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("취소")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(ok_btn)
        btn_row.addWidget(cancel_btn)
        layout.addLayout(btn_row)


def make_progress_dialog(action_label: str, total: int, parent=None) -> QProgressDialog:
    dlg = QProgressDialog(f"{action_label} 중...", "취소", 0, total, parent)
    dlg.setWindowTitle(action_label)
    dlg.setWindowModality(Qt.WindowModality.WindowModal)
    dlg.setMinimumWidth(340)
    dlg.setValue(0)
    return dlg
