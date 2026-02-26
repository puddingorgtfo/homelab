# Zigbee2MQTT + Mosquitto

Two services in one compose stack:

- **Zigbee2MQTT** — bridges a Zigbee USB coordinator to MQTT. Translates Zigbee device
  messages into MQTT topics that Home Assistant can subscribe to.
- **Mosquitto** — MQTT message broker. The communication backbone between Zigbee2MQTT
  and Home Assistant.

## Ports

| Port | Purpose |
|------|---------|
| 8080 | Zigbee2MQTT web UI |
| 1883 | Mosquitto MQTT broker |

## Setup

### 1. Connect the Zigbee USB coordinator

Add the coordinator device to the compose.yml under zigbee2mqtt volumes:
```yaml
devices:
  - /dev/serial/by-id/usb-ITead_Sonoff_Zigbee_3.0_USB_Dongle_Plus_...:/dev/ttyUSB0
```
Use `ls /dev/serial/by-id/` to find the exact device path.

### 2. Configure Zigbee2MQTT

Edit the config file in the `zigbee_zigbee2mqtt_data` volume at `/app/data/configuration.yaml`:
```yaml
mqtt:
  base_topic: zigbee2mqtt
  server: mqtt://mosquitto
serial:
  port: /dev/ttyUSB0
```

### 3. Configure Mosquitto

Create `mosquitto.conf` in the `zigbee_mosquitto_config` volume:
```
listener 1883
allow_anonymous true
```

### 4. Pair devices

Open the Zigbee2MQTT web UI → enable join mode → press the pair button on your Zigbee device.

## Notes

- Once paired in Z2M, devices appear automatically in Home Assistant via the MQTT integration.
- Z2M web UI is useful for checking device state, renaming devices, and updating firmware.
- Mosquitto `allow_anonymous true` is fine for a local LAN setup. Add username/password
  auth if exposing MQTT externally.
- **Zigbee2MQTT docs**: https://www.zigbee2mqtt.io/guide/getting-started/
- **Mosquitto docs**: https://mosquitto.org/documentation/
