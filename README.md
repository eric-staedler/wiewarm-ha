# WieWarm Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)

Monitor water temperatures of Swiss public swimming pools (Bäder) via [wiewarm.ch](https://www.wiewarm.ch).

One temperature sensor is created per pool basin (Becken) for the configured Badi.

---

## Installation

### Via HACS (recommended)

1. Open HACS in Home Assistant
2. Go to **Integrations** → click the three-dot menu → **Custom repositories**
3. Add `https://github.com/YOUR_GITHUB_USERNAME/wiewarm-ha` with category **Integration**
4. Search for **WieWarm** and install it
5. Restart Home Assistant

### Manual

1. Copy the `custom_components/wiewarm` folder into your Home Assistant `config/custom_components/` directory
2. Restart Home Assistant

---

## Configuration

1. Go to **Settings → Integrations → Add Integration**
2. Search for **WieWarm**
3. Enter the **Badi ID** for your local swimming pool

### Finding the Badi ID

Visit [wiewarm.ch](https://www.wiewarm.ch) and open the detail page of your Badi. The ID is the number at the end of the URL:

```
https://www.wiewarm.ch/badi/detail/1   →  Badi ID: 1
```

You can add multiple Badis by setting up the integration multiple times with different IDs.

---

## Sensors

For each configured Badi, one sensor is created per basin:

| Attribute | Description |
|---|---|
| State | Current water temperature in °C (`unavailable` if no data) |
| `beckenid` | Basin identifier from wiewarm.ch |
| `last_updated` | Timestamp of the last temperature reading |

Sensors are updated every **30 minutes**.

---

## License

[MIT](LICENSE)
