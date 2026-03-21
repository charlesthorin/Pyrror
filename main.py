import subprocess
import sys

if __name__ == "__main__":
    try:
        subprocess.run([sys.executable, "app.py"])
    finally:
        subprocess.run(["xrandr", "--output", "HDMI-0", "--off"], capture_output=True)
