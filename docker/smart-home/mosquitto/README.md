# Mosquitto

MQTT message broker. In this setup, Mosquitto runs as part of the Zigbee2MQTT compose
stack — see [zigbee2mqtt/README.md](../zigbee2mqtt/README.md) for full configuration details.

## Ports

| Port | Purpose |
|------|---------|
| 1883 | MQTT (unencrypted) |
| 8883 | MQTT over TLS (optional) |

## Notes

- Mosquitto is a lightweight pub/sub broker. Zigbee2MQTT publishes device states to it;
  Home Assistant subscribes to receive them.
- The actual compose file for Mosquitto lives in `zigbee2mqtt/compose.yml` alongside Z2M.
- **Official docs**: https://mosquitto.org/documentation/
