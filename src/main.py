import sys
import PySide6
from PySide6 import QtCore, QtGui, QtWidgets
import PySide6.QtGui

from Tabla import Tabla

# Prints PySide6 version
print(PySide6.__version__)

# Prints the Qt version used to compile PySide6
print(PySide6.QtCore.__version__)


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(750, 300)
        self.setAcceptDrops(True)

        buttons_layout = self.construirBotones()

        # construccion ventana
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.textoInicio = self.textoGrande("Arrastre los archivos aqui")
        self.textoInformacion = QtWidgets.QLabel("hola")
        self.textoInformacion.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        # Crear un QScrollArea para la etiqueta de texto
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.textoInformacion)
        scroll_area.setFixedHeight(150)

        # construir tabla
        self.tabla = Tabla()
        self.tabla.setVisible(False)
        self.tabla.RowCountChanged.connect(self.onRowCountChanged)
        # conectar botones a tabla
        self.btnLimpiarTodo.clicked.connect(self.onLimpiarTodo)

        self.mainLayout.addWidget(self.tabla)
        self.mainLayout.addWidget(self.textoInicio)
        self.mainLayout.addWidget(scroll_area)
        self.mainLayout.addLayout(buttons_layout)

    def onLimpiarTodo(self):
        self.tabla.removeAllRows()
        self.textoInformacion.setText("Limpio")

    def onRowCountChanged(self, cant):
        if cant == 0:
            self.tabla.setVisible(False)
            self.textoInicio.setVisible(True)
        else:
            self.tabla.setVisible(True)
            self.textoInicio.setVisible(False)

    def textoGrande(self, text: str = "") -> QtWidgets.QLabel:
        label = QtWidgets.QLabel(text if text else "No hay texto provisto")
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 24px; font-weight: bold;")
        return label

    def construirBotones(self):
        self.button_layout = QtWidgets.QHBoxLayout()

        self.btnConfirmar = QtWidgets.QPushButton("Confirmar")
        self.btnSeleccionarTodos = QtWidgets.QPushButton("Seleccionar todos")
        self.btnDeseleccionarTodos = QtWidgets.QPushButton("Deseleccionar todos")
        self.btnLimpiarTodo = QtWidgets.QPushButton("Limpiar Todo")
        self.btnLimpiarSeleccionado = QtWidgets.QPushButton("Limpiar seleccionado")

        self.button_layout.addWidget(self.btnConfirmar)
        self.button_layout.addWidget(self.btnSeleccionarTodos)
        self.button_layout.addWidget(self.btnDeseleccionarTodos)
        self.button_layout.addWidget(self.btnLimpiarTodo)
        self.button_layout.addWidget(self.btnLimpiarSeleccionado)
        return self.button_layout

    def dragEnterEvent(self, event):
        self.dragEnterEventText = self.textoInicio.text()
        if event.mimeData().hasUrls():
            file_urls = event.mimeData().urls()
            num_files = str(len(file_urls))
            self.textoInicio.setText("Numero de archivos: " + num_files)
            event.acceptProposedAction()

    def dragLeaveEvent(self, event) -> None:
        self.textoInicio.setText(self.dragEnterEventText)
        event.accept()

    def dropEvent(self, event):
        self.textoInicio.setText(self.dragEnterEventText)
        if event.mimeData().hasUrls():
            # Obtener la lista de URLs de los archivos arrastrados y soltados
            urls = event.mimeData().urls()
            lista_archivos = []
            # Procesar los archivos
            for url in urls:
                # Convertir la URL en una ruta de archivo local
                file_path = url.toLocalFile()
                # Aquí puedes realizar las acciones necesarias con el archivo
                print("Archivo arrastrado y soltado:", file_path)
                lista_archivos.append(file_path)
            self.construirTabla(lista_archivos)
            event.acceptProposedAction()

    def construirTabla(self, listaPath: list[str]):
        for path in listaPath:
            rta = self.tabla.addRow(path)
            if rta is not None:
                self.textoInformacion.setText(self.textoInformacion.text() + "\n" + rta)

        self.tabla.ordenar()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainWidget()
    widget.resize(900, 500)
    widget.show()

    sys.exit(app.exec())
