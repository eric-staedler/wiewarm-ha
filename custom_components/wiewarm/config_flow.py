import logging

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import BAD_API_URL, CONF_BADI_ID, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def _fetch_badi(hass: HomeAssistant, badi_id: str) -> dict:
    """Return bad.json data or raise ValueError on invalid ID / unreachable API."""
    url = BAD_API_URL.format(badi_id)
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10), allow_redirects=False) as resp:
            if resp.status != 200:
                raise ValueError("invalid_badi_id")
            data = await resp.json(content_type=None)

    if not isinstance(data, dict) or "becken" not in data:
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
                data = await _fetch_badi(self.hass, badi_id)
            except ValueError:
                errors[CONF_BADI_ID] = "invalid_badi_id"
            except aiohttp.ClientError:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected error during WieWarm setup")
                errors["base"] = "unknown"
            else:
                badname = data.get("badname") or f"Badi {badi_id}"
                ort = data.get("ort", "")
                title = f"{badname} ({ort})" if ort else badname
                return self.async_create_entry(title=title, data={CONF_BADI_ID: badi_id})

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_BADI_ID): str}),
            errors=errors,
        )
