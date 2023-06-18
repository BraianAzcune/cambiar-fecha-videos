from PySide6.QtCore import Signal
from PySide6.QtWidgets import QTableWidget


class Tabla(QTableWidget):
    RowCountChanged = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.model().rowsInserted.connect(self._handleRowCountChanged)
        self.model().rowsRemoved.connect(self._handleRowCountChanged)

    def _handleRowCountChanged(self):
        row_count = self.rowCount()
        self.RowCountChanged.emit(row_count)

    def removeAllRows(self):
        self.clear()
        self.setRowCount(0)
