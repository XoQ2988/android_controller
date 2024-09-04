from dataclasses import dataclass

@dataclass
class Device:
    device_name: str
    width: int
    height: int
    android_version: str
    sdk_version: str
    model: str
    manufacturer: str
    build_id: str
    cpu_abi: str
    screen_density: int
    serial_number: str
    imei: str
    network_operator: str

    def __str__(self):
        return (f"Device Name: {self.device_name}\n"
                f"Model: {self.manufacturer} {self.model}\n"
                f"Android Version: {self.android_version} (SDK: {self.sdk_version})\n"
                f"Build ID: {self.build_id}\n"
                f"CPU ABI: {self.cpu_abi}\n"
                f"Screen: {self.width}x{self.height} @ {self.screen_density}dpi\n"
                f"Serial Number: {self.serial_number}\n"
                f"IMEI: {self.imei}\n"
                f"Network Operator: {self.network_operator}")
