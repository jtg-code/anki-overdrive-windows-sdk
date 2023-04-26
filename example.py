import anki_sdk.cars as cars
import anki_sdk.controller as controller
import anki_sdk.utils as utils

def main():
    myCar: cars.carClass = cars.carClass("XX:XX:XX:XX")
    myController: controller.controllerClass = controller.controllerClass(myCar)
    speed, accel = 500, 1000
    myController.setSpeed(speed, accel)

    lanes = 3
    myController.leftLane(lanes)
    myController.rightLane(lanes)

    rightLane = 44.5
    leftLane = -44.5
    myController.changeLane(rightLane)
    myController.changeLane(leftLane)

    @myCar.notifyCallback(type=cars.Receive.trackChange)
    def newTrack(sender, data):
        print("New track")
        
        
    @myCar.notifyCallback(type=cars.Receive.specialTrack)
    def specialTrack(sender, data):
        print("Special track")
        
    print(myCar.ping())

if __name__ == "__main__":
    main()