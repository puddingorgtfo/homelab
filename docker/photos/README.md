# Photos

Self-hosted photo and video management.

## Services

| Service | Description | Port |
|---------|-------------|------|
| [Immich](immich/) | Photo and video manager — Google Photos alternative with mobile app | 2283 |

## Notes

- Immich has a mobile app (iOS and Android) that auto-backs up your camera roll, just like
  Google Photos. Point it at your Immich server URL.
- Supports Google Takeout import — export your Google Photos library and import it directly.
- Machine learning features (face recognition, object detection) require a CPU or GPU.
  The ML container can be disabled if resources are tight.
- Photo files are stored on the NAS to avoid filling the boot disk.
