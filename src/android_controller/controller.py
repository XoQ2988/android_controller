import os
import shlex
import subprocess
import logging
from typing import Union, Optional, Tuple, List
import re
import asyncio

from src.android_controller.device import Device

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Controller:
    def __init__(self, adb_path: str = None, scrcpy_path: str = None) -> None:
        """
        Initializes the Controller with the specified adb and optionally scrcpy paths.

        Args:
            adb_path (str, optional): The path to the adb executable. Default is None.
            scrcpy_path (str, optional): The path to the scrcpy executable. Default is None.

        Raises:
            ValueError: If the adb or scrcpy paths are invalid.
        """
        self.adb_path = adb_path or self._find_executable("adb")
        self.scrcpy_path = scrcpy_path or self._find_executable("scrcpy")

        if not os.path.isfile(self.adb_path):
            raise ValueError(f"Invalid adb path: {self.adb_path}. Please provide a valid adb executable path.")

        if self.scrcpy_path and not os.path.isfile(self.scrcpy_path):
            raise ValueError(f"Invalid scrcpy path: {self.scrcpy_path}. Please provide a valid scrcpy executable path.")

        logging.info(f"Controller initialized with adb path: {self.adb_path}")
        if self.scrcpy_path:
            logging.info(f"Controller initialized with scrcpy path: {self.scrcpy_path}")
        else:
            logging.warning("Scrcpy path not provided, streaming will be unavailable.")

    def _find_executable(self, name: str) -> Optional[str]:
        """
        Tries to find the specified executable in common installation directories.

        Args:
            name (str): The name of the executable to find.

        Returns:
            str: The full path to the executable if found, else None.
        """
        common_paths = ["/usr/bin", "/usr/local/bin", "C:\\Program Files\\", "C:\\Program Files (x86)\\"]

        for path in common_paths:
            executable = os.path.join(path, name)
            if os.path.isfile(executable):
                return executable

        logging.warning(f"Executable {name} not found in common directories.")
        return None

    async def _run_command(self, cmd: List[str]) -> tuple[str, str]:
        """
        Runs a shell command asynchronously and returns the result.

        Args:
            cmd (list[str]): The command to execute.

        Returns:
            subprocess.CompletedProcess: The result of the command execution.
        """
        try:
            result = await asyncio.create_subprocess_exec(
                *cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            stdout, stderr = await result.communicate()

            if result.returncode != 0:
                logging.error(f"Command {' '.join(cmd)} failed with error: {stderr.decode().strip()}")
            return stdout.decode().strip(), stderr.decode().strip()
        except Exception as e:
            logging.error(f"Error running command {' '.join(cmd)}: {e}")
            return "", str(e)

    def screenshot(self, path: str) -> Optional[str]:
        """
        Takes a screenshot of the Android device screen and saves it to the specified output path.

        Args:
            path (str): The file path where the screenshot will be saved.

        Returns:
            str: The output path of the saved screenshot.
        """
        cmd = [self.adb_path, "exec-out", "screencap", "-p"]
        try:
            with open(path, "wb") as f:
                subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, check=True)
            logging.info(f"Screenshot saved to {path}")
            return path
        except subprocess.CalledProcessError as e:
            logging.error(f"Error taking screenshot: {e.stderr.decode().strip()}")
            return None

    def tap(self, coords: Tuple[Union[int, float], Union[int, float]]) -> None:
        """
        Simulates a tap on the device screen at the specified coordinates.

        Args:
            coords (tuple[int, int]): The coordinates (x, y) where the tap should be performed.
        """
        x, y = map(lambda z: str(int(z)), coords)
        cmd = [self.adb_path, "shell", "input", "tap", x, y]
        try:
            subprocess.run(cmd, check=True)
            logging.info(f"Tap executed at {coords}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error executing tap: {e}")

    def swipe(self, start: Tuple[Union[int, float], Union[int, float]], end: Tuple[Union[int, float], Union[int, float]], duration: int = 300) -> None:
        """
        Swipes on the device screen from a start point to an end point.

        Args:
            start (tuple[int, int]): The starting coordinates (x, y).
            end (tuple[int, int]): The ending coordinates (x, y).
            duration (int, optional): Duration of the swipe in milliseconds. Default is 300ms.
        """
        start_x, start_y = map(lambda x: str(int(x)), start)
        end_x, end_y = map(lambda x: str(int(x)), end)
        duration = str(duration)
        cmd = [self.adb_path, "shell", "input", "swipe", start_x, start_y, end_x, end_y, duration]
        try:
            subprocess.run(cmd, check=True)
            logging.info(f"Swipe executed from {start} to {end} over {duration}ms")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error executing swipe: {e}")

    def type_text(self, text: str) -> None:
        """
        Types the given text on the device screen.

        Args:
            text (str): The text to be typed on the device.
        """
        escaped_text = shlex.quote(text)
        cmd = [self.adb_path, "shell", "input", "text", escaped_text]
        try:
            subprocess.run(cmd, check=True)
            logging.info(f"Text '{text}' typed successfully on the device.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error typing text on the device: {e}")

    async def stream(self, max_fps: int = 30, bit_rate: str = "8M",
                     rotate: bool = False, always_on_top: bool = True, disable_screensaver: bool = True,
                     no_audio: bool = True) -> None:
        """
        Streams the Android device screen to the computer using scrcpy with customizable options.

        Args:
            max_fps (int, optional): The maximum frame rate to stream at. Default is 30 fps.
            bit_rate (str, optional): The bit rate of the video stream. Default is '8M' (8Mbps).
            rotate (bool, optional): Whether to rotate the device screen. Default is False.
            always_on_top (bool, optional): Whether the streaming window should always be on top. Default is True.
            disable_screensaver (bool, optional): Whether to disable the screensaver while streaming. Default is True.
            no_audio (bool, optional): Whether to disable audio in the stream. Default is True.
        """
        if not self.scrcpy_path:
            logging.error("Scrcpy path not provided, streaming unavailable.")
            return

        cmd = [self.scrcpy_path]
        options = [
            ("--max-fps", str(max_fps)) if max_fps else None,
            ("--video-bit-rate", bit_rate) if bit_rate else None,
            ("--audio-bit-rate", bit_rate) if bit_rate else None,
            "--rotate" if rotate else None,
            "--always-on-top" if always_on_top else None,
            "--disable-screensaver" if disable_screensaver else None,
            "--no-audio" if no_audio else None
        ]
        cmd += [item for sublist in options if sublist for item in
                (sublist if isinstance(sublist, tuple) else (sublist,))]

        try:
            await self._run_command(cmd)
            logging.info(f"Streaming started with options: {cmd[1:]}")
        except Exception as e:
            logging.error(f"Error starting stream: {e}")

    def shell(self, command: List[str], debug: bool = False) -> str:
        """
        Executes a shell command and returns the output as a string.

        Args:
            command (list[str]): The command to execute as a list of strings.
            debug (bool, optional): Whether to print the command to the console.

        Returns:
            str: The command output as a string.
        """
        try:
            result = subprocess.run([self.adb_path, "shell"] + command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    text=True, check=True)
            if debug:
                logging.info(f"Executed command: {' '.join(command)}")
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logging.error(f"Error executing command \"{' '.join(command)}\": {e.stderr.strip()}")
            return ""

    def getDevice(self) -> Device:
        """
        Retrieves the device information including name, screen width, and height.

        Returns:
            Device: An instance of the Device dataclass.
        """
        def extract_screen_info(screen_info: str) -> Tuple[int, int]:
            match = re.search(r'(\d+)x(\d+)', screen_info)
            return (int(match.group(1)), int(match.group(2))) if match else (0, 0)

        def extract_screen_density(density_info: str) -> int:
            match = re.search(r'Physical density:\s*(\d+)', density_info)
            return int(match.group(1)) if match else 0

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

        width, height = extract_screen_info(screen_info)
        screen_density = extract_screen_density(screen_density_info)

        return Device(
            device_name=device_name, width=width, height=height,
            android_version=android_version, sdk_version=sdk_version,
            model=model, manufacturer=manufacturer, build_id=build_id,
            cpu_abi=cpu_abi, screen_density=screen_density,
            serial_number=serial_number, imei=imei, network_operator=network_operator
        )
