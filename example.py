import anki_sdk.cars as cars
import anki_sdk.controller as c
import anki_sdk.utils as utils
import keyboard as k
import time as t

def newTrack(data):
    print(f"New track: {data}")
    
def ClientFunc():
    car = cars.carClass(input("Address: "))
    car.connect()
    controller = c.controllerClass(car)
    while True:
        auswahl = str(input("1: Speed\n2: Left\n3: Right\n4: Quit\n5: Self controll\nSelect: "))
        if auswahl == "1":
            controller.setSpeed(int(input("Speed: ")), 1000)
        elif auswahl == "2":
            controller.changeLaneLeft(controller.speed, controller.accel, 1)
        elif auswahl == "3":
            controller.changeLaneRight(controller.speed, controller.accel, 1)   
        elif auswahl == "4":
            car.disconnect()
            break
        elif auswahl == "5":
            selfController(car, controller)
            break
    print("Finished")
    

def selfController(car, controller):
    while True:
        if k.is_pressed("w"):
            controller.setSpeed(controller.speed + 100, 1000)
        if k.is_pressed("s") and controller.speed - 100 > 500:
            controller.setSpeed(controller.speed - 100, 1000)
        if k.is_pressed("a"):
            controller.changeOffsetLeft(controller.speed, controller.accel, 10)
        if k.is_pressed("d"):
            controller.changeOffsetRight(controller.speed, controller.accel, 10)
        if k.is_pressed("esc"):
            car.disconnect()
            break
        t.sleep(0.001)
        
ClientFunc()