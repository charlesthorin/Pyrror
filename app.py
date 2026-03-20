import faulthandler
import sys

import numpy as np
from numpy.typing import ArrayLike
from PySide6 import QtCore, QtGui, QtWidgets

from capture import Capture

faulthandler.enable()


class MyWidget(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.capture: Capture = Capture()

        # QLabel contenat l'image dupliquée
        self.imageContainer = QtWidgets.QLabel()

        # QTimer appelant la capture à interval régulier
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000 / 30)
        self.timer.timeout.connect(self.stream)

        self.button = QtWidgets.QPushButton("Stream")
        self.button.clicked.connect(self.timer.start)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.imageContainer)
        self.layout.addWidget(self.button)

        self.resize(640, 480)

    @QtCore.Slot()
    def display_image(self, pixmap: QtGui.QPixmap):
        self.imageContainer.setPixmap(
            pixmap.scaled(
                self.imageContainer.size(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
        )

    @QtCore.Slot()
    def stream(self) -> ArrayLike:
        screenshot = self.capture.screen()
        success, imgData = self.capture.encode(screenshot)
        imgData = imgData.tobytes()
        if success:
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(imgData)
            self.display_image(pixmap)


def start():
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.show()

    sys.exit(app.exec())
