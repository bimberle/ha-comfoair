"""class for ComfoAir """
import socket
import logging
from typing import Any, Dict
from .const import *
from operator import methodcaller
import homeassistant.helpers.event as ev
import time
from .commands import ComfoAirCommand, ParseData, ComfoAirParsing, SKIPCOMMANDS, QUERYCOMMANDS, ACKNOLAGE_STRING, LEVEL_COMMAND, SPECIAL_COMMAND_ROTATION, SPECIAL_COMMAND_TEMPCALCULATION, SPECIAL_COMMAND_LEVEL

_LOGGER: logging.Logger = logging.getLogger(__package__)


class ComfoAirConnection:
    def __init__(self, udp_ip, udp_receiveport, udp_sendport, local_ip=None):
        self.UDP_IP = udp_ip
        self.UDP_RECEIVE_PORT = udp_receiveport
        self.UDP_SENDPORT = udp_sendport
        self.isConnected = False
        self.local_ip = local_ip

        

    def sendCommand(self, command: ComfoAirCommand):
        returnData = {}
        try:
            if not self.isConnected:
                self.connect()
            
            if self.isConnected:
                _LOGGER.debug("Send command %s", command.title)
                self.sendsocket.sendto(command.command, (self.UDP_IP, self.UDP_SENDPORT))
                data, addr = self.reveivesocket.recvfrom(1024)
                returnData = ComfoAirParsing().parseReply(data)
        except Exception as exception:
            _LOGGER.error("Failed to send Command %s: %s", command.title, exception)
        return returnData
        
    async def connect(self):
        try:
            self.sendsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sendsocket.settimeout(5)
            self.reveivesocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            if self.local_ip is None:
                host = None
                try:
                    host = socket.gethostbyname(socket.gethostname())
                except Exception as hostNotFound:
                    _LOGGER.warning("Host not found %s", hostNotFound)
                
                if host == None:
                    try:
                        host = socket.gethostbyname(socket.getfqdn())
                    except Exception as hostNotFound:
                        _LOGGER.warning("Host not found %s", hostNotFound)
            else:
                host = self.local_ip
            
            #host = socket.gethostbyname(socket.getfqdn())
            if host != None:
                self.reveivesocket.bind(
                    # socket.gethostbyname(socket.getfqdn()), self.UDP_RECEIVE_PORT) geht nicht immer
                    (host, self.UDP_RECEIVE_PORT)
                )
                self.reveivesocket.settimeout(5)
                self.isConnected = True
        except Exception as exception:
            _LOGGER.error("Error connecting to Server")
            self.isConnected = False
            ev.async_call_later(hass, 15, connect)
        

class ComfoAir:
    def __init__(self, connection):
        self.connection = connection
        self.attributes = ComfoAirParsing().getInitAttributes()
    
    def connect(self):
        self.connection.connect()
    
    def isConnected(self):
        if self.connection is None or self.connection.isConnected == False:
            return False
        else:
            return True
        

    def getAttributesDict(self):
        return self.attributes

    def setComfoAirSpeed(self, speed):
        """Method to set level speed"""
        try:
            data = self.connection.sendCommand(LEVEL_COMMAND[speed])
            if data:
                self.Stufe = speed
        except Exception as exception:
            _LOGGER.error("Could not set Fan-Speed! - %s", exception)

    def readAll(self):
        """Method to read all data"""
        for comm in QUERYCOMMANDS:
            try:
                reply = self.connection.sendCommand(comm)
                if reply:
                    for key in reply.keys():
                        self.attributes[key] = reply[key]
            except Exception as exception:
                _LOGGER.error("Error sending command %s: %s", comm.title, exception)
                
                            



