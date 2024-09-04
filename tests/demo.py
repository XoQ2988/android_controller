import os
from time import sleep as wait
import logging
import asyncio  # Import asyncio for asynchronous execution

from src.android_controller import Controller

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Paths to ADB and scrcpy executables
adb = os.path.join(os.path.abspath('.'), "assets", "adb.exe")
scrcpy = os.path.join(os.path.abspath('.'), "assets", "scrcpy.exe")

async def main():
    # Initialize the Controller
    controller = Controller(adb_path=adb, scrcpy_path=scrcpy)

    # Retrieve and display device information
    device = controller.getDevice()
    logging.info(f"Connected to device:\n{device}")

    # Swipe gesture to close to the home menu
    controller.swipe(
        start=(int(device.width / 2), int(device.height - 1)),
        end=(int(device.width / 2), int((device.height / 16) * 15)),
        duration=50
    )
    wait(0.25)
    controller.swipe(
        start=(int(device.width / 2), int((device.height / 5) * 3)),
        end=(int(device.width / 2), int((device.height / 5) * 2)),
        duration=100
    )

    # Tap on the search bar and type text
    wait(0.25)
    controller.tap((int(device.width / 2), int(device.height / 14)))
    wait(0.25)
    controller.type_text("Hello, World!")

    # Take a screenshot and save it
    screenshot_path = "scr.png"
    controller.screenshot(screenshot_path)
    logging.info(f"Screenshot saved to {screenshot_path}")

    # Set up streaming (will start scrcpy)
    await controller.stream(max_fps=30, bit_rate="8M", rotate=False, always_on_top=True, disable_screensaver=True, no_audio=True)

# Run the main function using asyncio
asyncio.run(main())
