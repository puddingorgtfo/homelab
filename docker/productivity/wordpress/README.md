# WordPress

Self-hosted website and blog platform. Runs with a MySQL/MariaDB database backend.

## Ports

| Port | Purpose |
|------|---------|
| 8088 | WordPress web UI |

## Configuration

| Variable | Description |
|----------|-------------|
| `WORDPRESS_DB_PASSWORD` | Database password for WordPress |
| `MYSQL_ROOT_PASSWORD` | MySQL root password |
| `WORDPRESS_DB_USER` | Database username |

## Notes

- First visit to the URL completes the WordPress install wizard.
- Admin panel at `/wp-admin`.
- Plugins and themes are persistent in the data volume.
- For best performance behind NPM, set `WORDPRESS_CONFIG_EXTRA` with the correct
  site URL and ensure `WP_HOME` / `WP_SITEURL` match the proxied domain.
- **Official docs**: https://wordpress.org/support/
