from __future__ import annotations

import logging

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import TerrarioCoordinator
from .base_entity import TerrarioBaseEntity
from .const import DOMAIN

SELECTS = [
    {
        "name": "Terrário Trem Status",
        "id": "terrario.train.status",
        "options": {
            "off": None,
            "forward": 2048,
            "backward": 4096
        },
        "icon": "mdi:train"
    },
    {
        "name": "Terrário Trem Velocidade",
        "id": "terrario.train.speed",
        "options": {
            "stop": None,
            "slow": 8192,
            "medium": 16384,
            "fast": 32768
        },
        "icon": "mdi:speedometer"
    }
]

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: TerrarioCoordinator = hass.data[DOMAIN][config_entry.entry_id][
        "coordinator"
    ]

    selects = list()

    for selectConfig in SELECTS:
        select =TerrarioSelectEntity(coordinator,
                                    selectConfig["id"],
                                    selectConfig["name"],
                                    selectConfig["icon"],
                                    selectConfig["options"])

        selects.append(select)
    
    async_add_entities(selects)

class TerrarioSelectEntity(TerrarioBaseEntity, SelectEntity):
    """Representation of a Xbox presence state."""

    def __init__(
            self, 
            coordinator: TerrarioCoordinator, 
            id: str,
            name: str,
            icon: str,
            options: dict
        ) -> None:
        """Initialize Xbox binary sensor."""
        super().__init__(coordinator, id, name, icon)
        self._options = options
        self._status = list(options.keys())[0]

    @property
    def current_option(self):
        """Return the state of the requested attribute."""
        return self._status

    @property
    def options(self) -> list:
        return list(self._options.keys())

    def select_option(self, option: str) -> None:
        self._status = option