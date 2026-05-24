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
from homeassistant.helpers.device_registry import DeviceInfo
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
        WieWarmSensor(coordinator, badi_id, becken_key, becken_data)
        for becken_key, becken_data in coordinator.data["becken"].items()
    ]
    async_add_entities(entities)


class WieWarmSensor(CoordinatorEntity[WieWarmCoordinator], SensorEntity):
    """Temperature sensor for a single Becken (pool basin)."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_attribution = "Data provided by http://www.wiewarm.ch sowie teilnehmende Badeanstalten und Individuen (CC BY-SA 3.0)"

    def __init__(
        self,
        coordinator: WieWarmCoordinator,
        badi_id: str,
        becken_key: str,
        initial_data: dict,
    ) -> None:
        super().__init__(coordinator)
        self._becken_key = becken_key
        self._becken_id = initial_data.get("beckenid", becken_key)
        self._attr_unique_id = f"wiewarm_{badi_id}_{self._becken_id}"
        self._attr_name = initial_data.get("beckenname") or f"Becken {self._becken_id}"

    @property
    def device_info(self) -> DeviceInfo:
        data = self.coordinator.data
        badname = data.get("badname") or f"Badi {self.coordinator.badi_id}"
        ort = data.get("ort", "")
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.badi_id)},
            name=f"{badname} ({ort})" if ort else badname,
            manufacturer="WieWarm",
            configuration_url=f"https://www.wiewarm.ch/badi/detail/{self.coordinator.badi_id}",
        )

    @property
    def _becken_data(self) -> dict:
        return self.coordinator.data.get("becken", {}).get(self._becken_key, {})

    @property
    def native_value(self) -> float | None:
        raw = self._becken_data.get("temp")
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
        data = self._becken_data
        return {
            "beckenid": data.get("beckenid"),
            "beckenname": data.get("beckenname"),
            "typ": data.get("typ"),
            "status": data.get("status"),
            "last_updated": data.get("date"),
        }
