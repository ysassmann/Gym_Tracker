import csv
import json
import os
import sqlite3
import time
from io import StringIO
from pathlib import Path

import psycopg
import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
from streamlit.errors import StreamlitSecretNotFoundError
from streamlit_cookies_controller import CookieController

from program import DAY_LBL, DAYS, DELOAD, RPE_L, cnt_done, day_exs, sk

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent
JSON_PATH = BASE_DIR / "gymtracker_state.json"
DB_PATH = BASE_DIR / "gymtracker_state.sqlite3"
PG_KEYS = ("PGHOST", "PGPORT", "PGDATABASE", "PGUSER", "PGPASSWORD")
AUTH_COOKIE = "gt_auth_until"
DAY_COOKIE = "gt_day"
WEEK_COOKIE = "gt_week"
AUTH_SECONDS = 90 * 60
LOCATION_SECONDS = 60 * 60 * 24 * 90


def cfg(key: str):
    v = os.getenv(key)
    if v:
        return v
    try:
        return st.secrets.get(key)
    except StreamlitSecretNotFoundError:
        return None


def expected_password() -> str:
    v = os.getenv("GYM_APP_PASSWORD")
    if v:
        return v
    try:
        return str(st.secrets["GYM_APP_PASSWORD"])
    except (StreamlitSecretNotFoundError, KeyError):
        return "Gym!"


def int_cookie(cookies: CookieController, key: str, default: int) -> int:
    v = cookies.get(key)
    return int(v) if str(v).isdigit() else default


def save_location(cookies: CookieController, week: int, day: str) -> None:
    cookies.set(WEEK_COOKIE, str(week), max_age=LOCATION_SECONDS, same_site="lax", secure=True)
    cookies.set(DAY_COOKIE, day, max_age=LOCATION_SECONDS, same_site="lax", secure=True)


def cookie_auth_ok(cookies: CookieController) -> bool:
    until = int_cookie(cookies, AUTH_COOKIE, 0)
    return until > int(time.time())


def sqlite_conn() -> sqlite3.Connection:
    c = sqlite3.connect(DB_PATH)
    c.execute("CREATE TABLE IF NOT EXISTS kv (k TEXT PRIMARY KEY, v TEXT NOT NULL)")
    return c


def load_sqlite_or_json_db() -> dict:
    if DB_PATH.is_file():
        with sqlite_conn() as c:
            rows = c.execute("SELECT k, v FROM kv").fetchall()
        if rows:
            return {k: json.loads(v) for k, v in rows}
    if not JSON_PATH.is_file():
        return {}
    db = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    save_sqlite_db(db)
    return db


def save_sqlite_db(db: dict) -> None:
    with sqlite_conn() as c:
        c.execute("DELETE FROM kv")
        c.executemany("INSERT INTO kv (k, v) VALUES (?, ?)", [(k, json.dumps(v, ensure_ascii=False)) for k, v in db.items()])


def pg_ready() -> bool:
    return all(cfg(k) for k in PG_KEYS)


def pg_conn() -> psycopg.Connection:
    c = psycopg.connect(
        host=cfg("PGHOST"),
        port=int(cfg("PGPORT")),
        dbname=cfg("PGDATABASE"),
        user=cfg("PGUSER"),
        password=cfg("PGPASSWORD"),
        sslmode=cfg("PGSSLMODE") or "require",
        connect_timeout=5,
    )
    with c.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS gym_kv (
              user_id TEXT NOT NULL DEFAULT 'default',
              k TEXT NOT NULL,
              v JSONB NOT NULL,
              updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
              PRIMARY KEY (user_id, k)
            )
            """
        )
    c.commit()
    return c


def load_pg_db() -> dict:
    with pg_conn() as c, c.cursor() as cur:
        cur.execute("SELECT k, v::text FROM gym_kv WHERE user_id = %s", ("default",))
        rows = cur.fetchall()
    return {k: json.loads(v) for k, v in rows}


def save_pg_db(db: dict) -> None:
    rows = [("default", k, json.dumps(v, ensure_ascii=False)) for k, v in db.items()]
    if not rows:
        return
    with pg_conn() as c, c.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO gym_kv (user_id, k, v)
            VALUES (%s, %s, %s::jsonb)
            ON CONFLICT (user_id, k)
            DO UPDATE SET v = EXCLUDED.v, updated_at = now()
            """,
            rows,
        )
        c.commit()


def load_db() -> dict:
    ready = pg_ready()
    if not ready:
        db = load_sqlite_or_json_db()
        return db
    db = load_pg_db()
    if db:
        return db
    local = load_sqlite_or_json_db()
    if local:
        save_pg_db(local)
    return local


def save_db(db: dict) -> None:
    target = "postgres" if pg_ready() else "local"
    if target == "postgres":
        save_pg_db(db)
    else:
        save_sqlite_db(db)


def ensure_db():
    if "db" not in st.session_state:
        st.session_state.db = load_db()
    if "saved_at" not in st.session_state:
        st.session_state.saved_at = "—"


def persist_values(keys: list[str]):
    ch = False
    for k in keys:
        if k in st.session_state and st.session_state.db.get(k) != st.session_state[k]:
            st.session_state.db[k] = st.session_state[k]
            ch = True
    if ch:
        save_db(st.session_state.db)
        st.session_state.saved_at = time.strftime("%H:%M:%S")


def persist_key(key: str):
    persist_values([key])


def as_float(v, d=0.0):
    if isinstance(v, bool):
        return d
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        s = v.strip().replace(",", ".")
        if s and s != "—":
            try:
                return float(s)
            except ValueError:
                return d
    return d


def as_int(v, d=0):
    if isinstance(v, bool):
        return d
    if isinstance(v, int):
        return v
    if isinstance(v, float):
        return int(v)
    if isinstance(v, str):
        s = v.strip().replace(",", ".")
        if s and s != "—":
            try:
                return int(float(s))
            except ValueError:
                return d
    return d


def init_widget(key: str, default):
    if key not in st.session_state:
        v = st.session_state.db.get(key, default)
        if isinstance(default, bool):
            st.session_state[key] = bool(v)
        elif isinstance(default, int):
            if isinstance(v, bool):
                st.session_state[key] = 0
            elif isinstance(v, (int, float)):
                st.session_state[key] = int(v)
            elif isinstance(v, str) and v.strip().replace(".", "", 1).isdigit():
                st.session_state[key] = int(float(v))
            else:
                st.session_state[key] = 0
        elif isinstance(default, float):
            if isinstance(v, bool):
                st.session_state[key] = 0.0
            elif isinstance(v, (int, float)):
                st.session_state[key] = float(v)
            elif isinstance(v, str):
                s = v.strip().replace(",", ".")
                if s and s not in ("—", "–"):
                    try:
                        st.session_state[key] = float(s)
                    except ValueError:
                        st.session_state[key] = 0.0
                else:
                    st.session_state[key] = 0.0
            else:
                st.session_state[key] = 0.0
        else:
            st.session_state[key] = "" if v is None else str(v)


def week_stats(db: dict, w: int) -> tuple[int, int]:
    td = tt = 0
    done_days = 0
    for d in DAYS:
        c, t = cnt_done(db, w, d)
        td += c
        tt += t
        if t > 0 and c == t:
            done_days += 1
    pct = round(td / tt * 100) if tt else 0
    return pct, done_days


def active_day_keys(exs: list[dict], w: int, d: str, k_rpe: str, k_sn: str) -> list[str]:
    return (
        [k_rpe, k_sn]
        + [sk(w, d, e["id"], "chk") for e in exs]
        + [k for e in exs if not e.get("noinput") for k in (sk(w, d, e["id"], "aw"), sk(w, d, e["id"], "ar"), sk(w, d, e["id"], "an"))]
    )


def build_csv(db: dict) -> str:
    buf = StringIO()
    wr = csv.writer(buf)
    wr.writerow(["woche", "tag", "tag_label", "uebung_id", "uebung", "aufwarmen", "erledigt", "gewicht", "wdh", "notiz", "rpe", "session_notizen"])
    for week in range(1, 25):
        for d in DAYS:
            rpe = db.get(sk(week, d, "_", "rpe"), "")
            sn = db.get(sk(week, d, "_", "sn"), "")
            for e in day_exs(d, week):
                wr.writerow(
                    [
                        week,
                        d,
                        DAY_LBL[d],
                        e["id"],
                        e["name"],
                        e.get("wu", False),
                        db.get(sk(week, d, e["id"], "chk"), False),
                        db.get(sk(week, d, e["id"], "aw"), ""),
                        db.get(sk(week, d, e["id"], "ar"), ""),
                        db.get(sk(week, d, e["id"], "an"), ""),
                        rpe,
                        sn,
                    ]
                )
    return buf.getvalue()


def build_summary_text(db: dict, w: int) -> str:
    ph = 1 if w <= 8 else (2 if w <= 16 else 3)
    dl = w in DELOAD
    lines = [f"=== WOCHE {w} – Phase {ph}{' (DELOAD)' if dl else ''} ===", ""]
    for d in DAYS:
        c, t = cnt_done(db, w, d)
        rpe = db.get(sk(w, d, "_", "rpe"), 0) or 0
        sn = db.get(sk(w, d, "_", "sn"), "")
        hdr = f"TAG {d} – {DAY_LBL[d]} | {c}/{t} erledigt"
        if rpe:
            hdr += f" | RPE {rpe}/10"
        lines.append(hdr)
        for e in [x for x in day_exs(d, w) if not x.get("wu")]:
            done = db.get(sk(w, d, e["id"], "chk"), False)
            aw, ar, an = db.get(sk(w, d, e["id"], "aw")), db.get(sk(w, d, e["id"], "ar")), db.get(sk(w, d, e["id"], "an"))
            parts = ["[x]" if done else "[ ]", e["name"]]
            if e.get("tgt") not in (None, "", "–"):
                parts.append(f"Ziel: {e['tgt']} {e.get('unit', '')}")
            if aw:
                parts.append(f"erreicht: {aw} {e.get('unit', '')}")
            if ar:
                parts.append(f"x{ar}")
            if an:
                parts.append(str(an))
            lines.append("  " + " | ".join(parts))
        if sn:
            lines.append(f"  Session-Notiz: {sn}")
        lines.append("")
    return "\n".join(lines)


st.set_page_config(page_title="Training", layout="centered", initial_sidebar_state="collapsed")
cookies = CookieController()

components.html(
    """
    <script>
    (() => {
      try {
        const KEY = 'gt_auth_until';
        const RELOAD_FLAG = 'gt_auth_reloaded';
        const now = Math.floor(Date.now() / 1000);
        const doc = window.parent.document;
        const m = doc.cookie.match(/(?:^|;\\s*)gt_auth_until=(\\d+)/);
        const cookieVal = m ? parseInt(m[1], 10) : 0;
        const stored = parseInt(window.parent.localStorage.getItem(KEY) || '0', 10);
        if (cookieVal > stored && cookieVal > now) {
          window.parent.localStorage.setItem(KEY, String(cookieVal));
          window.parent.sessionStorage.removeItem(RELOAD_FLAG);
          return;
        }
        if (stored <= now && cookieVal <= now) {
          window.parent.sessionStorage.removeItem(RELOAD_FLAG);
          return;
        }
        if (stored > cookieVal && stored > now) {
          const maxAge = stored - now;
          doc.cookie = `${KEY}=${stored}; path=/; max-age=${maxAge}; SameSite=Lax; Secure`;
          if (!window.parent.sessionStorage.getItem(RELOAD_FLAG)) {
            window.parent.sessionStorage.setItem(RELOAD_FLAG, '1');
            window.parent.location.reload();
          }
        }
      } catch (e) {}
    })();
    </script>
    """,
    height=0,
)

if "auth_ok" not in st.session_state:
    st.session_state.auth_ok = cookie_auth_ok(cookies)

if not st.session_state.auth_ok:
    st.title("Training")
    st.caption("Geschützter Zugang")
    st.text_input("Passwort", type="password", key="gate_pw")
    if st.button("Anmelden"):
        if st.session_state.get("gate_pw", "") == expected_password():
            st.session_state.auth_ok = True
            until = int(time.time()) + AUTH_SECONDS
            cookies.set(
                AUTH_COOKIE,
                str(until),
                max_age=AUTH_SECONDS,
                same_site="lax",
                secure=True,
            )
            components.html(
                f"""
                <script>
                  try {{
                    window.parent.localStorage.setItem('gt_auth_until', '{until}');
                    setTimeout(() => window.parent.location.reload(), 400);
                  }} catch(e) {{}}
                </script>
                """,
                height=0,
            )
        else:
            st.error("Falsches Passwort")
    st.stop()

ensure_db()
db = st.session_state.db

if "week" not in st.session_state:
    week_cookie = int_cookie(cookies, WEEK_COOKIE, 1)
    st.session_state.week = max(1, min(24, week_cookie))
if "day" not in st.session_state:
    day_cookie = cookies.get(DAY_COOKIE)
    st.session_state.day = day_cookie if day_cookie in DAYS else "A"

w = st.session_state.week
d = st.session_state.day
ph = 1 if w <= 8 else (2 if w <= 16 else 3)

st.markdown(
    """
    <style>
      :root {
        --gt-bg2:#f5f5f7; --gt-bg3:#ebebed; --gt-txt:#1c1c1e; --gt-txt2:#6e6e73; --gt-txt3:#aeaeb2;
        --gt-border:rgba(60,60,67,.13); --gt-border2:rgba(60,60,67,.25);
        --gt-blue:#0071e3; --gt-green:#34c759; --gt-red:#ff3b30; --gt-orange:#ff9500;
        --gt-info-bg:#e8f0fd; --gt-info-txt:#0071e3; --gt-warn-bg:#fff3e0; --gt-warn-txt:#c46000;
      }
      @media (prefers-color-scheme: dark) {
        :root {
          --gt-bg2:#2c2c2e; --gt-bg3:#3a3a3c; --gt-txt:#f5f5f7; --gt-txt2:#aeaeb2; --gt-txt3:#636366;
          --gt-border:rgba(255,255,255,.12); --gt-border2:rgba(255,255,255,.22);
          --gt-blue:#4da3ff; --gt-green:#30d158; --gt-info-bg:#002760; --gt-info-txt:#4da3ff;
          --gt-warn-bg:#3d2500; --gt-warn-txt:#ff9f0a;
        }
      }
      .block-container {max-width: 430px; padding: .7rem .9rem 5rem;}
      .gt-topbar {display:flex; align-items:center; justify-content:space-between; padding:.25rem 0 .45rem; border-bottom:.5px solid var(--gt-border);}
      .gt-title {font-size:1.05rem; font-weight:650; color:var(--gt-txt);}
      .gt-week-label {font-size:.9rem; font-weight:550; color:var(--gt-txt2); text-align:center; padding-top:.55rem;}
      .gt-pills {display:flex; gap:.45rem; align-items:center; margin:.7rem 0 .55rem;}
      .gt-pill {font-size:.75rem; font-weight:600; padding:.22rem .7rem; border-radius:999px; background:var(--gt-info-bg); color:var(--gt-info-txt);}
      .gt-pill.warn {background:var(--gt-warn-bg); color:var(--gt-warn-txt);}
      .gt-stats {display:grid; grid-template-columns:repeat(3,1fr); gap:.5rem; margin:.35rem 0 .75rem;}
      .gt-stat {background:var(--gt-bg2); border-radius:10px; padding:.6rem .7rem;}
      .gt-stat-val {font-size:1.35rem; font-weight:700; color:var(--gt-txt); line-height:1.05;}
      .gt-stat-lbl {font-size:.68rem; color:var(--gt-txt3); margin-top:.1rem;}
      .gt-meta {font-size:.72rem; color:var(--gt-txt3); margin:.1rem 0 .65rem;}
      .gt-sec {font-size:.76rem; font-weight:750; color:var(--gt-txt3); text-transform:uppercase; letter-spacing:.04em; margin:1rem 0 .35rem;}
      .gt-badges {display:flex; flex-wrap:wrap; gap:.3rem; margin:.25rem 0 .35rem;}
      .gt-badge {display:inline-block; background:var(--gt-info-bg); color:var(--gt-info-txt); font-size:.78rem; font-weight:650; padding:.22rem .55rem; border-radius:7px;}
      .gt-badge.alt {background:var(--gt-bg2); color:var(--gt-txt3);}
      .gt-card-title {font-size:1.13rem; font-weight:700; color:var(--gt-txt); line-height:1.25; padding-top:.08rem;}
      .gt-presc {font-size:.96rem; color:var(--gt-txt2); line-height:1.35; margin-top:.12rem;}
      .gt-warn {background:var(--gt-warn-bg); color:var(--gt-warn-txt); border-radius:10px; padding:.65rem .8rem; font-size:.82rem; margin:.45rem 0;}
      div[data-testid="stVerticalBlockBorderWrapper"] {border-color:var(--gt-border) !important; border-radius:14px !important; padding:.05rem 0 !important;}
      div[data-testid="stButton"] > button {border-radius:14px; min-height:2.75rem; font-weight:650;}
      div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea, div[data-testid="stNumberInput"] input {border-radius:10px; background:var(--gt-bg2);}
      div[data-testid="stCheckbox"] {padding:.1rem 0; min-height:3rem;}
      div[data-testid="stCheckbox"] label {font-size:1.15rem; min-height:3rem; display:flex; align-items:center;}
      div[data-testid="stCheckbox"] input {transform:scale(1.9); margin:.45rem;}
      div[data-testid="stSegmentedControl"] {margin:.1rem 0 .55rem;}
      div[data-testid="stSegmentedControl"] button {border-radius:10px !important; min-height:2.55rem;}
    </style>
    """,
    unsafe_allow_html=True,
)
components.html(
    """
    <script>
    (() => {
      try {
        const key = "gymtracker_scroll_y";
        const root = window.parent;
        const store = root.localStorage;
        const restore = () => {
          const y = Number(store.getItem(key) || 0);
          if (y > 0) root.scrollTo(0, y);
        };
        restore();
        setTimeout(restore, 350);
        setTimeout(restore, 900);
        let last = 0;
        root.addEventListener("scroll", () => {
          const now = Date.now();
          if (now - last > 250) {
            store.setItem(key, String(root.scrollY || 0));
            last = now;
          }
        }, {passive: true});
      } catch (_) {}
    })();
    </script>
    """,
    height=0,
)

cap = f"Phase {ph}"
if w in DELOAD:
    cap += " · Deload"
pct, dc = week_stats(db, w)

st.markdown('<div class="gt-topbar"><div class="gt-title">Training</div></div>', unsafe_allow_html=True)
x1, x2, x3 = st.columns([1, 2, 1])
with x1:
    if st.button("‹", use_container_width=True):
        st.session_state.week = max(1, w - 1)
        save_location(cookies, st.session_state.week, st.session_state.day)
        st.rerun()
with x2:
    st.markdown(f'<div class="gt-week-label">Wo {w}</div>', unsafe_allow_html=True)
with x3:
    if st.button("›", use_container_width=True):
        st.session_state.week = min(24, w + 1)
        save_location(cookies, st.session_state.week, st.session_state.day)
        st.rerun()

st.markdown(
    f"""
    <div class="gt-pills">
      <span class="gt-pill">Phase {ph}</span>
      {'<span class="gt-pill warn">Deload</span>' if w in DELOAD else ''}
    </div>
    <div class="gt-stats">
      <div class="gt-stat"><div class="gt-stat-val">{pct}%</div><div class="gt-stat-lbl">Woche</div></div>
      <div class="gt-stat"><div class="gt-stat-val">{dc}/{len(DAYS)}</div><div class="gt-stat-lbl">Tage</div></div>
      <div class="gt-stat"><div class="gt-stat-val">{w}/24</div><div class="gt-stat-lbl">Woche</div></div>
    </div>
    <div class="gt-meta">Gespeichert: {st.session_state.saved_at} · Backend: {'Postgres' if pg_ready() else 'SQLite lokal'}</div>
    """,
    unsafe_allow_html=True,
)
if w in DELOAD:
    st.markdown('<div class="gt-warn">Deload-Woche: alle Sätze halbieren, Gewicht gleich lassen</div>', unsafe_allow_html=True)

opts = [f"{x} · {DAY_LBL[x][:6]}" for x in DAYS]
idx = DAYS.index(d)
if hasattr(st, "segmented_control"):
    cur = opts[idx]
    day_sel = st.segmented_control("Tag", opts, selection_mode="single", default=cur, label_visibility="collapsed")
    st.session_state.day = day_sel[:1] if day_sel else DAYS[idx]
else:
    choice = st.radio("Tag", range(len(DAYS)), horizontal=True, format_func=lambda i: opts[i], index=idx, label_visibility="collapsed")
    st.session_state.day = DAYS[choice]
save_location(cookies, w, st.session_state.day)
d = st.session_state.day

exs = day_exs(d, w)
wus = [e for e in exs if e.get("wu")]
mains = [e for e in exs if not e.get("wu")]


def ex_block(e: dict, warmup: bool):
    k_chk = sk(w, d, e["id"], "chk")
    init_widget(k_chk, False)
    with st.container(border=True):
        ca, cb = st.columns([1, 5])
        with ca:
            st.checkbox("✓", key=k_chk, on_change=persist_key, args=(k_chk,), label_visibility="collapsed")
        with cb:
            badge = '<span class="gt-badge alt">warmup</span>' if warmup else ""
            st.markdown(f'<div class="gt-card-title">{e["name"]} {badge}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="gt-presc">{e["presc"]}</div>', unsafe_allow_html=True)
            badges = []
            if e.get("tgt") not in (None, "", "–"):
                badges.append(f'<span class="gt-badge">Ziel: {e["tgt"]} {e.get("unit", "")}</span>')
            if e.get("alt"):
                badges.append(f'<span class="gt-badge alt">{e["alt"]}</span>')
            if badges:
                st.markdown(f'<div class="gt-badges">{"".join(badges)}</div>', unsafe_allow_html=True)
        if not warmup and not e.get("noinput"):
            u = e.get("unit") or "kg"
            k_aw, k_ar, k_an = sk(w, d, e["id"], "aw"), sk(w, d, e["id"], "ar"), sk(w, d, e["id"], "an")
            init_widget(k_aw, 0.0)
            init_widget(k_ar, 0)
            init_widget(k_an, "")
            i1, i2 = st.columns(2)
            with i1:
                st.number_input(f"Erreicht ({u})", key=k_aw, min_value=0.0, step=0.5, format="%g", on_change=persist_key, args=(k_aw,))
            with i2:
                st.number_input("Reps", key=k_ar, min_value=0, step=1, on_change=persist_key, args=(k_ar,))
            st.text_input("Notiz", key=k_an, placeholder="Notiz...", on_change=persist_key, args=(k_an,))


if wus:
    st.markdown('<div class="gt-sec">Warmup</div>', unsafe_allow_html=True)
    for e in wus:
        ex_block(e, True)

st.markdown('<div class="gt-sec">Hauptübungen</div>', unsafe_allow_html=True)
for e in mains:
    ex_block(e, False)

if st.button("Werte aus Vorwoche uebernehmen", use_container_width=True, disabled=w <= 1):
    for e in [x for x in exs if not x.get("noinput")]:
        p_aw, c_aw = sk(w - 1, d, e["id"], "aw"), sk(w, d, e["id"], "aw")
        p_ar, c_ar = sk(w - 1, d, e["id"], "ar"), sk(w, d, e["id"], "ar")
        if p_aw in db:
            st.session_state[c_aw] = as_float(db[p_aw], st.session_state.get(c_aw, 0.0))
        if p_ar in db:
            st.session_state[c_ar] = as_int(db[p_ar], st.session_state.get(c_ar, 0))
    persist_values([sk(w, d, e["id"], f) for e in exs if not e.get("noinput") for f in ("aw", "ar")])
    st.rerun()

k_rpe = sk(w, d, "_", "rpe")
init_widget(k_rpe, 0)
v_rpe = st.session_state[k_rpe]
if v_rpe not in range(11):
    if isinstance(v_rpe, bool):
        x = 0
    elif isinstance(v_rpe, (int, float)):
        x = max(0, min(10, int(v_rpe)))
    elif isinstance(v_rpe, str) and v_rpe.strip().replace(".", "", 1).replace("-", "", 1).isdigit():
        x = max(0, min(10, int(float(v_rpe))))
    else:
        x = 0
    st.session_state[k_rpe] = x
    st.session_state.db[k_rpe] = x
    save_db(st.session_state.db)
with st.container(border=True):
    st.markdown('<div class="gt-card-title">Wie anstrengend? (RPE)</div>', unsafe_allow_html=True)
    if hasattr(st, "segmented_control"):
        rv = st.segmented_control("Wie anstrengend? (RPE)", list(range(11)), default=int(st.session_state[k_rpe]), selection_mode="single", format_func=lambda x: "—" if x == 0 else str(x), label_visibility="collapsed")
        st.session_state[k_rpe] = int(rv or 0)
        persist_key(k_rpe)
    else:
        st.radio(
            "Wie anstrengend? (RPE)",
            list(range(11)),
            horizontal=True,
            format_func=lambda x: "—" if x == 0 else str(x),
            key=k_rpe,
            on_change=persist_key,
            args=(k_rpe,),
            label_visibility="collapsed",
        )
    rv = int(st.session_state[k_rpe])
    if rv and rv in RPE_L:
        st.caption(f"RPE {rv} — {RPE_L[rv]}")
    if rv >= 9:
        st.caption("Gewicht nächste Woche NICHT steigern!")

k_sn = sk(w, d, "_", "sn")
init_widget(k_sn, "")
with st.container(border=True):
    st.text_area(
        "Session-Notizen",
        key=k_sn,
        placeholder="Schmerzen, Energie, Besonderheiten...",
        on_change=persist_key,
        args=(k_sn,),
        height=88,
    )

persist_values(
    active_day_keys(exs, w, d, k_rpe, k_sn)
)

cd, ct = cnt_done(db, w, d)
all_done = ct > 0 and cd == ct
with st.container(border=True):
    st.caption("Tag abgeschlossen ✓" if all_done else f"Hauptübungen: {cd}/{ct}")
    a1, a2 = st.columns([1, 1])
    with a1:
        if st.button("Jetzt speichern", use_container_width=True):
            persist_values(active_day_keys(exs, w, d, k_rpe, k_sn))
    with a2:
        if st.button("Alle abhaken", use_container_width=True):
            flip = all(db.get(sk(w, d, e["id"], "chk"), False) for e in mains) if mains else False
            for e in mains:
                k = sk(w, d, e["id"], "chk")
                nv = not flip
                st.session_state.db[k] = nv
                st.session_state[k] = nv
            save_db(st.session_state.db)
            st.rerun()

with st.expander("Export"):
    st.download_button("CSV (alle Wochen)", build_csv(db).encode("utf-8"), "gym_tracker_export.csv", "text/csv", on_click="ignore", use_container_width=True)
    st.download_button(
        "JSON-Backup",
        json.dumps(db, ensure_ascii=False, indent=2).encode("utf-8"),
        "gym_tracker_backup.json",
        "application/json",
        on_click="ignore",
        use_container_width=True,
    )
    st.download_button("Wochenzusammenfassung (.txt)", build_summary_text(db, w).encode("utf-8"), f"gym_woche_{w}.txt", "text/plain", on_click="ignore", use_container_width=True)

with st.expander("Hosting-Hinweise"):
    st.markdown(
        "- **Empfohlen:** Streamlit Cloud mit Supabase Postgres.\n"
        "- **Fallback:** lokal auf dem PC nur im selben Netzwerk/VPN.\n"
        "- **Speicher:** SQLite ist lokal, Postgres ist dauerhaft."
    )
