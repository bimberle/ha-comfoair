"""class for ComfoAir """
import socket
import logging
from typing import Any, Dict
from .const import *
from operator import methodcaller
from datetime import datetime
import time
from .commands import ComfoAirCommand, ParseData, SKIPCOMMANDS, QUERYCOMMANDS, ACKNOLAGE_STRING, LEVEL_COMMAND

_LOGGER: logging.Logger = logging.getLogger(__package__)


class ComfoAirConnection:
    def __init__(self, udp_ip, udp_receiveport, udp_sendport):
        self.UDP_IP = udp_ip
        self.UDP_RECEIVE_PORT = udp_receiveport
        self.UDP_SENDPORT = udp_sendport
        self.isConnected = False
        
        loopCount = 0

        # UDP Socket
        while loopCount < 3:
            try:
                self.sendsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.sendsocket.settimeout(5)
                self.reveivesocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                try:
                    self.reveivesocket.bind(
                        # socket.gethostbyname(socket.getfqdn()), self.UDP_RECEIVE_PORT) geht nicht immer
                        (socket.gethostbyname(socket.getfqdn()), self.UDP_RECEIVE_PORT)
                    )
                except Exception as excepti:
                    _LOGGER.error("Error setting up binding to Port %s", self.UDP_RECEIVE_PORT)
                    
                self.reveivesocket.settimeout(5)
                self.isConnected = True
                break
            except Exception as exception:
                _LOGGER.error("Error connecting to Server")
            loopCount += 1

    def sendCommand(self, command: ComfoAirCommand):
        try:
            _LOGGER.debug("Send command %s", command.title)
            self.sendsocket.sendto(command.command, (self.UDP_IP, self.UDP_SENDPORT))
            data, addr = self.reveivesocket.recvfrom(1024)
            return data
        except Exception as exception:
            raise exception
        

class ComfoAir:
    def __init__(self, connection):
        self.connection = connection
        self.lastcall = None
    
    def connect(self, connection):
        self.connection = connection
    
    def isConnected(self):
        if self.connection is None or self.connection.isConnected == False:
            return True
        

    def getAttributesDict(self):
        attr = {}
        for comm in QUERYCOMMANDS:
            for data in comm.parseData:
                attr[data.name] = data.value
        
        return attr

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
                self.parseReply(reply)
            except Exception as exception:
                _LOGGER.error("Error sending command %s: %s", comm.title, exception)
                
            


    def parseReply(self, reply):
        if reply:
            replyCommandsValue = hex(reply[5])
            if replyCommandsValue not in SKIPCOMMANDS:
                for comm in QUERYCOMMANDS:
                    if replyCommandsValue == comm.replycommand:
                        _LOGGER.debug("Parsing %s", comm.title)
                        self.lastcall = datetime.now()
                        for parsed in comm.parseData:
                            parsed.value = reply[parsed.arrayIndex]
                            _LOGGER.debug("Set Value %s=%s", parsed.name, parsed.value)
                            



