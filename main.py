import subprocess
import sys

from displayManager import VirtualDisplayManager

if __name__ == "__main__":
    dpManager = VirtualDisplayManager("HDMI-0", "DP-0")

    try:
        dpManager.start()
        subprocess.run([sys.executable, "app.py"])
    finally:
        dpManager.stop()
