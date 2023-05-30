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
## C++
### Client
````cpp
#include <iostream>
#include <string>
#include <cpprest/http_client.h>
#include <cpprest/json.h>

// Include the Client class
#include "anki_api.h"

using namespace std;

int main() {
  // Create the client and establish a connection to the server
  Client client("localhost");

  // Create a car and get the token
  client.create_car("AA:BB:CC:DD:EE:FF")
    .then([](const string& token) {
      cout << "Token: " << token << endl;
    })
    .wait();

  // Set the speed of the car
  client.set_speed(500)
    .then([](const string& response) {
      cout << "Set Speed Response: " << response << endl;
    })
    .wait();

  // Make the car switch to the left lane
  client.left_lane(0.5)
    .then([](const string& response) {
      cout << "Left Lane Response: " << response << endl;
    })
    .wait();

  // Make the car switch to the right lane
  client.right_lane(1.0)
    .then([](const string& response) {
      cout << "Right Lane Response: " << response << endl;
    })
    .wait();

  // Get a list of available cars
  client.get_cars(true)
    .then([](const vector<string>& cars) {
      cout << "Available Cars:" << endl;
      for (const auto& car : cars) {
        cout << car << endl;
      }
    })
    .wait();

  return 0;
}
````

## Java
### Client
````java
import api.anki_api;

import java.io.IOException;
import java.util.concurrent.CompletableFuture;

public class Main {
    public static void main(String[] args) {
        // Erstellen eines Client-Objekts
        Client client = new Client("localhost", 5555);

        try {
            // Beispielaufrufe der API-Funktionen
            CompletableFuture<String> createCarResult = client.create_car("AA:BB:CC:DD:EE:FF");
            createCarResult.thenAccept(token -> System.out.println("Token: " + token));

            CompletableFuture<String> setSpeedResult = client.set_speed(50, 2000);
            setSpeedResult.thenAccept(response -> System.out.println("Set Speed Response: " + response));

            CompletableFuture<String> leftLaneResult = client.left_lane(1.5);
            leftLaneResult.thenAccept(response -> System.out.println("Left Lane Response: " + response));

            CompletableFuture<String> rightLaneResult = client.right_lane(0.5);
            rightLaneResult.thenAccept(response -> System.out.println("Right Lane Response: " + response));

            CompletableFuture<String[]> getCarsResult = client.get_cars(true);
            getCarsResult.thenAccept(cars -> {
                System.out.println("Available Cars:");
                for (String car : cars) {
                    System.out.println(car);
                }
            });
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}
````