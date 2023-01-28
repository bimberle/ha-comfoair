# Comfoair Home Assistant Integration with Moxa
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![Build Status](https://img.shields.io/github/actions/workflow/status/bimberle/ha-comfoair/build.yaml?branch=master&style=flat-square)](https://github.com/bimberle/ha-comfoair-sensor/actions/workflows/build.yaml)

This integration receives data from comfoair CA350 via Moxa (RS232 IP Gateway)

To setup the hardware environment, please follow these instructions:
## 1. Connect your Comfoair via RS232 to LAN to your Moxa
![screenshot moxa serial connection](https://github.com/bimberle/ha-comfoair/blob/master/images/comfoair_moxa_rs232.png?raw=true)
## 2. Congifure your Moxa
2.1. Serial-Settings Port 1:
![screenshot moxa serial settings](https://github.com/bimberle/ha-comfoair/blob/9fbea868fbc7057e2884d97a76568af9c2a06e3d/images/moxa_serial_settings.jpg?raw=true)
- Baud Rate 9600
- Data bits 8
- Stop bits 1
- Parity: None
- Flow control: None
- FIFO: enable
2.2. Operating Settins Port 1:
![screenshot moxa operating settings](https://github.com/bimberle/ha-comfoair/blob/9fbea868fbc7057e2884d97a76568af9c2a06e3d/images/moxa_operating_settings.jpg?raw=true)
- Operation mode: UDP
- Packing length: 0
- Delimiter 1: 7 + Enable
- Delimiter 2: f + Enable
- Delimiter process: Do Nothing
- Force transmit: 0
- Desitnation IP address 1:
- - Begin: your HA IP
- - End: your HA IP
- - Port: 7001
- Local Listen port: 6999

## Install Integration
### Manual Installation
Copy...
### Installation via HACS

## Configure Integration
- IP-Address of Moxa
- UPD Receiveport
Moxa forwards all messages from your comfoair to you HA IP and Port 7001, so your integration Receiveport has to be 7001
- UDP Sendport
Moxa listens to Port 6999, so the integration Sendport has to be 6999
