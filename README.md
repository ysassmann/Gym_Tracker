# Gym Tracker

Mobile-first Streamlit workout tracker.

## Run

```bash
uv run streamlit run app.py
```

## iPhone usage at the gym

- Recommended: host on the internet (e.g. Streamlit Community Cloud) so your phone can access it anywhere.
- Fallback: run on your PC only for same-network access (or VPN).

## Data persistence

- App state is stored in `gymtracker_state.sqlite3`.
- If `gymtracker_state.json` exists and SQLite is empty, data migrates automatically on first load.
- Persistence is only durable if your host keeps files between restarts.
