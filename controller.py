import struct

class controllerClass():
    def __init__(self, carClass):
        self.carClass = carClass
        self.speed = 0
        self.accel = 0
        
        
    async def _setSpeed(self, speed:int, accel:int):
        # Parameters:
        # speed -- Desired speed. (from 0 - 1000)
        # accel -- Desired acceleration. (from 0 - 1000)
        self.speed = speed
        self.accel = accel
        if speed > 1000 or accel > 1000:
            print("Speed/Accellimit exceeded!")
        if speed < 0 or accel < 0:
            print("Not valid input!")
        else:
            command = struct.pack("<BHHB", 0x24, speed, accel, 0x01)
            await self.carClass._sendCommand(command)

    async def _setLane(self, offset:float):
        command = struct.pack("<Bf", 0x2c, offset)
        await self.carClass._sendCommand(command)

    async def _changeLane(self, speed:int, accel:int, offset:float):
        await self._setLane(0.0)
        command = struct.pack("<BHHf", 0x25, speed, accel, offset)
        await self.carClass._sendCommand(command)
        
    async def _changeLaneLeft(self, speed:int, accel:int, lanes:int):
        await self._changeLane(speed, accel, -44.5 * lanes)

    async def _changeLaneRight(self, speed:int, accel:int, lanes:int):
        await self._changeLane(speed, accel, 44.5 * lanes)
        
    async def _changeOffsetRight(self, speed:int, accel:int, offset:float):
        await self._changeLane(speed, accel, offset)
        
    async def _changeOffsetLeft(self, speed:int, accel:int, offset:float):
        await self._changeLane(speed, accel, offset * -1) 

# -------------------------------------------------------------------------------------

    def changeLaneLeft(self, speed:int, accel:int, lanes:int):
        self.changeLane(speed, accel, -44.5 * lanes)
    
    def changeLaneRight(self, speed:int, accel:int, lanes:int):
        self.changeLane(speed, accel, 44.5 * lanes)
        
    async def changeOffsetRight(self, speed:int, accel:int, offset:float):
        await self.changeLane(speed, accel, offset)
        
    async def changeOffsetLeft(self, speed:int, accel:int, offset:float):
        await self.changeLane(speed, accel, offset * -1) 

    def setLane(self, offset:float):
        command = struct.pack("<Bf", 0x2c, offset)
        self.carClass.sendCommand(command)

    def changeLane(self, speed, accel, offset:float):
        self.setLane(0.0)
        command = struct.pack("<BHHf", 0x25, speed, accel, offset)
        self.carClass.sendCommand(command)
        
    def setSpeed(self, speed:int, accel:int):
        self.speed = speed
        self.accel = accel
        if speed > 1000 or accel > 1000:
            print("Speed/Accellimit exceeded!")
        if speed < 0 or accel < 0:
            print("Not valid input!")
        else:
            command = struct.pack("<BHHB", 0x24, speed, accel, 0x01)
            self.carClass.sendCommand(command)




