import logging

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import API_URL, CONF_BADI_ID, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def _validate_badi_id(hass: HomeAssistant, badi_id: str) -> dict:
    """Return API data or raise ValueError on invalid ID / unreachable API."""
    url = API_URL.format(badi_id)
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            if resp.status != 200:
                raise ValueError("invalid_badi_id")
            data = await resp.json(content_type=None)

    if not isinstance(data, dict) or not data:
        raise ValueError("invalid_badi_id")

    return data


class WieWarmConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the WieWarm setup flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            badi_id = user_input[CONF_BADI_ID].strip()

            await self.async_set_unique_id(badi_id)
            self._abort_if_unique_id_configured()

            try:
                data = await _validate_badi_id(self.hass, badi_id)
            except ValueError:
                errors[CONF_BADI_ID] = "invalid_badi_id"
            except aiohttp.ClientError:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected error during WieWarm setup")
                errors["base"] = "unknown"
            else:
                # Use the first available pool name hint for the title if possible
                title = f"WieWarm Badi {badi_id}"
                return self.async_create_entry(title=title, data={CONF_BADI_ID: badi_id})

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_BADI_ID): str}),
            errors=errors,
        )
