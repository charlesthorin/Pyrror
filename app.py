import sys

from PySide6 import QtCore, QtGui, QtWidgets


class MyWidget(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.imageContainer = QtWidgets.QLabel()

        self.button = QtWidgets.QPushButton("Display image")
        self.button.clicked.connect(self.display_image)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.imageContainer)
        self.layout.addWidget(self.button)
        self.resize(640, 480)

    @QtCore.Slot()
    def display_image(self):
        pixmap = QtGui.QPixmap("sample.png")
        self.imageContainer.setPixmap(
            pixmap.scaled(
                self.imageContainer.size(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
        )


def start():
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.show()

    sys.exit(app.exec())
