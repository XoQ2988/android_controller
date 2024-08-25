import os
from time import sleep as wait

from android_controller import Controller

adb = os.path.join(os.getcwd(), "assets", "adb.exe")
scrcpy = os.path.join(os.getcwd(), "assets", "scrcpy.exe")

controller = Controller(adb)
device = controller.getDevice()

# Retrieve and display device information
print(device)

# Close to home menu
controller.swipe((device.width / 2, device.height - 1), (device.width / 2, (device.height / 16) * 15), 50)
wait(0.25)
controller.swipe((device.width / 2, (device.height / 5) * 3), (device.width / 2, (device.height / 5) * 2), 100)

# Tap and type in search bar
wait(0.25)
controller.tap((device.width / 2, device.height / 14))
wait(0.25)
controller.type_text("Hello, World!")

# Take a screenshot
controller.screenshot("scr.png")

# Set up streaming
controller.scrcpy_path = scrcpy
controller.stream()
