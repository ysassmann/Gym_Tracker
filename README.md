# Gym Tracker

Mobile-first Streamlit workout tracker.

## Run

```bash
uv run streamlit run app.py
```1

## iPhone usage at the gym

- Recommended: host on the internet (e.g. Streamlit Community Cloud) so your phone can access it anywhere.
- Connect with Postgres SQL database for permenante data

## Data persistence

- Preferred backend: Supabase Postgres via Streamlit.
- Fallback backend: local `gymtracker_state.sqlite3` when connection to Postgres db is not active.
- First Postgres start migrates local SQLite/JSON data automatically if remote table is still empty.
- For data peristance, use Postgres.
- The app shows the active backend in the UI (`Postgres (Supabase)` or local SQLite fallback).

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
