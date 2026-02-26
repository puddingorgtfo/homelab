# Home Assistant

Open-source home automation platform. Integrates with thousands of devices and services —
lights, thermostats, sensors, media players, security cameras, and more. Runs automations,
displays dashboards, and acts as a central hub for the smart home stack.

## Ports

| Port | Purpose |
|------|---------|
| 8123 | Web UI and API |

## Smart Home Stack

Home Assistant is the hub for the full stack in this repo:

```
Zigbee devices → Zigbee USB Coordinator → Zigbee2MQTT → Mosquitto (MQTT) → Home Assistant
                                                                          ↑
                                             Wi-Fi/Matter devices ────────┘
```

See [zigbee2mqtt/README.md](../zigbee2mqtt/README.md) and [mosquitto/README.md](../mosquitto/README.md)
for the supporting services.

## Notes

- Configuration (automations, dashboards, integrations) lives at `/opt/homeassistant/config`
  on the host — not on the NAS, to avoid latency with time-sensitive automations.
- After initial HA setup, install the MQTT integration and point it at the Mosquitto container
  (`mosquitto:1883` on the Docker network) to receive Zigbee device states.
- Home Assistant must be in `host` network mode OR have the host network for certain
  integrations that rely on network discovery (mDNS, UPnP). Adjust the compose if needed.
- Backups can be created via HA's built-in backup feature (Settings → System → Backups).
- **Official docs**: https://www.home-assistant.io/docs/
