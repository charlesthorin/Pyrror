import cv2
import numpy as np
from mss.linux import MSS as mss


class Capture:
    def __init__(self) -> None:
        self.mss = mss()

    def start(self):
        with self.mss as sct:
            monitor = sct.monitors[1]

            while True:
                screen = sct.grab(monitor)
                img = np.array(screen)
                cv2.imshow("Monitor #1", img)
                if cv2.waitKey(1) == ord("q"):
                    break

        cv2.destroyAllWindows()


if __name__ == "__main__":
    capture = Capture()
    capture.start()
