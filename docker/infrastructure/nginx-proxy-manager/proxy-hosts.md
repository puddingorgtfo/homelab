# Nginx Proxy Manager -- Proxy Hosts Reference

| Conf # | Subdomain | Backend Server | Backend Port | SSL | HTTP2 | Notable Custom Config |
|--------|-----------|----------------|--------------|-----|-------|-----------------------|
| 1 | portainer.yourdomain.com | <DOCKER_HOST_IP> | 9443 | Yes | off | Forward scheme HTTPS; `proxy_ssl_verify off`; custom `X-Forwarded-Proto/Port/For` headers; connect/send/read timeouts 60s |
| 2 | paperless.yourdomain.com | <DOCKER_HOST_IP> | 8010 | Yes | off | Custom `Host`, `X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto` headers |
| 3 | npm.yourdomain.com | <DOCKER_HOST_IP> | 81 | Yes | off | `large_client_header_buffers 4 32k`; `client_header_buffer_size 32k` |
| 5 | proxmox.yourdomain.com | <PROXMOX_IP> | 8006 | Yes | off | Forward scheme HTTPS; `proxy_ssl_verify off`; `proxy_redirect off`; read/send timeouts 3600s; connect timeout 60s; custom `X-Forwarded-Proto/Port/For` headers |
| 6 | pihole.yourdomain.com | <DOCKER_HOST_IP> | 8081 | Yes | off | -- |
| 7 | nas.yourdomain.com | <NAS_IP> | 8084 | Yes | off | Asset caching |
| 8 | jellyfin.yourdomain.com | <DOCKER_HOST_IP> | 8096 | Yes | off | Asset caching; custom `X-Forwarded-Proto`, `X-Forwarded-For`, `X-Real-IP`, `Host` headers; `proxy_buffering off` |
| 9 | searxng.yourdomain.com | <DOCKER_HOST_IP> | 8082 | Yes | off | Asset caching |
| 10 | qbit.yourdomain.com | gluetun | 8080 | Yes | on | Asset caching |
| 11 | prowlarr.yourdomain.com | prowlarr | 9696 | Yes | off | Asset caching |
| 12 | sonarr.yourdomain.com | sonarr | 8989 | No | off | Asset caching; HTTP only (no SSL listener) |
| 13 | radarr.yourdomain.com | radarr | 7878 | Yes | off | Asset caching |
| 14 | oversee.yourdomain.com | overseerr | 5055 | Yes | off | Asset caching |
| 15 | plex.yourdomain.com | plex | 32400 | Yes | off | Asset caching |
| 16 | audiobooks.yourdomain.com | audiobookshelf | 80 | Yes | off | Asset caching |
| 17 | readarr.yourdomain.com | readarr | 8787 | Yes | on | Asset caching |
| 18 | zigbee.yourdomain.com | zigbee2mqtt | 8080 | Yes | on | Asset caching |
| 19 | wordpress.yourdomain.com | wp_app | 80 | Yes | off | Asset caching |
| 20 | calibre.yourdomain.com | calibre | 8080 | Yes | off | Asset caching |
| 21 | cloud.yourdomain.com | nextcloud-db | 80 | Yes | on | -- |
| 22 | dumbpad.yourdomain.com | dumbpad | 3000 | Yes | off | Asset caching |
| 23 | homeassistant.yourdomain.com | homeassistant | 8123 | Yes | on | Custom `Host`, `X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto` headers; WebSocket upgrade (`Connection "upgrade"`); `proxy_buffering off` |
| 26 | photos.yourdomain.com | immich-immich-server-1 | 2283 | Yes | off | `client_max_body_size 50000M`; custom `Host`, `X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto` headers |
| 27 | home.yourdomain.com | homepage | 3000 | Yes | off | -- |

## Notes

- All hosts use Let's Encrypt SSL via the shared certificate at `/etc/letsencrypt/live/npm-2/` (except conf 12 which has no SSL).
- All hosts include `block-exploits.conf`.
- All hosts set WebSocket upgrade headers (`Upgrade`, `Connection`) and `proxy_http_version 1.1` at the server level.
- HSTS is configured globally on all hosts (`max-age=63072000; preload`).
- Conf numbers 4, 24, and 25 are absent (deleted or unused).
- Conf 8 uses a slightly different domain variant (minor typo in domain name).
