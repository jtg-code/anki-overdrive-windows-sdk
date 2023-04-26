import bleak
import asyncio
from anki_sdk.exceptions import *

async def _scanner(active: bool = True) -> list:
    deviceList = await bleak.BleakScanner.discover()
    result: list = []
    for device in deviceList:
        if device.name != None:
            if "Drive" in device.name:
                if active == True:
                    if not "P" in device.name:
                        result.append(device.address)
                else:
                    result.append(device.address)
                    
    return result
        
def scanner(active: bool = True) -> list:
    return asyncio.run(_scanner(active))

async def _getData(address: str) -> str:
    deviceList = await bleak.BleakScanner.discover()
    carData: list = [device for device in deviceList if device.address == address]
    if len(carData) <= 0:
        raise NotFoundError("Address not valid")
    dataTable: list = carData[0].metadata["manufacturer_data"]
    data: list = [data for data in dataTable]
    return str(data[0])
    

def getData(address: str) -> str:
    return asyncio.run(_getData(address))


if __name__ == "__main__":
    getData("dasdsa")