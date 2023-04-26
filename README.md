# Anki Overdrive windows SDK

## installation
1. Download the newest release</li>
2. Extract the ```anki_sdk``` directory
3. Run ```pip install -r requirements.txt``` <b>OR</b> run the ```Setup.py```


## Functions
```python
import anki_sdk.cars as cars
import anki_sdk.controller as controller
import anki_sdk.utils as utils

# Utils
carList: list = utils.scanner(active: bool) # active: Only cars which are turned on -> returns an anki overdrive MAC-address list
carData: str = utils.getData(address: str) # active: The MAC-address of the vehicle -> returns the manufacturer_data

# Init
myCar: cars.carClass = cars.carClass("XX:XX:XX:XX")
myController: controller.controllerClass = controller.controllerClass(myCar)

# Controller functions
speed, accel = 500, 1000 # Max 1000
myController.setSpeed(speed, accel)

lanes = 3 # Recommend max 3
myController.leftLane(lanes)
myController.rightLane(lanes)

rightLane = 44.5 # One lane right
leftLane = -44.5 # One lane left
myController.changeLane(rightLane)
myController.changeLane(leftLane)

@myCar.notifyCallback(type=cars.Receive.trackChange) # Gets triggered every new track
def newTrack(sender, data):
    print("New track")
    
    
@myCar.notifyCallback(type=cars.Receive.specialTrack) # Gets triggered every special track
def specialTrack(sender, data):
    print("Special track")
    
print(myCar.ping()) # Prints the car ping
```
