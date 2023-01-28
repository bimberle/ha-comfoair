"""ComfoAir Sensors."""
import logging

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
)
from typing import Any
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.const import *

from .comfoair import ComfoAir
from .const import *

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the ComfoAir entry."""
    # model_code = hass.data[DOMAIN][entry.entry_id][DATA_CONNECTION].model_code
    async_add_entities(
        [ComfoAirDataSensor(hass, entry)]
    )


class ComfoAirDataSensor(SensorEntity):
    """Representation of a ComfoAir data sensor device."""

    def __init__(self, hass, entry):
        """Initialize the sensor device."""
        self.hass = hass
        self.entry = entry
        self.sensor_type = SENSOR
        self._attributes = None
        self._state = None
        conn = hass.data[DOMAIN][entry.entry_id][COMFOAIR_CONNECTION] 
        self.comfoair = ComfoAir(conn)

    async def async_added_to_hass(self):
        self.update()
        self.async_on_remove(
            async_dispatcher_connect(self.hass, DISPATCHER_UPDATE, self.update)
        )

    def update(self):
        if self.comfoair.isConnected() == False:
            self.comfoair.connect(self.comfoair_connection())
            
        self.comfoair.readAll()
        self._attributes = self.comfoair.getAttributesDict()
        self._state = self.comfoair.isConnected()
        self.schedule_update_ha_state()

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return entity specific state attributes for babybuddy."""
        return self._attributes

    @property
    def state(self):
        """Return the state of the device."""
        return self._state
        
    #@property
    def comfoair_connection(self):
        return self.hass.data[DOMAIN][self.entry.entry_id][COMFOAIR_CONNECTION]

    @property
    def unique_id(self):
        return f"{self.entry.entry_id}_{self.sensor_type}"

    @property
    def device_info(self):
        return f"{DOMAIN}_{self.entry.entry_id}"
        #return self.hass.data[DOMAIN][DATA_DEVICE_INFO]()

    @property
    def last_update(self):
        return None

    @property
    def name(self):
        """Name of the entity."""
        return (
            FRIENDLY_NAME + " " + self.entry.data.get(CONF_FRIENDLY_NAME, "")
        ).strip()

    @property
    def icon(self):
        return "mdi:climate"

    @property
    def available(self):
        return True  # Always readable

    @property
    def entity_category(self):
        return None

    @property
    def device_class(self):
        return None  # Unusual class

    @property
    def state_class(self):
        return SensorStateClass.MEASUREMENT

    @property
    def native_unit_of_measurement(self):
        return None

    @property
    def native_value(self):
        return None

