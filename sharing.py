import socket
from sys import byteorder

from capture import Capture


class Sharing:
    def __init__(self) -> None:
        self.port = 12345
        self.capture = Capture()

    def share(self):
        with socket.socket() as s:
            s.bind(("", self.port))
            s.listen()
            con, addr = s.accept()
            with con:
                while True:
                    img = self.capture.encode(self.capture.screen())
                    header = int(img[1].size).to_bytes(8, byteorder="big")
                    print("Image size: ", int(img[1].size))
                    con.send(header)

                    con.sendall(img[1].tobytes())

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
                print("Image size: ", imgSize)
                buf = b""
                recvd = 0
                while recvd < imgSize:
                    data = s.recv(imgSize - recvd)
                    if not data:
                        print("Lost connection")
                        return
                    buf += data
                    recvd = len(buf)


if __name__ == "__main__":
    screenShare = Sharing()
    match input("Select mode:\n-[S]hare\n[M]irror").lower():
        case "s":
            screenShare.share()
        case "m":
            screenShare.mirror()
