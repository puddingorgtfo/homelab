# Mealie

Recipe manager and meal planner. Import recipes from any URL, organise them, plan meals
for the week, and auto-generate a shopping list.

## Ports

| Port | Purpose |
|------|---------|
| 9000 | Web UI |

## Configuration

| Variable | Description |
|----------|-------------|
| `BASE_URL` | Public URL of your Mealie instance |
| `ALLOW_SIGNUP` | `false` to disable open registration |
| `TZ` | Timezone |

## Notes

- Uses SQLite by default (`DB_ENGINE=sqlite`) — no separate database container needed.
- Import a recipe by pasting a URL — Mealie scrapes the ingredients and instructions
  from the page automatically.
- Meal planner integrates with a shopping list that groups ingredients by category.
- REST API available for integrations.
- **Official docs**: https://docs.mealie.io/
