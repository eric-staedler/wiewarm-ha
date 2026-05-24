# WieWarm Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)

Monitor water temperatures of Swiss public swimming pools (Bäder) via [wiewarm.ch](https://www.wiewarm.ch).

One temperature sensor is created per pool basin (Becken) for the configured Badi.

---

## Installation

### Via HACS (recommended)

1. Open HACS in Home Assistant
2. Go to **Integrations** → click the three-dot menu → **Custom repositories**
3. Add `https://github.com/eric-staedler/wiewarm-ha` with category **Integration**
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

Find your Badi in the following json file. 

```
https://www.wiewarm.ch/api/v1/temperature/all_current.json/0
```

```
    {
        "badid": "14", <-- The Badi ID
        "badid_text": "Zürichsee_Zürich",
        "bad": "Zürichsee",
        "ort": "Zürich",
        "plz": "",
        "kanton": "ZH",
        "beckenid": "43",
        "becken": "Tiefenbrunnen",
        "temp": "16.2",
        "date": "2026-05-24 16:30:02",
        "ortlat": "47.366211",
        "ortlong": "8.543380",
        "date_pretty": "heute, 16:30",
        "images": []
    },
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

## Data Source & Attribution

Water temperature data is provided by [wiewarm.ch](http://www.wiewarm.ch) and contributing baths and individuals.

> **http://www.wiewarm.ch sowie teilnehmende Badeanstalten und Individuen**

The dataset from wiewarm.ch is licensed under a [Creative Commons Attribution-ShareAlike 3.0 Unported License](https://creativecommons.org/licenses/by-sa/3.0/).
Based on a work at [http://www.wiewarm.ch](http://www.wiewarm.ch).
Permissions beyond the scope of this license may be available at [info@wiewarm.ch](mailto:info@wiewarm.ch).

---

## License

The integration code is licensed under [MIT](LICENSE).
Data fetched at runtime originates from wiewarm.ch and remains subject to the [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/) license terms above.
