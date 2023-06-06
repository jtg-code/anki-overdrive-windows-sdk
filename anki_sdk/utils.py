"""Utils file from anki sdk"""
import asyncio
import bleak
try:
    from anki_sdk.exceptions import NotFoundError
except ModuleNotFoundError:
    from exceptions import NotFoundError

async def async_scanner(active: bool = True):
    """Scan for cars

    Args:
        active (bool): Only search for active cars. Defaults to True.

    Returns:
        list: list with all Anki Overdrive vehicle MAC-address
    """
    device_list = await bleak.BleakScanner.discover()
    result: list = []
    if len(device_list) == 0:
        raise NotFoundError()
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

def decodeCarname(manufacturerData):
    carId = manufacturerData[1]
    carnames = {
        0: 'x52',
        8: 'Groundshock',
        9: 'Skull',
        10: 'Thermo',
        11: 'Nuke',
        12: 'Guardian',
        14: 'Bigbang',
        15: 'Free Wheel',
        16: 'x52',
        17: 'x52 Ice',
        18: 'MXT',
        19: 'Ice Charger',
    }

    if carId in carnames:
        return carnames[carId]
    else:
        return "Unknown"


async def async_get_data(address: str):
    """Get manufacturer data from car

    Args:
        address (str): Car MAC-address

    Returns:
        dict: Data from the car
    """
    scanner = bleak.BleakScanner()
    car_data = await scanner.find_device_by_address(address)
    data_table: list = car_data.metadata["manufacturer_data"][61374]
    value = bytearray(data_table)
    car_name = decodeCarname(value)
    answer = {
        "name": car_name,
        "manufacturer_data": value
    }
    return answer

def get_data(address: str):
    """Get manufacturer data from car

    Args:
        address (str): Car MAC-address

    Returns:
        dict: Data from the car
    """
    value: dict = asyncio.run(async_get_data(address))

    return value





if __name__ == "__main__":
    get_data("F8:21:8E:B8:E0:85")
