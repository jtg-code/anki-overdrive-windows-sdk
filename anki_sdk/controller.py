"""Controller class file"""

import asyncio
import struct
import anki_sdk.cars as cars

class ControllerClass():
    """Controller class object

    Args:
        carClass (carClass): Car to be controlled
    """

    def __init__(self, car_class: cars.CarClass):
        self.car_class: cars.CarClass = car_class
        self.speed = 0
        self.accel = 0
        self.light = (0, 0, 0)

    ######
    def set_speed(self, speed: int, accel: int = 1000):
        """Set the vehicle speed

        Args:
            speed (int): Speed to set.
            accel (int): Accelration. Defaults to 1000.
        """
        asyncio.run(self.async_set_speed(speed, accel))

    async def async_set_speed(self, speed: int, accel: int = 1000):
        """Set the vehicle speed

        Args:
            speed (int): Speed to set.
            accel (int): Accelration. Defaults to 1000.
        """
        command = struct.pack("<BHHB", cars.CommandList.SET_SPEED, speed, accel, 0x01)
        self.speed = speed
        self.accel = accel
        await self.car_class.async_send_command(command)

    ######
    def set_lane(self, offset: float = 0.0):
        """Set the current lane for the vehicle (doesn't move the car)

        Args:
            offset (float): Offset from lane. Defaults to 0.0.
        """
        command = struct.pack("<Bf", cars.CommandList.RESET_LANE, offset)
        self.car_class.send_command(command)

    async def async_set_lane(self, offset: float = 0.0):
        """Set the current lane for the vehicle (doesn't move the car)

        Args:
            offset (float): Offset from lane. Defaults to 0.0.
        """
        command = struct.pack("<Bf", cars.CommandList.RESET_LANE, offset)
        await self.car_class.async_send_command(command)

    ######
    def change_lane(self, offset: float):
        """Change current lane

        -44.5 left
        44.5 right
        
        Args:
            offset (float): How much the car should move.
        """
        asyncio.run(self.async_change_lane(offset))

    async def async_change_lane(self, offset: float):
        """Change current lane

        -44.5 left
        44.5 right
        
        Args:
            offset (float): How much the car should move.
        """
        command = struct.pack("<BHHf", cars.CommandList.CHANGE_LANE, self.speed, self.accel, offset)
        await self.car_class.async_send_command(command)

    def left_lane(self, lanes: float = 1.0):
        """Change the lane to left

        Args:
            lanes (float): How many lanes to left. Default 1.0
        """
        lane = lanes * -44.5
        self.change_lane(lane)

    async def async_left_lane(self, lanes: float = 1.0):
        """Change the lane to left

        Args:
            lanes (float): How many lanes to left. Default 1.0
        """
        lane = lanes * -44.5
        await self.async_change_lane(lane)

    def right_lane(self, lanes: float = 1.0):
        """Change the lane to right

        Args:
            lanes (float): How many lanes to right. Default 1.0
        """
        lane = lanes * 44.5
        self.change_lane(lane)

    async def async_right_lane(self, lanes: float = 1.0):
        """Change the lane to right

        Args:
            lanes (float): How many lanes to right. Default 1.0
        """
        lane = lanes * 44.5
        await self.async_change_lane(lane)

    def set_light(self, red: float, green: float, blue: float, pattern: float):
        """Set vehicle light

        Args:
            red (float): Red
            green (float): Green
            blue (float): Blue
            pattern (float): Pattern type
        """
        asyncio.run(self.async_set_light(red, green, blue, pattern))

    async def async_set_light(self, red: float, green: float, blue: float, pattern: float):
        """Set vehicle light

        Args:
            red (float): Red
            green (float): Green
            blue (float): Blue
            pattern (float): Pattern type
        """
        command = struct.pack('BBB', 2, 29, pattern)
        self.light = (red, green, blue, pattern)
        await self.car_class.async_send_command(command)
