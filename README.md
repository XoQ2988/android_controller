# Android Device Controller

The **Android Device Controller** is a Python-based utility for controlling and interacting with Android devices via ADB. This project provides a convenient set of tools for automating tasks such as taking screenshots, simulating touch gestures, typing text, streaming the device's screen to your computer, and retrieving detailed device information.

## Features

- **Retrieve Device Information**: Get detailed information about the connected Android device.
- **Execute Shell Commands**: Run shell commands directly on the device.
- **Screenshot**: Capture and save the current screen of the Android device.
- **Tap**: Simulate a tap on the device screen at specified coordinates.
- **Swipe**: Simulate a swipe gesture on the device screen from a start to an end point.
- **Type Text**: Simulate typing text on the device.
- **Stream**: Stream the Android device's screen to your computer using `scrcpy`.

## Requirements

- Python 3.x
- ADB (Android Debug Bridge)
- [scrcpy](https://github.com/Genymobile/scrcpy) (for streaming the device's screen, optional)

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/XoQ2988/android_controller.git
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
from android_controller import Controller

# Initialize the controller with the path to the adb executable
controller = Controller(adb_path="/path/to/adb")

# Take a screenshot and save it to a file
controller.screenshot("/path/to/save/screenshot.png")

# Simulate a tap at coordinates (100, 200)
controller.tap((100, 200))

# Simulate a swipe from (100, 200) to (300, 400) over 500ms
controller.swipe((100, 200), (300, 400), duration=500)

# Type text "Hello, World!" on the device
controller.type_text("Hello, World!")

# Stream the device's screen to your computer
controller.scrcpy_path = "/path/to/scrcpy"
controller.stream()

# Retrieve and display device information
device_info = controller.getDevice()
print(device_info)
