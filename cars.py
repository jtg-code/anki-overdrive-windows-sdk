import asyncio
import bleak as b
import struct
import time

class carClass():
    def __init__(self, address: str):
        self.connected = False
        # UUIDs für das Schreiben und Lesen von Charakteristiken
        self.WRITE_UUID = "BE15BEE1-6186-407E-8381-0BD89C4D8DF4"
        self.UUID_READ = "BE15BEE0-6186-407E-8381-0BD89C4D8DF4"
        # Fahrzeug Mac-Adresse
        self.address = address
        # Start vehicle
        
    def __str__(self):
        while self.connected == False:
            time.sleep(0.1)
        return self
    
    async def _sendCommand(self, command):
        finalCommand = struct.pack("B", len(command)) + command
        await self.client.write_gatt_char(self.WRITE_UUID, finalCommand)

    async def _connect(self):
        self.client = b.BleakClient(self.address)
        time.sleep(1) # make sure that bleakClient is ready
        await self.client.connect()
        print("Connected!")
        sdk_command = b"\x90\x01\x01"
        await self._sendCommand(sdk_command) # Enable SDK Mode
        print("SDK Mode on!")
        print(f"Connected to {self.address}")
            
    async def _disconnect(self):
        break_command = struct.pack("<BHHB", 0x24, 0, 1000, 0x01)
        await self._sendCommand(break_command) # Slow down
        await self.client.disconnect()

#------------------------------------------------------------------- 

    def sendCommand(self, command):
        asyncio.run(self._sendCommand(command))
        
    def connect(self):
        asyncio.run(self._connect())
        
    def disconnect(self):
        asyncio.run(self._disconnect())