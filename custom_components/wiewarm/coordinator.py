from datetime import timedelta
import logging

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import BAD_API_URL, DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class WieWarmCoordinator(DataUpdateCoordinator):
    """Fetches Badi data (names + temperatures) from wiewarm.ch."""

    def __init__(self, hass: HomeAssistant, badi_id: str) -> None:
        self.badi_id = badi_id
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{badi_id}",
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self) -> dict:
        url = BAD_API_URL.format(self.badi_id)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10), allow_redirects=False) as resp:
                    if resp.status != 200:
                        raise UpdateFailed(f"API returned HTTP {resp.status}")
                    data = await resp.json(content_type=None)
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with wiewarm.ch: {err}") from err

        if not isinstance(data, dict) or "becken" not in data:
            raise UpdateFailed("Unexpected API response format")

        return data
