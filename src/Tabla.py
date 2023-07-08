from enum import IntEnum
from PySide6.QtCore import Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QAbstractItemView,
    QHeaderView,
)
from MediaData import getFechaProduccion, updateDateProduction
from datetime import datetime


class Columna(IntEnum):
    # ORIGEN = 0
    ARCHIVO = 0
    FECHA = 1
    # SELECCIONADO = 3


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
        self.horizontalHeader().setSectionResizeMode(
            Columna.ARCHIVO, QHeaderView.Stretch
        )
        self.horizontalHeader().setSectionResizeMode(Columna.FECHA, QHeaderView.Stretch)

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
        # btnOrigen = QPushButton("Poner origen")
        # btnOrigen.setCheckable(True)
        # btnOrigen.setStyleSheet(
        #     """
        # QPushButton {background:rgb(200,200,200); color: black;}
        # QPushButton::checked{background:rgb(255, 0, 0); color: white;}
        #     """
        # )
        # self.setCellWidget(posFila, Columna.ORIGEN, btnOrigen)

        # poner nombre del archivo
        item = QTableWidgetItem(path)
        self.setItem(posFila, Columna.ARCHIVO, item)

        # poner fecha de produccion
        item = QTableWidgetItem(fechaProduccion.strftime("%Y-%m-%d %H:%M"))
        self.setItem(posFila, Columna.FECHA, item)

        # poner boton seleccionar para copia
        # btnCopia = QPushButton("Poner a copia")
        # btnCopia.setCheckable(True)
        # btnCopia.setStyleSheet(
        #     """
        # QPushButton {background:rgb(200,200,200); color: black;}
        # QPushButton::checked{background:rgb(0, 255, 0); color: white;}
        #     """
        # )
        # self.setCellWidget(posFila, Columna.SELECCIONADO, btnCopia)

    def checkUnique(self, path):
        for row in range(self.rowCount()):
            item = self.item(row, 0)
            if item is not None and item.text() == path:
                # Duplicate found
                return False
        return True

    def actualizarFechaTodosConElMasViejo(self):
        path_archivo_fecha_mas_vieja = ""
        fecha_mas_vieja_texto = ""
        fecha_mas_vieja = None
        try:
            # Obtener la fecha más antigua de todas las filas
            for row in range(self.rowCount()):
                item = self.item(row, Columna.FECHA)
                if item is not None:
                    fecha_str = item.text()
                    fecha_actual = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M")
                    if fecha_mas_vieja is None or fecha_actual < fecha_mas_vieja:
                        fecha_mas_vieja = fecha_actual
                        path_archivo_fecha_mas_vieja = self.item(
                            row, Columna.ARCHIVO
                        ).text()

            # Actualizar todas las filas con la fecha más antigua
            if fecha_mas_vieja is not None:
                fecha_mas_vieja_texto = fecha_mas_vieja.strftime("%Y-%m-%d %H:%M")

                for row in range(self.rowCount()):
                    item = self.item(row, Columna.FECHA)
                    if item is not None:
                        print("antes de entrar a updateDateProduction")
                        respuesta_update = updateDateProduction(
                            path_archivo_fecha_mas_vieja,
                            self.item(row, Columna.ARCHIVO).text(),
                        )
                        if respuesta_update is not None:
                            return respuesta_update
                        item.setText(fecha_mas_vieja_texto)

            # Actualizar visualmente la tabla
            self.viewport().update()
        except Exception as err:
            print(err)
            return str(err)
        if fecha_mas_vieja is None:
            return "No hay registros para actualizar"
        return (
            "actualizadas todas las tablas con la informacion del mas viejo: "
            + fecha_mas_vieja_texto
        )

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
