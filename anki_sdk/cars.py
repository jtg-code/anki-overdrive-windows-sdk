"""Car Class file"""

import asyncio
import time as t
import threading
import struct
from enum import Enum
import bleak
from anki_sdk.exceptions import NotConnected


class CommandList(Enum):
    """All found BLE commands

    Commands:
        BLE Connection:
            DISCONNECT (bytes): Command for disconnect.\n
            PING_REQUEST (bytes): Command to send a ping request.\n
            PING_RESPONSE (bytes): Response from the vehicle to ping.\n
            VERSION_REQUEST (bytes): Command to send a version request\n
            VERSION_RESPONSE (bytes): Response from the vehicle to version.\n
        -------------------------------------------------------------------\n
        Lights:
            SET_LIGHTS (bytes): Set vehicle lights.\n
            LIGHTS_PATTERN (bytes): Set light pattern.\n
        -------------------------------------------------------------------\n
        Driving Commands:
            SET_SPEED (bytes): Set vehicle speed and accel.\n
            CHANGE_LANE (bytes): Change vehicle lane.\n
            CANCEL_LANE_CHANGE (bytes): Cancel lane change.\n
            TURN_180 (bytes): Turn 180.\n
        -------------------------------------------------------------------\n
        Misc commands:
            SDK_MODE (bytes): Enable SDK Mode.\n
            RESET_LANE (bytes): Enable SDK Mode.\n
        -------------------------------------------------------------------\n
    """
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
    LIGHTS_PATTERN: bytes = 0x33
    #Driving Commands
    SET_SPEED: bytes = 0x24
    CHANGE_LANE: bytes = 0x25
    CANCEL_LANE_CHANGE: bytes = 0x26
    TURN_180: bytes = 0x32
    #SDK Mode
    SDK_MODE: bytes = 0x90
    RESET_LANE: bytes = 0x2c
    SERVICE_UUID: str = "BE15BEEF-6186-407E-8381-0BD89C4D8DF4"
    READ_UUID: str = "BE15BEE0-6186-407E-8381-0BD89C4D8DF4"
    WRITE_UUID: str = "BE15BEE1-6186-407E-8381-0BD89C4D8DF4"
    def sdk(self):
        """Get byte command

        Returns:
            bytes: SDK Mode byte command
        """
        return self.SDK_MODE
    def __str__(self):
        """str

        Returns:
            String: Command list to send to car
        """
        return "Command list to send to car"

class Receive(Enum):
    """@notifyCallback types

    Commands:
        Connection:
            PING_RESPONSE (tuple): Response from the vehicle to ping.\n
        -------------------------------------------------------------------\n
        Track:
            TRACK_CHANGE (tuple): A new Track
            FINISHLINE: (tuple): Drive over finishline.\n
            SPECIAL_TRACK: (tuple): Drive over special track\n
            STRAIGHT_TRACK: (tuple): Drive over straight track.\n
    """
    class Connection(Enum):
        """Connection notify events
        
        Connection:
            PING_RESPONSE (tuple): Response from the vehicle to ping.\n
        """
        PING_RESPONSE: int = (23, 1)

    class Track(Enum):
        """Track notify events

        Track:
            TRACK_CHANGE (tuple): A new Track
            FINISHLINE: (tuple): Drive over finishline.\n
            SPECIAL_TRACK: (tuple): Drive over special track\n
            STRAIGHT_TRACK: (tuple): Drive over straight track.\n
        """
        TRACK_CHANGE: int = (17, 0)
        FINISHLINE: int = (34, 16)
        SPECIAL_TRACK: int = (6, 0)
        STRAIGHT_TRACK: int = (38, 16)

    # UNKNOWN: int = (23, 13)
    # UNKNOWN: int = (22, 13)
    # UNKNOWN: int = 16

class CarClass():
    """Car class object

    Args:
        carAddress (str): vehicle MAC-address
    """
    ## Make everything ready
    def __init__(self, car_address: str):
        self.address: str = car_address
        self.client: bleak.BleakClient = bleak.BleakClient(self.address)
        #connection status
        self.connected: bool = False
        self.wait_ping: bool = False
        self.notify_events: dict = {}
        #tmp var
        self.before = ""
        self.start_ping_time = None

    ## Get object as string
    def __str__(self):
        return f"Anki Overdrive carclass | {self.address}"

    ### Register the notifycallback type
    def notifycallback(self, event: tuple[int, int] | Receive = (17, 0)):
        """@decorator

        Args:
            event (tuple[int, int]): Code when it should get triggered. Defaults to (17, 0).
        """
        def wrapper(func):
            if event in self.notify_events:
                self.notify_events[event].append(func)
            else:
                self.notify_events[event] = []
                self.notify_events[event].append(func)
            return func
        return wrapper

    # Send BLE command to car
    def send_command(self, command: bytes):
        """Send BLE command to car

        Args:
            command (bytes): Command that should get send.
        """
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.async_send_command(command))
    async def async_send_command(self, command: bytes):
        """Send BLE command to car

        Args:
            command (bytes): Command that should get send.
        """
        if self.connected:
            command = struct.pack("B", len(command)) + command
            await self.client.write_gatt_char(CommandList.WRITE_UUID, command)
        else:
            raise NotConnected("Not connected to vehicle")

    # connect to car & enable SDK mode
    def connect(self):
        """Connect with car

        Returns:
            bool: Connected
        """
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self._connect())
        return loop
    async def _connect(self):
        """Connect with car

        Returns:
            bool: Connected
        """
        await self.client.connect()
        self.connected: bool = True
        await self.async_send_command(b"\x90\x01\x01")
        return True

    # Ping to car
    def ping(self):
        """Get the ping to vehicle

        Returns:
            ping (int): Ping in ms.
        """
        value: int = asyncio.run(self._ping())
        return value
    async def _ping(self):
        """Get the ping to vehicle

        Returns:
            ping (int): Ping in ms.
        """
        command = struct.pack("<BBB", CommandList.PING_REQUEST, 0x01, 0x01)
        await self.async_send_command(command)
        self.start_ping_time: int = t.time_ns()
        self.wait_ping: bool = True
        while self.wait_ping:
            t.sleep(0)
        return self.start_ping_time

    # disconnect from car
    def disconnect(self, stop_car: bool = True):
        """Disconnect from vehicle

        Args:
            stopCar (bool): Forcestop car.
            
        Returns:
            worked (bool): Disconnect worked.
        """
        value: bool = asyncio.run(self._disconnect(stop_car=stop_car))
        return value

    # disconnect and slow down the car
    async def _disconnect(self, stop_car:bool = True):
        """Disconnect from vehicle

        Args:
            stop_car (bool): Forcestop car.
            
        Returns:
            worked (bool): Disconnect worked.
        """
        if self.connected:
            if stop_car:
                command = struct.pack("<BHHB", CommandList.SET_SPEED, 0, 1000, 0x01)
                await self.async_send_command(command)

            t.sleep(0.5)
            await self.async_send_command(struct.pack("<BB", CommandList.DISCONNECT, 0x01))
            self.connected = False
            await self.client.disconnect()
            return True

    def trigger_notify(self, sender: str, data: bytearray):
        """_summary_

        Args:
            sender (str): Sender from the notify
            data (bytearray): Data what got send
        """
        for event, eventindex in self.notify_events:
            if not eventindex in range(len(data) - 1):
                continue
            if data[eventindex] is None:
                continue
            index = data[eventindex]
            if index != event:
                continue
            for function in self.notify_events[(event, eventindex)]:
                if (event, eventindex) in dict(Receive.Track):
                    if data[0] == 17:
                        function(sender, data)
                else:
                    function(sender, data)

    # Start to receive notify
    def start_notify(self):
        """Starts the notification callback"""
        def notify(sender, data: bytearray):
            if data == self.before:
                return

            self.before = data

            if self.wait_ping and data[1] == Receive.Connection.PING_RESPONSE:
                self.start_ping_time = t.time_ns() - self.start_ping_time
                self.start_ping_time /= 1000000
                self.wait_ping = False

            self.trigger_notify(sender, data)
            # with open("log.txt", "a") as file:
            #     if data[0] != 16:
            #         text = "["
            #         i = 0
            #         for v in list(data):
            #             text += f"{v}(%{i}),"
            #             i += 1
            #         text += "]"
            #         file.write(f"{text}\n")

        async def loop_def():
            while True:
                if self.connected:
                    await self.client.start_notify(CommandList.READ_UUID, notify)
                    await asyncio.sleep(60*60)  # Run for an hour
                else:
                    break

        threading.Thread(target=asyncio.run, args=[loop_def()], daemon=True).start()

    #######
    def stop_notify(self):
        """Stops the notification callback"""       
        async def stop_notify_loop():
            while True:
                if self.connected:
                    await self.client.stop_notify(CommandList.READ_UUID)
                else:
                    break
        threading.Thread(target=asyncio.run, args=[stop_notify_loop()], daemon=True).start()
