from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import TerrarioCoordinator
from .const import DOMAIN


class TerrarioBaseEntity(CoordinatorEntity[TerrarioCoordinator]):

    def __init__(
        self, 
        coordinator: TerrarioCoordinator, 
        id: str,
        name: str,
        icon: str = "mdi:terrain"
    ) -> None:
        """Initialize Xbox binary sensor."""
        super().__init__(coordinator)
        self._id = id
        self._name = name
        self._icon = icon

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return self._id

    @property
    def name(self) -> str | None:
        return self._name

    @property
    def icon(self) -> str | None:
        return self._icon

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Return if the entity should be enabled when first added to the entity registry."""
        return True

    @property
    def device_info(self) -> DeviceInfo:
        """Return a device description for device registry."""
        return DeviceInfo(
            # entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN)},
            manufacturer="TioRAC",
            model="Terrário",
            name="Terrário",
        )