import cv2 as cv
import numpy as np
from mss.linux import MSS
from mss.screenshot import ScreenShot


class Capture:
    def __init__(self) -> None:
        self.mss = MSS()

    def screen(self):
        with self.mss as sct:
            monitor = sct.monitors[1]
            screen = sct.grab(monitor)
            return np.array(screen)

    def encode(self, screenshot: np.typing.ArrayLike):
        return cv.imencode(".jpg", screenshot)


if __name__ == "__main__":
    capture = Capture()
    img = capture.screen()
    cv.imshow("test", img)
    if cv.waitKey(0) == ord("q"):
        cv.destroyAllWindows()
