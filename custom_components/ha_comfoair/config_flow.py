"""Config flow for ComfoAir integration."""
import logging
import voluptuous as vol
from homeassistant.const import *
from homeassistant import config_entries
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv
from .const import *
from .comfoair import ComfoAir, ComfoAirConnection

_LOGGER = logging.getLogger(__name__)


class ComfoAirConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(entry):
        """Get options flow for this handler."""
        return ComfoAirConfigFlow(entry=entry)

    def __init__(self, entry=None):
        """Initialize a new ComfoAirConfigFlow."""
        self.entry = entry
        self.config = {} if not entry else dict(entry.data.items())

    async def async_step_user(self, user_input=None):
        """Handle the user step."""
        return await self.async_step_connect()

    async def async_step_connect(self, user_input=None):
        """Handle the connect step."""
        errors = {}
        if user_input is not None:
            conn = ComfoAirConnection(
                udp_ip=self.config[CONFIG_MOXA_IP],
                udp_receiveport=self.config[CONFIG_UDP_RECEIVE_PORT],
                udp_sendport=self.config[CONFIG_UDP_SENDPORT]
                # model=self.config.get(CONF_FRIENDLY_NAME, None),
            )
            comfoAir = ComfoAir(connection=conn)
            comfoAir.readAll()

            if comfoAir.Stufe == -1:
                errors["base"] = "cant_connect"
            else:
                return await self.async_step_init()
        else:
            return await self.async_step_init()

        return self.async_show_form(
            step_id="connect", errors=errors, data_schema=vol.Schema({})
        )

    async def async_step_init(self, user_input=None):
        """Handle the options step."""
        errors = {}
        if user_input is not None and len(user_input) > 0:
            self.config[CONFIG_MOXA_IP] = user_input[CONFIG_MOXA_IP]
            self.config[CONFIG_UDP_RECEIVE_PORT] = user_input[CONFIG_UDP_RECEIVE_PORT]
            self.config[CONFIG_UDP_SENDPORT] = user_input[CONFIG_UDP_SENDPORT]
            fname = f"{self.config.get(CONF_FRIENDLY_NAME, FRIENDLY_NAME)} ({self.config[CONFIG_MOXA_IP]})"
            # _LOGGER.debug(f"saving config: {self.config}")
            if self.entry:
                self.hass.config_entries.async_update_entry(
                    self.entry, data=self.config
                )
            _LOGGER.info(f"Config saved")
            return self.async_create_entry(
                title=fname, data=self.config if not self.entry else {}
            )

        schema = vol.Schema(
            {
                vol.Required(
                    CONFIG_MOXA_IP,
                    default=self.config.get(CONFIG_MOXA_IP, CONFIG_MOXA_IP_DEFAULT),
                ): cv.string,
                vol.Required(
                    CONFIG_UDP_RECEIVE_PORT,
                    default=self.config.get(
                        CONFIG_UDP_RECEIVE_PORT, CONFIG_UDP_RECEIVE_PORT_DEFAULT
                    ),
                ): cv.positive_int,
                vol.Required(
                    CONFIG_UDP_SENDPORT,
                    default=self.config.get(
                        CONFIG_UDP_SENDPORT, CONFIG_UDP_SENDPORT_DEFAULT
                    ),
                ): cv.positive_int,
            }
        )

        return self.async_show_form(step_id="init", errors=errors, data_schema=schema)
