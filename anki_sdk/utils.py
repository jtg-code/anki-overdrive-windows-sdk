"""Utils file from anki sdk"""
import asyncio
import bleak
from anki_sdk.exceptions import NotFoundError


async def async_scanner(active: bool = True):
    """Scan for cars

    Args:
        active (bool): Only search for active cars. Defaults to True.

    Returns:
        list: list with all Anki Overdrive vehicle MAC-address
    """
    device_list = await bleak.BleakScanner.discover()
    result: list = []
    for device in device_list:
        if device.name is not None:
            if "Drive" in device.name:
                if active:
                    if not "P" in device.name:
                        result.append(device.address)
                else:
                    result.append(device.address)
    return result

def scanner(active: bool = True):
    """Scan for cars

    Args:
        active (bool): Only search for active cars. Defaults to True.

    Returns:
        list: list with all Anki Overdrive vehicle MAC-address
    """
    value: list = asyncio.run(async_scanner(active))
    return value

async def async_get_data(address: str):
    """Get manufacturer data from car

    Args:
        address (str): Car MAC-address

    Returns:
        bytes: list with all Anki Overdrive vehicle MAC-address
    """
    device_list = await bleak.BleakScanner.discover()
    car_data: list = [device for device in device_list if device.address == address]
    if len(car_data) <= 0:
        raise NotFoundError("Address not valid")
    data_table: list = car_data[0].metadata["manufacturer_data"]
    data: list = list(data_table)
    value: bytes = data_table[data[0]]
    return value

def get_data(address: str):
    """Get manufacturer data from car

    Args:
        address (str): Car MAC-address

    Returns:
        bytes: list with all Anki Overdrive vehicle MAC-address
    """
    value: bytes = asyncio.run(async_get_data(address))
    return value

if __name__ == "__main__":
    get_data("F8:21:8E:B8:E0:85")
