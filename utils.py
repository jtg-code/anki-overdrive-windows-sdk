import bleak as b
import asyncio
import time as t
import struct

async def _scanner(active: bool):
    carList = []
    devices = await b.BleakScanner.discover()
    for device in devices:
        if "Drive" in str(device):
            if active == False:
                carList.append(device)
            elif active == True and not "P" in str(device):
                carList.append(device)
            #print(device)
    return carList

def scanner(active: bool):
    scannerloop = asyncio.get_event_loop()
    carlist = scannerloop.run_until_complete(_scanner(active))
    return carlist
