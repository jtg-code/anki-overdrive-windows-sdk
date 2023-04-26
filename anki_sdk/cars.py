import bleak
import asyncio
import time as t
import threading
import struct
from anki_sdk.exceptions import *

class commandList:
    #BLE Connections
    DISCONNECT: bytes = 0xd
    
    #Ping request / response
    PING_REQUEST: bytes = 0x16
    PING_RESPONSE: bytes = 0x17
    
    #Messages for checking vehicle version info
    VERSION_REQUEST: bytes = 0x18
    VERSION_RESPONSE: bytes = 0x19
    
    #Lights
    SET_LIGHTS: bytes = 0x1D
    
    #Driving Commands
    SET_SPEED: bytes = 0x24
    CHANGE_LANE: bytes = 0x25
    CANCEL_LANE_CHANGE: bytes = 0x26
    TURN_180: bytes = 0x32
    
    #Light Patterns
    LIGHTS_PATTERN: bytes = 0x33
    
    #SDK Mode
    SDK_MODE: bytes = 0x90
    
    #Set lane
    RESET_LANE: bytes = 0x2c
    
    
class Receive:
    trackChange: int = 17
    specialTrack: int = 6
    pingResponse: int = 23
    unknown: int = 16
    
    

class carClass():
    def __init__(self, carAddress: str):
       self.address: str = carAddress
       self.client: bleak.BleakClient = bleak.BleakClient(self.address)
       
       # default-Identifiers for the car
       self.SERVICE_UUID: str = "BE15BEEF-6186-407E-8381-0BD89C4D8DF4"
       self.READ_UUID: str = "BE15BEE0-6186-407E-8381-0BD89C4D8DF4"
       self.WRITE_UUID: str = "BE15BEE1-6186-407E-8381-0BD89C4D8DF4"

        # connection status 
       self.connected: bool = False
       self.stop: bool = False
       self.waitPing: bool = False

       self.notifyEvents: dict = {
           17: []
       }
        
    def __str__(self):
        return "Anki Overdrive carClass object"
    
    ######
    
    def notifyCallback(self, type: int = 17):
        def wrapper(func):
            if type in self.notifyEvents.keys():
                self.notifyEvents[type].append(func)
            else:
                self.notifyEvents[type] = []
                self.notifyEvents[type].append(func)
            return func
        return wrapper

    ######
    
    # sends a command via async lib
    def sendCommand(self, command):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._sendCommand(command, loop=loop))

    async def _sendCommand(self, command, loop=None):
        if self.connected == True:
            print(f"Command: {command}")
            command = struct.pack("B", len(command)) + command
            await self.client.write_gatt_char(self.WRITE_UUID, command)
        else:
            raise ConnectionResetError("Not connected to vehicle")
        
    ######        

    # connect to the car with func via async lib
    def connect(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._connect(loop=loop))
        
    # connect to car & enable SDK mode
    async def _connect(self, loop=None):
        await self.client.connect()
        s = await self.client.get_services()  
        self.connected: bool = True
        await self._sendCommand(b"\x90\x01\x01")
        
        
    ######
    def ping(self):
        return asyncio.run(self._ping())
    
    async def _ping(self):
        string = b"\x16\x01\x01"
        await self._sendCommand(string)
        self.startPingTime: int = t.time_ns()
        self.waitPing: bool = True
        while self.waitPing == True:
            t.sleep(0)
        return self.startPingTime
    ######
    
    # disconnect from car
    def disconnect(self, stopCar: bool = True):
        asyncio.run(self._disconnect(stopCar=stopCar))
    
    # disconnect and slow down the car
    async def _disconnect(self, stopCar:bool = True):
        if self.connected == True:
            if stopCar == True:
                await self._sendCommand(struct.pack("<BHHB", commandList.SET_SPEED, 0, 1000, 0x01))
                
            await self._sendCommand(struct.pack("<BB", commandList.DISCONNECT, 0x01))
            self.connected = False
            await self.client.disconnect()
            return True
        else:
            raise ConnectionResetError("Not connected to vehicle")
    ######
    
    def startNotify(self):      
        self.last = ""
        
        def notify(sender, data):
            if data == self.last:
                return
            else:
                self.last = data
            
            index = data[0]
            
            if self.waitPing == True:
                if data[1] == Receive.pingResponse:
                    self.startPingTime = t.time_ns() - self.startPingTime
                    self.startPingTime /= 1000000
                    self.waitPing = False
            
            if index in self.notifyEvents.keys():
                for function in self.notifyEvents[index]:
                    function(sender, data)
                    
            else:
                with open("log.txt", "a") as readFile:
                    readFile.write(f"Sender: {sender} | Data: {data}\n")
                

            
        async def loopDef():
            while True:
                if self.connected == False:
                    break
                if self.connected == True:
                    await self.client.start_notify(self.READ_UUID, notify)
                    await asyncio.sleep(60*60)  # Run for an hour
                if self.connected == False:
                    break
                if self.stop == True:
                    break
            
        
        Threader01: threading.Thread = threading.Thread(target=asyncio.run, args=[loopDef()], daemon=True)
        Threader01.start()
        
    def stopNotify(self):        
        async def loopDef():
            while True:
                if self.connected == False:
                    break
                if self.connected == True:
                    await self.client.stop_notify(self.READ_UUID)
                    self.stop = True
                if self.connected == False:
                    break
            
        
        Threader01 = threading.Thread(target=asyncio.run, args=[loopDef()], daemon=True)
        Threader01.start()