from __future__ import annotations

import logging

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from . import TerrarioCoordinator
from .base_entity import TerrarioBaseEntity

SWITCHES = [
    {
        "name": "Terrário Luz",
        "id": "terrario.luz.status",
        "icon": "mdi:lightbulb",
        "value": 1
    },
    {
        "name": "Terrário Espectro",
        "id": "terrario.espectro.status",
        "icon": "mdi:lightbulb-cfl",
        "value": 2
    },
    {
        "name": "Terrário Bomba Lago",
        "id": "terrario.pump.lake",
        "icon": "mdi:water-pump",
        "value": 32
    },
    {
        "name": "Terrário Bomba Reservatório",
        "id": "terrario.pump.tank",
        "icon": "mdi:cup-water",
        "value": 64
    },
    {
        "name": "Terrário Válvula Cascata",
        "id": "terrario.valve.waterfall",
        "icon": "mdi:pipe-valve",
        "value": 128
    },
    {
        "name": "Terrário Válvula Irrigação",
        "id": "terrario.valve.irrigation",
        "icon": "mdi:sprinkler",
        "value": 256
    },
    {
        "name": "Terrário Neblina",
        "id": "terrario.fog",
        "icon": "mdi:weather-fog",
        "value": 512
    }
]

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Xbox Live friends."""
    coordinator: TerrarioCoordinator = hass.data[DOMAIN][config_entry.entry_id][
        "coordinator"
    ]

    switches = list()

    for switchConfig in SWITCHES:
        switch = TerrarioSwitchEntity(coordinator,
                                    switchConfig["id"],
                                    switchConfig["name"],
                                    switchConfig["icon"])

        switches.append(switch)

    async_add_entities(switches)

class TerrarioSwitchEntity(TerrarioBaseEntity, SwitchEntity):
    _state: bool = False

    @property
    def is_on(self) -> bool | None:
        return self._state

    def turn_on(self, **kwargs) -> None:
        self._state = True

    def turn_off(self, **kwargs):
        self._state = False

    def toggle(self, **kwargs):
        self._state = not self._state
