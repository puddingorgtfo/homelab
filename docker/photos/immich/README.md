# Immich

Self-hosted photo and video management — a Google Photos alternative with a mobile app,
face recognition, object detection, and shared albums.

## Ports

| Port | Purpose |
|------|---------|
| 2283 | Web UI and mobile app API |

## Configuration

| Variable | Description |
|----------|-------------|
| `IMMICH_DB_PASSWORD` | PostgreSQL database password |
| `IMMICH_PUBLIC_URL` | Public URL of your Immich instance (e.g. `https://photos.yourdomain.com`) |
| `TZ` | Timezone |

## Notes

- **Mobile app**: Available for iOS and Android. Point it at your Immich URL for automatic
  camera roll backup — works like Google Photos.
- **Google Takeout import**: Export your Google Photos library as a Takeout archive and
  import it directly via the web UI (Tools → Google Photos Migration).
- **Machine learning**: Immich runs a separate ML container for face recognition and CLIP
  (object/scene search). Can be disabled if resources are tight.
- Photos are stored on the NAS — do NOT store them in the Docker volume (fills boot disk).
- The database and thumbnail cache are separate from the original photo files.
- **Official docs**: https://immich.app/docs/overview/introduction
