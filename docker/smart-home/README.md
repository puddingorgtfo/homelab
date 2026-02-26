# Smart Home

Home automation stack. Home Assistant is the hub; Mosquitto is the MQTT message broker;
Zigbee2MQTT bridges Zigbee devices (lights, sensors, switches) to MQTT so HA can control them.

## Services

| Service | Description | Port |
|---------|-------------|------|
| [Home Assistant](homeassistant/) | Central home automation hub — automations, dashboards, integrations | 8123 |
| [Zigbee2MQTT](zigbee2mqtt/) | Bridges a Zigbee USB coordinator to MQTT | 8080 (web UI) |
| [Mosquitto](zigbee2mqtt/) | MQTT message broker (runs in the same compose stack as Z2M) | 1883 |

## How They Connect

```
Zigbee devices (lights, sensors, plugs)
    ↓  (radio, 2.4 GHz)
Zigbee USB coordinator (e.g. Sonoff Zigbee 3.0)
    ↓  (USB passthrough to container)
Zigbee2MQTT container
    ↓  (MQTT publish/subscribe)
Mosquitto broker
    ↑  (MQTT subscribe)
Home Assistant
```

Home Assistant can also integrate non-Zigbee devices directly (Z-Wave, Wi-Fi, Matter, etc.)
via its own integrations — the MQTT stack is specifically for Zigbee devices.

## Notes

- The Zigbee USB coordinator must be passed through to the Zigbee2MQTT container. Add the
  device path to the compose.yml volumes (e.g. `/dev/serial/by-id/usb-ITead_Sonoff_Zigbee_3.0_...:/dev/ttyUSB0`).
- Mosquitto config (username/password, persistence) lives in the named volume
  `zigbee_mosquitto_config`. First-time setup requires creating the config file manually.
- Home Assistant config is stored at `/opt/homeassistant/config` (not on NAS, to avoid
  latency with time-sensitive automations).
- Zigbee2MQTT web UI is on port 8080 — useful for pairing new devices and checking
  device state without going into HA.
