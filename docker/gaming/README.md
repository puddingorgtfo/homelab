# Gaming

ROM management and emulation library.

## Services

| Service | Description | Port |
|---------|-------------|------|
| [RomM](romm/) | ROM manager with metadata scraping, artwork, and multi-platform support | 8085 |

## Notes

- RomM scrapes metadata and artwork for your ROM library automatically — just point it at
  your ROMs directory and it handles the rest.
- Supports a wide range of platforms (NES, SNES, N64, GBA, PS1, PS2, and many more).
- ROMs are stored on the NAS and mounted into the container at `/romm/library`.
- Uses a MariaDB database (`romm-db`) for metadata storage.
- Authentication is enabled via `ROMM_AUTH_SECRET_KEY` — set a strong random key.
