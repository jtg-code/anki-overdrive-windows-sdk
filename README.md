# Anki Overdrive windows SDK

## Installation
1. Download the newest release</li>
2. Extract the ```anki_sdk``` directory
3. Run ```pip install -r requirements.txt``` <b>OR</b> run ```python setup.py```
4. For update run ```python setup.py --update --upgrade```


## .anki code language
### Syntax
````json
{
    "function": "def",
    "#include utils": "import anki_sdk.utils as utils",
    "#include cars": "import anki_sdk.cars as cars",
    "#include controllers": "import anki_sdk.controllers as controllers",
    "#include api": "import anki_sdk.api as api",
    "new Car": "cars.CarClass",
    "new Controller": "controllers.ControllerClass",
    "#import": "import",
    "#": "@",
    "//": "#",
    "log": "print",
    ".end": "exit()"
}
````

## Default Example
```python
import anki_sdk as sdk
import time

def controll_car(address: str):
    # Create a new car object with the given address
    car = sdk.cars.CarClass(address)
    car.connect()  # Connect to the car
    car.start_notify()  # Start receiving notifications from the car
    controller = sdk.controller.ControllerClass(car)
    print(f"Pong! {car.ping()}ms")  # Print the ping time to the car
    controller.set_speed(500, 500)  # Set the speed of the car
    time.sleep(10)  # Wait for 10 seconds
    controller.left_lane(1.0)  # Move the car to the left lane
    time.sleep(10)  # Wait for 10 seconds
    controller.right_lane(1.0)  # Move the car to the right lane
    time.sleep(10)  # Wait for 10 seconds
    
    # Define a callback function for when a new track is detected
    @car.notifycallback(sdk.cars.Receive.Track.TRACK_CHANGE)
    def new_track(sender, data):
        print("New Track!")
        
    # Define a callback function for when the car crosses the finish line
    @car.notifycallback(sdk.cars.Receive.Track.FINISHLINE)
    def finish_line(sender, data):
        print("Finish!")
        
    # Define a callback function for when a special track is encountered
    @car.notifycallback(sdk.cars.Receive.Track.SPECIAL_TRACK)
    def special_track(sender, data):
        print("Special Track!")
        
    # Define a callback function for when a straight track is detected
    @car.notifycallback(sdk.cars.Receive.Track.STRAIGHT_TRACK)
    def straight_track(sender, data):
        print("New Straight Track!")
        
    # Define a callback function for when a ping response is received
    @car.notifycallback(sdk.cars.Receive.Connection.PING_RESPONSE)
    def ping_response(sender, data):
        print("Ping Response!")
    
    car.stop_notify()  # Stop receiving notifications from the car
    car.disconnect()  # Disconnect from the car
```

## API Example
### Python
#### Client
````python
from anki_sdk import api
# Create the client and establish a connection to the server
client = api.Client("localhost")

# Create a car and get the token
token = client.create_car("AA:BB:CC:DD:EE:FF")
print("Token:", token)

# Set the speed of the car
speed = 500  # Speed value (in millimeters per second)
accel = 1000  # Acceleration value (in millimeters per second squared)
response = client.set_speed(speed, accel)
print("Set Speed Response:", response)

# Make the car switch to the left lane
lanes = 0.5  # Number of lanes to switch (can be a decimal value)
response = client.left_lane(lanes)
print("Left Lane Response:", response)

# Make the car switch to the right lane
lanes = 1.0  # Number of lanes to switch (can be a decimal value)
response = client.right_lane(lanes)
print("Right Lane Response:", response)

# Get a list of available cars
active = True  # Flag to retrieve only active cars
car_list = client.get_cars(active=active)
print("Available Cars:")
for car in car_list:
    print(car)
````

### Javascript
#### Client
````javascript
const { Client } = require("./api/anki_api");

async function main() {
  // Create the client and establish a connection to the server
  const client = new Client("localhost");

  // Create a car and get the token
  const token = await client.create_car("AA:BB:CC:DD:EE:FF");
  console.log("Token:", token);

  // Set the speed of the car
  const setSpeedResponse = await client.set_speed(500);
  console.log("Set Speed Response:", setSpeedResponse);

  // Make the car switch to the left lane
  const leftLaneResponse = await client.left_lane(0.5);
  console.log("Left Lane Response:", leftLaneResponse);

  // Make the car switch to the right lane
  const rightLaneResponse = await client.right_lane(1.0);
  console.log("Right Lane Response:", rightLaneResponse);

  // Get a list of available cars
  const carList = await client.get_cars(true);
  console.log("Available Cars:");
  for (const car of carList) {
    console.log(car);
  }
}
main();
````