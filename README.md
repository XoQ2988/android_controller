# PyDroidCTRL

The **Android Device Controller** is a Python-based utility for controlling and interacting with Android devices via ADB. This project provides a convenient set of tools for automating tasks such as taking screenshots, simulating touch gestures, typing text, streaming the device's screen to your computer, and retrieving detailed device information.

## Features

- **Retrieve Device Information**: Get detailed information about the connected Android device.
- **Execute Shell Commands**: Run shell commands directly on the device.
- **Screenshot**: Capture and save the current screen of the Android device.
- **Tap**: Simulate a tap on the device screen at specified coordinates.
- **Swipe**: Simulate a swipe gesture on the device screen from a start to an end point.
- **Type Text**: Simulate typing text on the device.
- **Stream**: Stream the Android device's screen to your computer using `scrcpy` (now fully asynchronous).

## Requirements

- Python 3.x
- ADB (Android Debug Bridge)
- [scrcpy](https://github.com/Genymobile/scrcpy) (for streaming the device's screen, optional)

## Installation

1. **Clone the repository**:

    ```bash
    pip install PyDroidCTRL
    cd android_controller
    ```

2. **Install required dependencies** (if any):

    ```bash
    pip install -r requirements.txt
    ```

3. **Ensure ADB is installed** and accessible from your system's PATH. You can download ADB from the [official Android website](https://developer.android.com/studio/releases/platform-tools).

4. **Ensure `scrcpy` is installed** for screen streaming functionality. You can find installation instructions for `scrcpy` [here](https://github.com/Genymobile/scrcpy).

## Usage

Create an instance of the `Controller` class with the path to the ADB executable. Then use the provided methods to interact with the device.

### Example

```python
import os
import asyncio
from android_controller import Controller

# Define paths to the adb and scrcpy executables
adb_path = os.path.join(os.path.abspath('.'), "assets", "adb.exe")
scrcpy_path = os.path.join(os.path.abspath('.'), "assets", "scrcpy.exe")

async def main():
    # Initialize the controller with the paths to adb and scrcpy executables
    controller = Controller(adb_path=adb_path, scrcpy_path=scrcpy_path)

    # Retrieve and display device information
    device = controller.getDevice()
    print(device)

    # Simulate a swipe to the home menu
    controller.swipe(
        start=(device.width // 2, device.height - 1),
        end=(device.width // 2, (device.height // 16) * 15),
        duration=50
    )
    
    # Add a slight delay between gestures
    await asyncio.sleep(0.25)

    controller.swipe(
        start=(device.width // 2, (device.height // 5) * 3),
        end=(device.width // 2, (device.height // 5) * 2),
        duration=100
    )

    # Tap on the search bar and type text
    await asyncio.sleep(0.25)
    controller.tap((device.width // 2, device.height // 14))
    await asyncio.sleep(0.25)
    controller.type_text("Hello, World!")

    # Take a screenshot and save it to a file
    screenshot_path = "scr.png"
    controller.screenshot(screenshot_path)
    print(f"Screenshot saved to {screenshot_path}")

    # Stream the device's screen to your computer
    await controller.stream(max_fps=30, bit_rate="8M", rotate=False, always_on_top=True, disable_screensaver=True, no_audio=True)

# Run the main function using asyncio
asyncio.run(main())
```