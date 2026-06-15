from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QComboBox
from PyQt6.QtCore import pyqtSignal
from models.artifact import ArtifactStatus

_ALL_LABEL = "All"


class FilterBar(QWidget):
    """Package / Artifact 검색 입력과 Status 콤보박스를 제공하는 필터 영역."""

    package_changed = pyqtSignal(str)
    artifact_changed = pyqtSignal(str)
    status_changed = pyqtSignal(str)   # "" 이면 전체

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 4)

        layout.addWidget(QLabel("Package:"))
        self._pkg_edit = QLineEdit()
        self._pkg_edit.setPlaceholderText("패키지명 검색...")
        self._pkg_edit.textChanged.connect(self.package_changed)
        layout.addWidget(self._pkg_edit)

        layout.addWidget(QLabel("Artifact:"))
        self._art_edit = QLineEdit()
        self._art_edit.setPlaceholderText("아티팩트명 검색...")
        self._art_edit.textChanged.connect(self.artifact_changed)
        layout.addWidget(self._art_edit)

        layout.addWidget(QLabel("Status:"))
        self._status_combo = QComboBox()
        self._status_combo.addItem(_ALL_LABEL, "")
        for s in ArtifactStatus:
            self._status_combo.addItem(s.value, s.value)
        self._status_combo.currentIndexChanged.connect(self._on_status_changed)
        layout.addWidget(self._status_combo)

    def _on_status_changed(self, _idx: int):
        self.status_changed.emit(self._status_combo.currentData())

    def clear(self):
        self._pkg_edit.clear()
        self._art_edit.clear()
        self._status_combo.setCurrentIndex(0)
