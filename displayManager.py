import subprocess


class VirtualDisplayManager:
    def __init__(self, output_name="HDMI-0", primary_output="DP-0"):
        self.output_name = output_name
        self.primary_output = primary_output
        self.mode_name = "1920x1080_dummy"

    def start(self):
        modeline = [
            "173.00",
            "1920",
            "2048",
            "2248",
            "2576",
            "1080",
            "1083",
            "1088",
            "1120",
            "-hsync",
            "+vsync",
        ]

        subprocess.run(
            ["xrandr", "--newmode", self.mode_name] + modeline, capture_output=True
        )
        subprocess.run(
            ["xrandr", "--addmode", self.output_name, self.mode_name],
            capture_output=True,
        )
        subprocess.run(
            [
                "xrandr",
                "--output",
                self.output_name,
                "--mode",
                self.mode_name,
                "--right-of",
                self.primary_output,
            ],
            capture_output=True,
        )

    def stop(self):
        subprocess.run(
            ["xrandr", "--output", self.output_name, "--off"], capture_output=True
        )
