import anki_sdk.cars as cars
import asyncio
import struct
from anki_sdk.exceptions import *

class controllerClass():
    def __init__(self, carClass: cars.carClass):
        self.carClass = carClass
        self.speed = 0
        self.accel = 0
        
    ######
    def setSpeed(self, speed: int, accel: int = 1000):
        loop = asyncio.run(self._setSpeed(speed, accel))
    
    async def _setSpeed(self, speed: int, accel: int = 1000):
        command = struct.pack("<BHHB", cars.commandList.SET_SPEED, speed, accel, 0x01)
        self.speed = speed
        self.accel = accel
        await self.carClass._sendCommand(command)
            
    ######
    def setLane(self, offset: float = 0.0):
        command = struct.pack("<Bf", cars.commandList.RESET_LANE, offset)
        self.carClass.sendCommand(command)

    async def _setLane(self, offset: float = 0.0):
        command = struct.pack("<Bf", cars.commandList.RESET_LANE, offset)
        await self.carClass._sendCommand(command)
        
    def changeLane(self, offset: float):
        asyncio.run(self._changeLane(offset))
    
    async def _changeLane(self, offset: float):
        command = struct.pack("<BHHf", cars.commandList.CHANGE_LANE, self.speed, self.accel, offset)
        await self.carClass._sendCommand(command)
        
    def leftLane(self, lanes: float):
        lane = lanes * -44.5
        self.changeLane(lane)
        
    async def _leftLane(self, lanes: float):
        lane = lanes * -44.5
        await self._changeLane(lane)
        
    def rightLane(self, lanes: float):
        lane = lanes * 44.5
        self.changeLane(lane)
        
    async def _rightLane(self, lanes: float):
        lane = lanes * 44.5
        await self._changeLane(lane)
        
    ######
    
    
    def setLight(self, Red: float, Green: float, Blue: float, Type: float):
        loop = asyncio.run(self._setLight(Red, Green, Blue, Type))
    
    async def _setLight(self, Red: float, Green: float, Blue: float, Type: float):
        command = struct.pack('BBB', 2, 29, Type)
        self.light = (Red, Green, Blue, Type)
        await self.carClass._sendCommand(command)
        
