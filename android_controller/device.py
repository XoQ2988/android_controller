from dataclasses import dataclass


@dataclass
class Device:
    name: str
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
        return f"{self.name} Android {self.android_version} (SN: {self.serial_number})"