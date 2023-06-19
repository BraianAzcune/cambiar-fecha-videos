from enum import IntEnum
from PySide6.QtCore import Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QAbstractItemView,
)
from getMediaData import getFechaProduccion


class Columna(IntEnum):
    ORIGEN = 0
    ARCHIVO = 1
    FECHA = 2
    SELECCIONADO = 3


class Tabla(QTableWidget):
    RowCountChanged = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setColumnCount(Columna.__len__())
        columna_names = list(columna.name.capitalize() for columna in Columna)
        self.setHorizontalHeaderLabels(columna_names)
        self.model().rowsInserted.connect(self._handleRowCountChanged)
        self.model().rowsRemoved.connect(self._handleRowCountChanged)

    def _handleRowCountChanged(self):
        row_count = self.rowCount()
        self.RowCountChanged.emit(row_count)

    def removeAllRows(self):
        self.clear()
        self.setRowCount(0)

    def addRow(self, path: str):
        if not self.checkUnique(path):
            return "duplicado= " + path
        # ver si se le puede extraer fecha de produccion, sino tiene, es porque no.
        fechaProduccion = getFechaProduccion(path)
        if fechaProduccion is None:
            return "no se le puede extraer fecha produccion= " + path

        self.insertRow(self.rowCount())
        posFila = self.rowCount() - 1
        # poner boton de origen
        btnOrigen = QPushButton("Poner origen")
        btnOrigen.setCheckable(True)
        btnOrigen.setStyleSheet(
            """
        QPushButton {background:rgb(200,200,200); color: black;} 
        QPushButton::checked{background:rgb(255, 0, 0); color: white;}
            """
        )
        self.setCellWidget(posFila, Columna.ORIGEN, btnOrigen)

        # poner nombre del archivo
        item = QTableWidgetItem(path)
        self.setItem(posFila, Columna.ARCHIVO, item)

        # poner fecha de produccion
        item = QTableWidgetItem(fechaProduccion.strftime("%Y-%m-%d %H:%M"))
        self.setItem(posFila, Columna.FECHA, item)

        # poner boton seleccionar para copia
        btnCopia = QPushButton("Poner a copia")
        btnCopia.setCheckable(True)
        btnCopia.setStyleSheet(
            """
        QPushButton {background:rgb(200,200,200); color: black;} 
        QPushButton::checked{background:rgb(0, 255, 0); color: white;}
            """
        )
        self.setCellWidget(posFila, Columna.SELECCIONADO, btnCopia)

    def checkUnique(self, path):
        for row in range(self.rowCount()):
            item = self.item(row, 0)
            if item is not None and item.text() == path:
                # Duplicate found
                return False
        return True

    def ordenar(self):
        pass
        # self.sortByColumn()
        # self.setFirstOrigen()
        # self.setAllSeleccionados()}

    # def setOrigen(self):
    #     selectionModel = self.selectionModel()
    #     if selectionModel is None:
    #         return
    #     first = selectionModel.selectedIndexes()
    #     if len(first) == 0:
    #         return
    #     first = first[0]

    #     for column in range(self.columnCount()):
    #         item = self.item(first.row(), column)
    #         if item is not None:
    #             item.setBackground(QColor("green"))
