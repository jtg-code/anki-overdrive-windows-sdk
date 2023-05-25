# Anki Overdrive windows SDK

## installation
1. Download the newest release</li>
2. Extract the ```anki_sdk``` directory
3. Run ```pip install -r requirements.txt``` <b>OR</b> run the ```Setup.py```


## Functions
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
