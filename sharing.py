import socket
import time

import cv2 as cv
from PySide6 import QtCore
from PySide6.QtCore import QObject, Signal

from capture import Capture


class Sharing(QObject):
    image_received = Signal(bytes)

    def __init__(self) -> None:
        super().__init__()
        self.port = 12345

    @QtCore.Slot()
    def share(self):
        fps = 30
        frameTime = 1.0 / fps
        parameters = [int(cv.IMWRITE_JPEG_QUALITY), 50]

        self.capture = Capture()

        with socket.socket() as s:
            s.bind(("", self.port))
            s.listen()
            con, addr = s.accept()
            with con:
                con.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                while True:
                    startTime = time.time()
                    img = self.capture.encode(self.capture.screen(), parameters)
                    header = int(img[1].size).to_bytes(8, byteorder="big")
                    con.send(header)

                    con.sendall(img[1].tobytes())

                    elapsedTime = time.time() - startTime
                    timeToSleep = frameTime - elapsedTime
                    if timeToSleep > 0:
                        time.sleep(timeToSleep)

    @QtCore.Slot()
    def mirror(self):
        with socket.socket() as s:
            s.connect(("192.168.1.68", self.port))
            while True:
                buf = b""
                recvd = 0
                while recvd < 8:
                    data = s.recv(8 - recvd)
                    if not data:
                        print("Lost connection")
                        return
                    buf += data
                    recvd = len(buf)
                imgSize = int.from_bytes(buf, "big")
                buf = b""
                recvd = 0
                while recvd < imgSize:
                    data = s.recv(imgSize - recvd)
                    if not data:
                        print("Lost connection")
                        return
                    buf += data
                    recvd = len(buf)
                self.image_received.emit(buf)


if __name__ == "__main__":
    screenShare = Sharing()
    match input("Select mode:\n-[S]hare\n-[M]irror").lower():
        case "s":
            screenShare.share()
        case "m":
            screenShare.mirror()
