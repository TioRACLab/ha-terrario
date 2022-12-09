from __future__ import annotations

import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import TerrarioCoordinator
from .base_entity import TerrarioBaseEntity
from .const import DOMAIN

SENSORS = [
    {
        "name": "Terrário",
        "id": "terrario.status",
        "options": {
            "on": None,
            "auto": None,
            "off": None
        },
        "icon": "mdi:terrain"
    },
    {
        "name": "Terrário Nível Lago",
        "id": "terrario.lake.level",
        "options": {
            "vazio": None,
            "baixo": 8,
            "medio": 4,
            "alto": 12
        },
        "icon": "mdi:waves-arrow-up"
    },
    {
        "name": "Terrário Nível Reservatório",
        "id": "terrario.tank.level",
        "options": {
            "vazio": None,
            "alto": 64
        },
        "icon": "mdi:car-coolant-level"
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

    sensors = list()

    for sensorsConfig in SENSORS:
        sensor =TerrarioSensorEntity(coordinator,
                                    sensorsConfig["id"],
                                    sensorsConfig["name"],
                                    sensorsConfig["icon"],
                                    sensorsConfig["options"])

        sensors.append(sensor)
    
    async_add_entities(sensors)

class TerrarioSensorEntity(TerrarioBaseEntity, SensorEntity):
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
    def native_value(self):
        """Return the state of the requested attribute."""

        # return getattr(self._attr_status, self.attribute, None)
        return self._status

    @property
    def options(self) -> list:
        return list(self._options.keys())