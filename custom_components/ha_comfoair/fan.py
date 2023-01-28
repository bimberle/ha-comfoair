"""Comfoair fan platform for speed"""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.fan import FanEntity
from homeassistant.components.fan import FanEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util.percentage import ordered_list_item_to_percentage
from homeassistant.util.percentage import percentage_to_ordered_list_item

from .comfoair import ComfoAir

from .const import DEFAULT_NAME
from .const import ATTR_CURRENT_STAGE
from .const import FRIENDLY_NAME
from .const import DOMAIN
from .const import FAN_SPEEDS
from .const import COMFOAIR_CONNECTION
from .const import DISPATCHER_UPDATE

LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the ComfoAir fan."""
    async_add_entities(
        [
            ComfoAirFan(hass,entry)
        ]
    )


class ComfoAirFan(FanEntity):
    """ComfoAir Fan"""

    _attr_supported_features = (
        FanEntityFeature.SET_SPEED
    )
    _attr_has_entity_name = True
    _attr_name = None
    _attr_should_poll = True

    def __init__(self, hass: HomeAssistant, entry) -> None:
        """Initialize the entity."""
        self.hass = hass
        self.entry = entry
        conn = hass.data[DOMAIN][entry.entry_id][COMFOAIR_CONNECTION] 
        self.comfoair = ComfoAir(conn)
    
    async def async_added_to_hass(self) -> None:
        self.update()
        self.async_on_remove(
            async_dispatcher_connect(self.hass, DISPATCHER_UPDATE, self.update)
        )
    
    def update(self):
        if self.comfoair.isConnected() == False:
            self.comfoair.connect(self.comfoair_connection())

        self.comfoair.readAll()
        comLevel = self.comfoair.getAttributesDict()[ATTR_CURRENT_STAGE]
        fanLevel = percentage_to_ordered_list_item(FAN_SPEEDS, self.percentage)
        if comLevel != fanLevel and comLevel > -1 and comLevel <= len(FAN_SPEEDS)-1:
            self.set_percentage(ordered_list_item_to_percentage(FAN_SPEEDS, FAN_SPEEDS[comLevel]))
        self.schedule_update_ha_state()            

    def comfoair_connection(self):
        return self.hass.data[DOMAIN][self.entry.entry_id][COMFOAIR_CONNECTION]
    
    @property
    def name(self):
        """Name of the entity."""
        return FRIENDLY_NAME

    @property
    def unique_id(self) -> str:
        """Return the unique id."""
        return f"{self.entry.entry_id}"
    
    @property
    def device_info(self):
        return f"{DOMAIN}_{self.entry.entry_id}"
        #return self.hass.data[DOMAIN][DATA_DEVICE_INFO]()


    @property
    def speed_count(self) -> int:
        """Return the number of speeds the fan supports."""
        return len(FAN_SPEEDS)

    def set_percentage(self, percentage: int) -> None:
        """Set the speed of the fan, as a percentage."""
        self._attr_percentage = percentage


    async def async_set_percentage(self, percentage: int) -> None:
        """Set the speed of the fan, as a percentage."""
        if percentage == 0:
            level = 0 
        else:
            level = percentage_to_ordered_list_item(FAN_SPEEDS, percentage)
        self.comfoair.setComfoAirSpeed(level)
        await self.hass.async_add_executor_job(self.set_percentage, percentage)
        self.async_write_ha_state()

    async def async_turn_on(
        self,
        percentage: int | None = None,
        preset_mode: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Turn on the entity."""
        if percentage is None:
            percentage = ordered_list_item_to_percentage(FAN_SPEEDS, FAN_SPEEDS[2])

        await self.async_set_percentage(percentage)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the entity."""
        await self.async_set_percentage(0)
        self.async_write_ha_state()


    

    