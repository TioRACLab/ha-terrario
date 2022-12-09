import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from typing import Any, Dict, Optional
from homeassistant.const import CONF_URL
from homeassistant import config_entries, core
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_URL, DOMAIN

TERRARIO_SCHEMA = vol.Schema(
    {vol.Required(CONF_URL): cv.string}
)

async def validate_terrario(url: str, hass: core.HomeAssistant) -> None:
    session = async_get_clientsession(hass)

    try:
        return
    except BadRequest:
        raise ValueError


class TerrarioConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    data: Optional[Dict[str, Any]]

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None):
        errors: Dict[str, str] = {}
        
        if user_input is not None:
            try:
                await validate_terrario(user_input[CONF_URL], self.hass)
                self.data = user_input

                return self.async_create_entry(title="Terrário", data=self.data)
            except ValueError:
                errors["base"] = "url"

        return self.async_show_form(
            step_id="user", data_schema=TERRARIO_SCHEMA, errors=errors
        )