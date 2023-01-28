"""Support for ComfoAir."""
import logging
from .const import *
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import *
import homeassistant.helpers.event as ev
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.entity import DeviceInfo
from .comfoair import ComfoAirConnection

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR, Platform.FAN]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up ComfoAir integration from a config entry."""
    entry.async_on_unload(entry.add_update_listener(entry_update_listener))

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    if entry.entry_id not in hass.data:
        hass.data[DOMAIN][entry.entry_id] = {}

    connection = ComfoAirConnection(
        udp_ip=entry.data[CONFIG_MOXA_IP],
        udp_receiveport=entry.data[CONFIG_UDP_RECEIVE_PORT],
        udp_sendport=entry.data[CONFIG_UDP_SENDPORT],
        local_ip=entry.data[CONFIG_OPTIONAL_LOCAL_IP]
    )
    
    
    try:
        await connection.connect()
        if connection.isConnected:
            hass.data[DOMAIN][entry.entry_id][COMFOAIR_CONNECTION] = connection
            hass.data[DOMAIN][DATA_DEVICE_INFO] = lambda: device_info(entry)

            for component in PLATFORMS:
                hass.async_create_task(
                    hass.config_entries.async_forward_entry_setup(entry, component)
                )
            return True
        # mal abwarten ob sich die Komponente erneut lädt
        else:
            return False
    except (asyncio.TimeoutError, TimeoutException) as ex:
        raise ConfigEntryNotReady(f"Timeout while connecting to {CONFIG_MOXA_IP}") from ex

    
    


def device_info(entry):
    return DeviceInfo(
        name=(FRIENDLY_NAME + " " + entry.data.get(CONF_FRIENDLY_NAME, "")).strip(),
        manufacturer=MANUFACTORER,
        model=entry.data.get(CONF_FRIENDLY_NAME, None),
        sw_version=entry.data.get(VERSION, None),
        #identifiers=DOMAIN + entry.data.get(CONFIG_MOXA_IP, ""),
        identifiers={(DOMAIN, entry.entry_id)}
    )


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    _LOGGER.debug("Unloading")
    # hass.data[DOMAIN][DATA_WORKING] = False
    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_unload(entry, component)
        )
    # hass.data[DOMAIN][DATA_CANCEL]()
    # await hass.async_add_executor_job(
    #    hass.data[DOMAIN][entry.entry_id][DATA_CONNECTION].stop
    # )
    # hass.data[DOMAIN][entry.entry_id][DATA_CONNECTION] = None
    _LOGGER.debug("Entry unloaded")
    return True


async def entry_update_listener(hass, entry):
    """Handle options update."""
    # kettle = hass.data[DOMAIN][entry.entry_id][DATA_CONNECTION]
    # kettle.persistent = entry.data.get(CONF_PERSISTENT_CONNECTION)
    _LOGGER.debug("Options updated")
