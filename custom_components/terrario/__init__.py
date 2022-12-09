"""Integração Terrário"""

from __future__ import annotations

import voluptuous as vol

import logging
from datetime import timedelta

from homeassistant.helpers import (
    config_validation as cv
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.const import Platform, CONF_HOST

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema(
        {
            vol.Required(CONF_HOST): cv.string
        })
    },
    extra=vol.ALLOW_EXTRA
)

PLATFORMS = [
    # Platform.BINARY_SENSOR,
    # Platform.MEDIA_PLAYER,
    Platform.SENSOR,
    Platform.SWITCH,
    Platform.SELECT,
]

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the xbox component."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up xbox from a config entry."""

    coordinator = TerrarioCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        # Unsub from coordinator updates
        # hass.data[DOMAIN][entry.entry_id]["sensor_unsub"]()
        # hass.data[DOMAIN][entry.entry_id]["binary_sensor_unsub"]()
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

class TerrarioCoordinator(DataUpdateCoordinator):

    def __init__(
        self,
        hass: HomeAssistant
    ) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=10),
        )

        self.status = 0

    async def _async_update_data(self) -> float:
        return 0.0

    def addToStatus(value: int) -> None:
        self.status |= value

    def isStatus(value: int) -> bool:
        return ((self.status & value) == self.status)