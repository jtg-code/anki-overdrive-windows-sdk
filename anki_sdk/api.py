"""API module Anki Overdrive SDK"""

import flask
import secrets
import requests
import anki_sdk.cars as cars
import anki_sdk.controller as controllers
import anki_sdk.utils as utils
import threading

class Server:
    """Anki Overdrive API"""
    def __init__(self, address: str, port: int = 5555):
        """Init the API

        Args:
            address (str): Local address
            port (int, optional): Local port. Defaults to 5555.
        """
        self.app: flask.Flask = flask.Flask(__name__)
        
        self.port: int = port
        self.address: str = address
        
        self.cars: dict = {}
        
        self.setup_api()
        
        self.app.run(host=self.address, port=self.port)
        
    def setup_api(self):
        app = self.app
        @app.route("/anki_api/create_car", methods=["POST"])
        def create_car():
            args = flask.request.args
            mac = args["address"]
            car = cars.CarClass(mac)
            car.connect()
            car.start_notify()
            controller = controllers.ControllerClass(car)
            token = secrets.token_urlsafe(16)
            self.cars[token] = {
                "car": car,
                "controller": controller,
                "address": mac
            }
            return token
        
        @app.route("/anki_api/set_speed", methods=["POST"])
        def set_speed():
            args = flask.request.args
            token: str = args["token"]
            car: dict = self.cars[token]
            
            controller: controllers.ControllerClass = car["controller"]
            controller.set_speed(int(args["speed"]), int(args["accel"]))
            return token
        
        @app.route("/anki_api/left_lane", methods=["POST"])
        def left_lane():
            args = flask.request.args
            token: str = args["token"]
            car: dict = self.cars[token]
            
            controller: controllers.ControllerClass = car["controller"]
            controller.left_lane(args["lanes"])
            return token
        
        @app.route("/anki_api/right_lane", methods=["POST"])
        def right_lane():
            args = flask.request.args
            token: str = args["token"]
            if token in self.cars:
                car: dict = self.cars[token]

                controller: controllers.ControllerClass = car["controller"]
                controller.left_lane(float(args["lanes"]))
                return token
            else:
                return "Error: Token not found"

        @app.route("/anki_api/get_cars", methods=["POST"])
        def get_cars():
            active = flask.request.json["active"]
            car_list = utils.scanner(active)
            return flask.jsonify({
                "cars": car_list
            })
         
            
class Client:
    def __init__(self, address: str, port: int = 5555):
        """Init the API

        Args:
            address (str): Local address
            port (int, optional): Local port. Defaults to 5555.
        """
        self.port: int = port
        self.address: str = address
        self.base_url = f"http://{self.address}:{self.port}/anki_api"
        self.token: str = ""
    
    def create_car(self, car: str):
        r = requests.post(f"{self.base_url}/create_car", params={
            "address": car
        })
        self.token = r.text
        return self.token
    
    def set_speed(self, speed: int, accel: int = 1000):
        r = requests.post(f"{self.base_url}/set_speed", params={
            "token": self.token,
            "speed": speed,
            "accel": accel
        })
        return r.text
    
    def left_lane(self, lanes: float = 1.0):
        r = requests.post(f"{self.base_url}/left_lane", params={
            "token": self.token,
            "lanes": lanes
        })
        return r.text
        
    def right_lane(self, lanes: float = 1.0):
        r = requests.post(f"{self.base_url}/right_lane", params={
            "token": self.token,
            "lanes": lanes
        })
        return r.text

    def get_cars(self, active: bool = False):
        r = requests.post(f"{self.base_url}/get_cars", json={
            "active": active
        })
        return r.json()["cars"]