import shlex
import subprocess
from typing import Union

from android_controller.device import Device


class Controller:
    def __init__(self, adb_path):
        self.adb_path = adb_path
        self.scrcpy_path = None

    def screenshot(self, path: str):
        """
            Takes a screenshot of the Android device screen and saves it to the specified output path.

        Args:
            path (str): The file path where the screenshot will be saved.

        Returns:
            str: The output path of the saved screenshot.
        """
        # Prepare the ADB screencap command
        cmd = [self.adb_path, "exec-out", "screencap", "-p"]

        try:
            # Open the output file in binary write mode
            with open(path, "wb") as f:
                # Run the ADB command and write the output to the file
                subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, check=True)

            print(f"Screenshot saved to {path}")
            return path

        except subprocess.CalledProcessError as e:
            print(f"Error taking screenshot: {e.stderr.decode().strip()}")
            return None

    def tap(self, coords: tuple[Union[int, float], Union[int, float]]) -> None:
        """
            Simulates a tap on the device screen at the specified coordinates.

        Args:
            coords (tuple[int, int]): The coordinates (x, y) where the tap should be performed.
        """
        # Convert coordinates to strings
        x, y = map(lambda z: str(int(z)), coords)

        # Prepare the ADB tap command
        cmd = [self.adb_path, "shell", "input", "tap", x, y]

        try:
            # Run the command
            subprocess.run(cmd, check=True)
            print(f"Tap executed at {coords}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing tap: {e}")

    def swipe(self, start: tuple[Union[int, float], Union[int, float]], end: tuple[Union[int, float], Union[int, float]], duration: int = 300) -> None:
        """
            Swipes on the device screen from a start point to an end point.

        Args:
            start (tuple[int, int]): The starting coordinates (x, y).
            end (tuple[int, int]): The ending coordinates (x, y).
            duration (int, optional): Duration of the swipe in milliseconds. Default is 300ms.
        """
        # Convert coordinates to integers and then to strings
        start_x, start_y = map(lambda x: str(int(x)), start)
        end_x, end_y = map(lambda x: str(int(x)), end)
        duration = str(duration)

        # Prepare the ADB swipe command
        cmd = [self.adb_path, "shell", "input", "swipe", start_x, start_y, end_x, end_y, duration]

        try:
            # Run the command
            subprocess.run(cmd, check=True)
            print(f"Swipe executed from {start} to {end} over {duration}ms")
        except subprocess.CalledProcessError as e:
            print(f"Error executing swipe: {e}")

    def type_text(self, text: str) -> None:
        """
        Types the given text on the device screen.

        Args:
            text (str): The text to be typed on the device.
        """
        # Escape special characters for the ADB shell command
        escaped_text = shlex.quote(text)

        # Prepare the ADB command to input text
        cmd = [self.adb_path, "shell", "input", "text", escaped_text]

        try:
            # Run the command
            subprocess.run(cmd, check=True)
            print(f"Text '{text}' typed successfully on the device.")
        except subprocess.CalledProcessError as e:
            print(f"Error typing text on the device: {e}")

    def stream(self):
        subprocess.run([
            self.scrcpy_path,
            #"--max-fps=30",
            "--no-audio",
            "--disable-screensaver",
            "--always-on-top"

        ])

    def shell(self, command: list[str], debug: bool = False) -> str:
        """
        Executes a shell command and returns the output as a string.

        Args:
            :param command: The command to execute as a list of strings.
            :param debug: Whether to print the command to console

        Returns:
            str: The command output as a string.
        """
        try:
            result = subprocess.run([self.adb_path, "shell"] + command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    text=True, check=True)
            if debug:
                print(f"Executed command \"{' '.join(command)}\"")

            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error executing command \"{' '.join(command)}\": {e.stderr.strip()}")
            return ""

    def getDevice(self):
        """
            Retrieves the device information including name, screen width, and height.

        Returns:
            Device: An instance of the Device dataclass
        """

        # Get device properties
        device_name = self.shell(["getprop", "ro.boot.em.model"])
        screen_info = self.shell(["getprop", "service.secureui.screeninfo"])
        android_version = self.shell(["getprop", "ro.build.version.release"])
        sdk_version = self.shell(["getprop", "ro.build.version.sdk"])
        model = self.shell(["getprop", "ro.product.model"])
        manufacturer = self.shell(["getprop", "ro.product.manufacturer"])
        build_id = self.shell(["getprop", "ro.build.id"])
        cpu_abi = self.shell(["getprop", "ro.product.cpu.abi"])
        screen_density_info = self.shell(["wm", "density"])
        serial_number = self.shell(["getprop", "ro.boot.serialno"])
        imei = self.shell(["service", "call", "iphonesubinfo", "1"])
        network_operator = self.shell(["getprop", "gsm.operator.alpha"])

        # Parse screen size
        if screen_info:
            try:
                width, height = map(int, screen_info.split("x"))
            except ValueError:
                print(f"Error parsing screen info: {screen_info}")
                width, height = 0, 0
        else:
            width, height = 0, 0

        # Extract screen density from wm density output
        screen_density = 0
        for line in screen_density_info.splitlines():
            if "Physical density:" in line:
                try:
                    screen_density = int(line.split(":")[1].strip())
                except ValueError:
                    print(f"Error parsing screen density: {line}")
                    screen_density = 0

        return Device(
            name=device_name,
            width=width,
            height=height,
            android_version=android_version,
            sdk_version=sdk_version,
            model=model,
            manufacturer=manufacturer,
            build_id=build_id,
            cpu_abi=cpu_abi,
            screen_density=screen_density,
            serial_number=serial_number,
            imei=imei,
            network_operator=network_operator
        )
