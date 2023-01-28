from datetime import timedelta

DOMAIN = "ha_comfoair"
SENSOR = "sensor"
ICON = "mdi:format-quote-close"
STARTUP_MESSAGE = "Comfoair Integration wird geladen"
FRIENDLY_NAME = "ComfoAir"
MANUFACTORER = "Zehnder"

CONFIG_MOXA_IP = "moxa_ip_address"
CONFIG_MOXA_IP_DEFAULT = "192.168.178.47"
CONFIG_UDP_SENDPORT = "moxa_udp_sendport"
CONFIG_UDP_SENDPORT_DEFAULT = "6999"
CONFIG_UDP_RECEIVE_PORT = "moxa_udp_receiveport"
CONFIG_UDP_RECEIVE_PORT_DEFAULT = "7001"
CONFIG_OPTIONAL_LOCAL_IP_DEFAULT = "192.168.178.77"
CONFIG_OPTIONAL_LOCAL_IP = "local_ip"


DEFAULT_NAME = DOMAIN
ATTRIBUTION = "ComfoAir Integration by kechm"
NAME = "ComfoAirMoxa"
VERSION = "1.0.0"
COMFOAIR_CONNECTION = "ComfoAirConnection"

SCAN_INTERVAL = timedelta(minutes=10)
DATA_DEVICE_INFO = "device_info"
DISPATCHER_UPDATE = "update"

ATTR_TEMP_ENTHALPIE = "temperature_enthalpie"
ATTR_HUMIDITY = "humidity"
ATTR_ENTHALPIE_TIMER = "timer_enthalpie"
ATTR_TEMP_OUTSIDE = "temperature_outside"
ATTR_TEMP_SUPPLY_AIR = "temperature_supply_air"
ATTR_TEMP_USED_AIR = "temperature_used_air"
ATTR_TEMP_FORT_AIR = "temperature_fort_air"
ATTR_TEMP_KOMFORT = "temperature_komfort"
ATTR_SUPPLY_AIR_SPEED = "speed_supply_air"
ATTR_SUPPLY_AIR_PERCENTAGE = "supply_air_percentage"
ATTR_USED_AIR_SPEED = "speed_used_air"
ATTR_USED_AIR_PERCENTAGE = "used_air_percentage"

ATTR_BYPASS_STATUS = "bypass_status"
ATTR_FILTER_OK = "filterstatus"
ATTR_STAGE = "stage"
ATTR_LASTCALL = "lastcall"

ATTR_PERCENT_OUT_AWAY = "percent_abluft_abwesend"
ATTR_PERCENT_OUT_LEVEL1 = "percent_abluft_stufe1"
ATTR_PERCENT_OUT_LEVEL2 = "percent_abluft_stufe2"
ATTR_PERCENT_OUT_LEVEL3 = "percent_abluft_stufe3"
ATTR_PERCENT_IN_AWAY = "percent_zuluft_abwesend"
ATTR_PERCENT_IN_LEVEL1 = "percent_zuluft_stufe1"
ATTR_PERCENT_IN_LEVEL2 = "percent_zuluft_stufe2"
ATTR_PERCENT_IN_LEVEL3 = "percent_zuluft_stufe3"
ATTR_PERCENT_OUT = "percent_abluft_ist"
ATTR_PERCENT_IN = "percent_zuluft_ist"
ATTR_ROTATION_SUPPLY_AIR = "rotation_zuluft"
ATTR_ROTATION_USED_AIR = "rotation_abluft"
ATTR_CURRENT_STAGE = "aktuelle_stufe"

FAN_SPEEDS = [0,1,2,3]
OFFLINE_TEXT = "Offline"
ICON_OFFLINE = "mdi:fan-alert"
ICON_ONLINE = "mdi:fan"