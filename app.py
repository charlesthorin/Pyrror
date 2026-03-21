import faulthandler
import sys

import numpy as np
from numpy.typing import ArrayLike
from PySide6 import QtCore, QtGui, QtWidgets

from sharing import Sharing

faulthandler.enable()


class MyWidget(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.screenShare = Sharing()
        self.screenShareThread = QtCore.QThread()

        self.screenShare.moveToThread(self.screenShareThread)
        self.screenShare.image_received.connect(self.display_image)

        # QLabel contenat l'image dupliquée
        self.imageContainer = QtWidgets.QLabel()

        self.streamButton = QtWidgets.QPushButton("Stream")
        self.streamButton.clicked.connect(self.stream)

        self.mirrorButton = QtWidgets.QPushButton("Mirror")
        self.mirrorButton.clicked.connect(self.mirror)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.imageContainer)
        self.layout.addWidget(self.streamButton)
        self.layout.addWidget(self.mirrorButton)

        self.resize(640, 480)

    @QtCore.Slot(bytes)
    def display_image(self, imgData: bytes):
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(imgData)
        self.imageContainer.setPixmap(
            pixmap.scaled(
                self.imageContainer.size(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
        )

    @QtCore.Slot()
    def stream(self):
        self.screenShareThread.started.connect(self.screenShare.share)
        self.screenShareThread.start()

    @QtCore.Slot()
    def mirror(self):
        self.screenShareThread.started.connect(self.screenShare.mirror)
        self.screenShareThread.start()


def start():
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.show()

    sys.exit(app.exec())
