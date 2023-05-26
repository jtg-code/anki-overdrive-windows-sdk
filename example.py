import anki_sdk as sdk
import threading
import time

def controll_car(address: str):
    car = sdk.cars.CarClass(address)
    car.connect()
    car.start_notify()
    controller = sdk.controller.ControllerClass(car)
    #print(f"Pong! {car.ping()}ms")
    controller.set_speed(500, 500)
    time.sleep(10)
    controller.left_lane(1.0)
    time.sleep(10)
    controller.right_lane(1.0)
    time.sleep(10)
    
    
    @car.notifycallback(sdk.cars.Receive.Track.TRACK_CHANGE)
    def new_track(sender, data):
        print("New Track!")
        
    @car.notifycallback(sdk.cars.Receive.Track.FINISHLINE)
    def finish_line(sender, data):
        print("Finish!")
        
    @car.notifycallback(sdk.cars.Receive.Track.SPECIAL_TRACK)
    def special_track(sender, data):
        print("Special Track!")
        
    @car.notifycallback(sdk.cars.Receive.Track.STRAIGHT_TRACK)
    def straight_track(sender, data):
        print("New Straight Track!")
        
    @car.notifycallback(sdk.cars.Receive.Connection.PING_RESPONSE)
    def ping_response(sender, data):
        print("Ping Response!")
    
    car.stop_notify()
    car.disconnect()
    
def main():
    car_list_address = sdk.utils.scanner(False)
    car_list = {address: sdk.utils.get_data(address) for address in car_list_address}
    for car in car_list:
        threading.Thread(target=controll_car, args=[car])



if __name__ == "__main__":
    #main()
    controll_car("F8:21:8E:B8:E0:85")