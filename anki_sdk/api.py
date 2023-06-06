"""API module Anki Overdrive SDK"""

import flask
import secrets
import requests
import threading

try:
    import cars
    import controllers
    import utils
except ModuleNotFoundError:
    from anki_sdk import cars
    from anki_sdk import controllers
    from anki_sdk import utils


class Server:
    """Anki Overdrive API"""
    def __init__(self, address: str = "127.0.0.1", port: int = 5555):
        """Init the API

        Args:
            address (str): Local address
            port (int, optional): Local port. Defaults to 5555.
        """
        self.app: flask.Flask = flask.Flask(__name__)
        
        self.port: int = port
        self.address: str = address
        
        self.cars: dict = {}
        self.events: list = []
        
        self.setup_api()
        
        self.app.run(host=self.address, port=self.port)
        
    def add_event_handler(self, func):
        self.events.append(func)
        
    def trigger_event(self, type: str, *data):
        for event in self.events:
            event(type, data)
        
    def setup_api(self):
        app = self.app
        @app.route("/anki_api/create_car", methods=["POST"])
        def create_car():
            try:
                args = flask.request.args
                mac = args["address"]
                print(mac)
                car = cars.CarClass(mac)
                car.connect()
                car.start_notify()
                controller = controllers.ControllerClass(car)
                token = secrets.token_urlsafe(16)
                self.cars[token] = {
                    "token": token,
                    "car": car,
                    "controller": controller,
                    "address": mac,
                    "speed": 0,
                    "accel": 0
                }
                self.trigger_event("create_car", self.cars[token])
                return token
            except Exception as e:
                return str(e)
        
        @app.route("/anki_api/set_speed", methods=["POST"])
        def set_speed():
            args = flask.request.args
            token: str = args["token"]
            if token in self.cars:
                car: dict = self.cars[token]
                speed = int(flask.request.json["speed"])
                accel = int(flask.request.json["accel"])
                controller: controllers.ControllerClass = car["controller"]
                controller.set_speed(speed, accel)
                self.cars[token]["speed"] = speed
                self.cars[token]["accel"] = accel
                return token
            else:
                return "Error: Token not found"
        
        @app.route("/anki_api/left_lane", methods=["POST"])
        def left_lane():
            args = flask.request.args
            token: str = args["token"]
            if token in self.cars:
                car: dict = self.cars[token]
                lanes = flask.request.json["lanes"]
                controller: controllers.ControllerClass = car["controller"]
                controller.left_lane(float(lanes))
                return token
            else:
                return "Error: Token not found"
        
        @app.route("/anki_api/right_lane", methods=["POST"])
        def right_lane():
            args = flask.request.args
            token: str = args["token"]
            if token in self.cars:
                car: dict = self.cars[token]
                lanes = flask.request.json["lanes"]
                controller: controllers.ControllerClass = car["controller"]
                controller.right_lane(float(lanes))
                return token
            else:
                return "Error: Token not found"

        @app.route("/anki_api/get_cars", methods=["POST"])
        def get_cars():
            try:
                active = flask.request.json["active"]
                car_list = utils.scanner(active)
                return flask.jsonify({
                    "cars": car_list
                })
            except Exception as e:
                return str(e)
            
        @app.route("/anki_api/get_data", methods=["POST"])
        def get_data():
            try:
                car = flask.request.json["car"]
                data = utils.get_data(car)
                return flask.jsonify({
                    "data": data
                })
            except Exception as e:
                return str(e)
            
        @app.route("/anki_api/disconnect", methods=["POST"])
        def disconnect():
            try:
                args = flask.request.args
                token: str = args["token"]
                force_stop = flask.request.json["force_stop"]
                car = self.cars[token]
                car["car"].disconnect(force_stop)
                del self.cars[token]
                return "Disconnected"
            except Exception as e:
                return str(e)
            
            
            
         
            
class Client:
    def __init__(self, address: str = "127.0.0.1", port: int = 5555, token: str = ""):
        """Init the API

        Args:
            address (str): Local address
            port (int, optional): Local port. Defaults to 5555.
        """
        self.port: int = port
        self.address: str = address
        self.base_url = f"http://{self.address}:{self.port}/anki_api"
        self.token: str = token
    
    def create_car(self, address: str):
        if self.token == "":
            r = requests.post(f"{self.base_url}/create_car", params={
                "address": address
            })
            self.token = r.text
            return self.token
        else:
            return self.token
    
    def set_speed(self, speed: int, accel: int = 1000):
        r = requests.post(f"{self.base_url}/set_speed", params={
            "token": self.token
        }, json={
            "speed": speed,
            "accel": accel
        })
        return r.text
    
    def left_lane(self, lanes: float = 1.0):
        r = requests.post(f"{self.base_url}/left_lane", params={
            "token": self.token,
        }, json={
            "lanes": lanes
        })
        return r.text
        
    def right_lane(self, lanes: float = 1.0):
        r = requests.post(f"{self.base_url}/right_lane", params={
            "token": self.token,
        }, json={
            "lanes": lanes
        })
        return r.text

    def get_cars(self, active: bool = False):
        r = requests.post(f"{self.base_url}/get_cars", json={
            "active": active
        })
        return r.json()["cars"]
    
    def get_data(self, car: str):
        r = requests.post(f"{self.base_url}/get_data", json={
            "car": car
        })
        return r.json()["data"]

    def disconnect(self, force_stop: bool = True):
        r = requests.post(f"{self.base_url}/disconnect", json={
            "force_stop": force_stop
        }, params={
            "token": self.token
        })
        return r.text

if __name__ == "__main__":
    server = Server("127.0.0.1", 5555)