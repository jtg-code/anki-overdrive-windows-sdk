# API

## Python
### Server
````python
from anki_sdk import api
# Start API server
server = api.Server("localhost")
````
### Client
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

## Javascript
### Client
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