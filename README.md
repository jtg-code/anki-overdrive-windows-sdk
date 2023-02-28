# Anki Overdrive Windows SDK

## [Support us](https://www.buymeacoffee.com/AnkiOverdrive)

## Prologue
The following library is based off Python 3.11 and with the usage of the [bleak](https://github.com/hbldh/bleak) bluetooth library and [asyncio](https://github.com/python/asyncio/tree/master).
Julius and yours truly have decided to program the library because there wasn't an anki overdrive sdk for the windows usage.

## Installation
1. Install Python 3.11 (I'd recommend 3.9) if you don't already have Python installed
2. Run the following commands:
```
pip install bleak
pip install asyncio
```
3. Have fun and I'd suggest to ```await _functions()```

## Example

### async def myDef():
```
from anki_sdk.cars import *
from anki_sdk.controller import *
import anki_sdk.utils as utils
import time

async def myDef():
    test_car = carClass("XX:XX:XX:XX:XX:XX")
    test_car_controller = controllerClass(test_car)
    await test_car._connect()
    await test_car_controller._setSpeed(1000, 1000)
    time.sleep(3)
    await test_car._disconnect()

asyncio.run(myDef())
```

### def myDef():
```
from anki_sdk.cars import *
from anki_sdk.controller import *
import anki_sdk.utils as utils
import time

async def myDef():
    test_car = carClass("XX:XX:XX:XX:XX:XX")
    test_car_controller = controllerClass(test_car)
    test_car.connect()
    test_car_controller.setSpeed(1000, 1000)
    time.sleep(3)
    test_car.disconnect()

myDef()
```
