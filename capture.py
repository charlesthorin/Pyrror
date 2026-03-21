import cv2 as cv
import numpy as np
from mss.linux import MSS


class Capture:
    def __init__(self) -> None:
        self.mss = MSS()

    def screen(self):
        monitor = self.mss.monitors[1]
        screenshot = self.mss.grab(monitor)
        return np.array(screenshot)

    def encode(self, screenshot, parameters):
        return cv.imencode(".jpg", screenshot, parameters)


if __name__ == "__main__":
    capture = Capture()
    img = capture.screen()
    cv.imshow("test", img)
    if cv.waitKey(0) == ord("q"):
        cv.destroyAllWindows()
