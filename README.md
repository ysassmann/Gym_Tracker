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

- Preferred backend: Supabase Postgres via Streamlit secrets (`PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, `PGPASSWORD`, `PGSSLMODE`).
- Fallback backend: local `gymtracker_state.sqlite3` when Postgres secrets are not set.
- First Postgres start migrates local SQLite/JSON data automatically if remote table is still empty.
- For Streamlit Cloud durability, use Postgres; local files are not guaranteed across app rebuilds.

## Supabase table

```sql
create table if not exists gym_kv (
  user_id text not null default 'default',
  k text not null,
  v jsonb not null,
  updated_at timestamptz not null default now(),
  primary key (user_id, k)
);
```
