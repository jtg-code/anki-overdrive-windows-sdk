import requests

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

    def disconnect(self, force_stop: bool = True):
        r = requests.post(f"{self.base_url}/disconnect", json={
            "force_stop": force_stop
        }, params={
            "token": self.token
        })
        return r.text