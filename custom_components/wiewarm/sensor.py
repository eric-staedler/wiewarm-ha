from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_BADI_ID, DOMAIN
from .coordinator import WieWarmCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: WieWarmCoordinator = hass.data[DOMAIN][entry.entry_id]
    badi_id = entry.data[CONF_BADI_ID]

    entities = [
        WieWarmSensor(coordinator, badi_id, basin_key, basin_data)
        for basin_key, basin_data in coordinator.data.items()
    ]
    async_add_entities(entities)


class WieWarmSensor(CoordinatorEntity[WieWarmCoordinator], SensorEntity):
    """Temperature sensor for a single Becken (pool basin)."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(
        self,
        coordinator: WieWarmCoordinator,
        badi_id: str,
        basin_key: str,
        initial_data: dict,
    ) -> None:
        super().__init__(coordinator)
        self._basin_key = basin_key
        self._becken_id = initial_data.get("beckenid", basin_key)
        self._attr_unique_id = f"wiewarm_{badi_id}_{self._becken_id}"
        self._attr_name = f"WieWarm Becken {self._becken_id}"

    @property
    def _basin_data(self) -> dict:
        return self.coordinator.data.get(self._basin_key, {})

    @property
    def native_value(self) -> float | None:
        raw = self._basin_data.get("temp")
        if raw is None:
            return None
        try:
            value = float(raw)
        except (ValueError, TypeError):
            return None
        # API returns 0.0 when no data is available
        return value if value > 0 else None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        data = self._basin_data
        return {
            "beckenid": data.get("beckenid"),
            "last_updated": data.get("date"),
        }
