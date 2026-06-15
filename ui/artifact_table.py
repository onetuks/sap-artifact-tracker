from PyQt6.QtCore import Qt, QSortFilterProxyModel
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QColor
from PyQt6.QtWidgets import QTableView, QHeaderView
from models.artifact import Artifact

# 테이블 열 인덱스
COL_CHECK = 0
COL_PACKAGE = 1
COL_ARTIFACT = 2
COL_RUNTIME = 3
COL_STATUS = 4

_GREY_COLOR = QColor("#e6e6e6")
_TEXT_COLOR = QColor("#000000")
_SELECTED_COLOR = QColor("#87CEEB")  # 투명한 파란색


class ArtifactFilterProxy(QSortFilterProxyModel):
    """Package / Artifact / Status 세 가지 필터를 AND 조건으로 적용."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._package_filter = ""
        self._artifact_filter = ""
        self._status_filter = ""   # "" 이면 전체

    def set_package_filter(self, text: str):
        self._package_filter = text.lower()
        self.invalidateFilter()

    def set_artifact_filter(self, text: str):
        self._artifact_filter = text.lower()
        self.invalidateFilter()

    def set_status_filter(self, status: str):
        self._status_filter = status
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row: int, source_parent) -> bool:
        model = self.sourceModel()

        def cell(col):
            return model.item(source_row, col).text() if model.item(source_row, col) else ""

        if self._package_filter and self._package_filter not in cell(COL_PACKAGE).lower():
            return False
        if self._artifact_filter and self._artifact_filter not in cell(COL_ARTIFACT).lower():
            return False
        if self._status_filter and cell(COL_STATUS) != self._status_filter:
            return False
        return True


class ArtifactTableWidget(QTableView):
    """체크박스 + 아티팩트 정보를 표시하는 테이블 위젯."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._source_model = QStandardItemModel()
        self._source_model.setHorizontalHeaderLabels(
            ["", "Package", "Artifact", "Runtime", "Status"]
        )
        self._source_model.itemChanged.connect(self._on_item_changed)

        self._proxy = ArtifactFilterProxy(self)
        self._proxy.setSourceModel(self._source_model)
        self.setModel(self._proxy)

        self._setup_view()

    def _setup_view(self):
        hdr = self.horizontalHeader()
        hdr.setSectionResizeMode(COL_CHECK, QHeaderView.ResizeMode.Fixed)
        hdr.setSectionResizeMode(COL_PACKAGE, QHeaderView.ResizeMode.Stretch)
        hdr.setSectionResizeMode(COL_ARTIFACT, QHeaderView.ResizeMode.Stretch)
        hdr.setSectionResizeMode(COL_RUNTIME, QHeaderView.ResizeMode.Stretch)
        hdr.setSectionResizeMode(COL_STATUS, QHeaderView.ResizeMode.ResizeToContents)
        self.setColumnWidth(COL_CHECK, 36)

        self.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.verticalHeader().setVisible(False)
        self.setAlternatingRowColors(False)
        self.setSortingEnabled(True)

    def load_artifacts(self, artifacts: list[Artifact]):
        self._source_model.removeRows(0, self._source_model.rowCount())
        for art in artifacts:
            check_item = QStandardItem()
            check_item.setCheckable(True)
            check_item.setCheckState(Qt.CheckState.Unchecked)
            check_item.setData(art, Qt.ItemDataRole.UserRole)

            items = [
                check_item,
                QStandardItem(art.package_name),
                QStandardItem(art.artifact_name),
                QStandardItem(art.runtime_name),
                QStandardItem(art.status.value),
            ]
            for item in items:
                item.setBackground(_GREY_COLOR)
                item.setForeground(_TEXT_COLOR)
            self._source_model.appendRow(items)

    def get_checked_artifacts(self) -> list[Artifact]:
        """체크된 행의 Artifact 객체 목록 반환."""
        result = []
        for row in range(self._source_model.rowCount()):
            item = self._source_model.item(row, COL_CHECK)
            if item and item.checkState() == Qt.CheckState.Checked:
                result.append(item.data(Qt.ItemDataRole.UserRole))
        return result

    def _on_item_changed(self, item: QStandardItem):
        """체크박스 상태 변경 시 행의 배경색 업데이트."""
        if item.column() != COL_CHECK:
            return
        row = item.row()
        is_checked = item.checkState() == Qt.CheckState.Checked
        color = _SELECTED_COLOR if is_checked else _WHITE_COLOR
        for col in range(self._source_model.columnCount()):
            cell = self._source_model.item(row, col)
            if cell:
                cell.setBackground(color)

    def proxy(self) -> ArtifactFilterProxy:
        return self._proxy
