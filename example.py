import anki_sdk as sdk
import threading

def test(addr, speed):
    car = sdk.cars.CarClass(addr)
    car.connect()
    controller = sdk.controllers.ControllerClass(car)
    controller.set_speed(speed)

threading.Thread(target=test, args=("F8:21:8E:B8:E0:85", 1000)).start()
threading.Thread(target=test, args=("EF:4E:49:08:14:F6", 1000)).start()


print(sdk.utils.scanner(True))