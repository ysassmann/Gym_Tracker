import csv
import json
import os
import sqlite3
import time
from io import StringIO
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from streamlit.errors import StreamlitSecretNotFoundError

from program import DAY_LBL, DAYS, DELOAD, RPE_L, cnt_done, day_exs, sk

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent
JSON_PATH = BASE_DIR / "gymtracker_state.json"
DB_PATH = BASE_DIR / "gymtracker_state.sqlite3"


def expected_password() -> str:
    v = os.getenv("GYM_APP_PASSWORD")
    if v:
        return v
    try:
        return str(st.secrets["GYM_APP_PASSWORD"])
    except (StreamlitSecretNotFoundError, KeyError):
        return "Gym!"


def conn() -> sqlite3.Connection:
    c = sqlite3.connect(DB_PATH)
    c.execute("CREATE TABLE IF NOT EXISTS kv (k TEXT PRIMARY KEY, v TEXT NOT NULL)")
    return c


def load_db() -> dict:
    with conn() as c:
        rows = c.execute("SELECT k, v FROM kv").fetchall()
    if rows:
        return {k: json.loads(v) for k, v in rows}
    if not JSON_PATH.is_file():
        return {}
    db = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    save_db(db)
    return db


def save_db(db: dict) -> None:
    with conn() as c:
        c.execute("DELETE FROM kv")
        c.executemany("INSERT INTO kv (k, v) VALUES (?, ?)", [(k, json.dumps(v, ensure_ascii=False)) for k, v in db.items()])


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

if "auth_ok" not in st.session_state:
    st.session_state.auth_ok = False

if not st.session_state.auth_ok:
    st.title("Training")
    st.caption("Geschützter Zugang")
    st.text_input("Passwort", type="password", key="gate_pw")
    if st.button("Anmelden"):
        if st.session_state.get("gate_pw", "") == expected_password():
            st.session_state.auth_ok = True
            st.rerun()
        st.error("Falsches Passwort")
    st.stop()

ensure_db()
db = st.session_state.db

if "week" not in st.session_state:
    st.session_state.week = 1
if "day" not in st.session_state:
    st.session_state.day = "A"

w = st.session_state.week
d = st.session_state.day
ph = 1 if w <= 8 else (2 if w <= 16 else 3)

st.title("Training")
st.markdown(
    """
    <style>
      .block-container {max-width: 760px; padding-top: 1rem; padding-bottom: 5rem;}
      div[data-testid="stButton"] > button {border-radius: 12px; height: 2.7rem;}
      div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea {border-radius: 10px;}
    </style>
    """,
    unsafe_allow_html=True,
)

x1, x2, x3 = st.columns([1, 2, 1])
with x1:
    if st.button("‹", use_container_width=True):
        st.session_state.week = max(1, w - 1)
        st.rerun()
with x2:
    st.markdown(f"<div style='text-align:center;font-weight:600'>Wo {w} / 24</div>", unsafe_allow_html=True)
with x3:
    if st.button("›", use_container_width=True):
        st.session_state.week = min(24, w + 1)
        st.rerun()

cap = f"Phase {ph}"
if w in DELOAD:
    cap += " · Deload"
st.caption(cap)
if w in DELOAD:
    st.warning("Deload-Woche: alle Sätze halbieren, Gewicht gleich lassen.")

pct, dc = week_stats(db, w)
st.metric("Fortschritt Woche", f"{pct}%")
st.caption(f"Tage fertig: {dc}/{len(DAYS)}")
st.caption(f"Letztes Speichern: {st.session_state.saved_at}")

opts = [f"{x} · {DAY_LBL[x][:6]}" for x in DAYS]
idx = DAYS.index(d)
if hasattr(st, "segmented_control"):
    cur = opts[idx]
    day_sel = st.segmented_control("Tag", opts, selection_mode="single", default=cur, label_visibility="collapsed")
    st.session_state.day = day_sel[:1] if day_sel else DAYS[idx]
else:
    choice = st.radio("Tag", range(len(DAYS)), horizontal=True, format_func=lambda i: opts[i], index=idx, label_visibility="collapsed")
    st.session_state.day = DAYS[choice]
d = st.session_state.day

exs = day_exs(d, w)
wus = [e for e in exs if e.get("wu")]
mains = [e for e in exs if not e.get("wu")]


def ex_block(e: dict, warmup: bool):
    k_chk = sk(w, d, e["id"], "chk")
    init_widget(k_chk, False)
    with st.container(border=True):
        tag = " · Warmup" if warmup else ""
        st.markdown(f"**{e['name']}**{tag}")
        st.caption(e["presc"])
        if e.get("tgt") not in (None, "", "–"):
            st.caption(f"Ziel: {e['tgt']} {e.get('unit', '')}")
        if e.get("alt"):
            st.caption(e["alt"])
        st.checkbox("Erledigt", key=k_chk, on_change=persist_key, args=(k_chk,))
        if not warmup and not e.get("noinput"):
            u = e.get("unit") or "kg"
            k_aw, k_ar, k_an = sk(w, d, e["id"], "aw"), sk(w, d, e["id"], "ar"), sk(w, d, e["id"], "an")
            init_widget(k_aw, 0.0)
            init_widget(k_ar, 0)
            init_widget(k_an, "")
            st.number_input(f"Gewicht ({u})", key=k_aw, min_value=0.0, step=0.5, format="%g", on_change=persist_key, args=(k_aw,))
            st.number_input("Wdh", key=k_ar, min_value=0, step=1, on_change=persist_key, args=(k_ar,))
            st.text_input("Notiz", key=k_an, placeholder="Kurz notieren…", on_change=persist_key, args=(k_an,))


if wus:
    st.subheader("Warmup")
    for e in wus:
        ex_block(e, True)

st.subheader("Hauptübungen")
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
if hasattr(st, "segmented_control"):
    rv = st.segmented_control("Wie anstrengend? (RPE)", list(range(11)), default=int(st.session_state[k_rpe]), selection_mode="single", format_func=lambda x: "—" if x == 0 else str(x))
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
    )
rv = int(st.session_state[k_rpe])
if rv and rv in RPE_L:
    st.caption(f"RPE {rv} — {RPE_L[rv]}")
if rv >= 9:
    st.caption("Gewicht nächste Woche NICHT steigern!")

k_sn = sk(w, d, "_", "sn")
init_widget(k_sn, "")
st.text_area(
    "Session-Notizen",
    key=k_sn,
    placeholder="Schmerzen, Energie, Besonderheiten…",
    on_change=persist_key,
    args=(k_sn,),
    height=88,
)

persist_values(
    [k_rpe, k_sn]
    + [sk(w, d, e["id"], "chk") for e in exs]
    + [k for e in exs if not e.get("noinput") for k in (sk(w, d, e["id"], "aw"), sk(w, d, e["id"], "ar"), sk(w, d, e["id"], "an"))]
)

cd, ct = cnt_done(db, w, d)
all_done = ct > 0 and cd == ct
if st.button("Jetzt speichern", use_container_width=True):
    persist_values(
        [k_rpe, k_sn]
        + [sk(w, d, e["id"], "chk") for e in exs]
        + [k for e in exs if not e.get("noinput") for k in (sk(w, d, e["id"], "aw"), sk(w, d, e["id"], "ar"), sk(w, d, e["id"], "an"))]
    )
if st.button("Alle Hauptübungen abhaken / lösen"):
    flip = all(db.get(sk(w, d, e["id"], "chk"), False) for e in mains) if mains else False
    for e in mains:
        k = sk(w, d, e["id"], "chk")
        nv = not flip
        st.session_state.db[k] = nv
        st.session_state[k] = nv
    save_db(st.session_state.db)
    st.rerun()

st.caption("Tag abgeschlossen ✓" if all_done else f"Hauptübungen: {cd}/{ct}")

with st.expander("Export"):
    st.download_button("CSV (alle Wochen)", build_csv(db).encode("utf-8"), "gym_tracker_export.csv", "text/csv", on_click="ignore")
    st.download_button(
        "JSON-Backup",
        json.dumps(db, ensure_ascii=False, indent=2).encode("utf-8"),
        "gym_tracker_backup.json",
        "application/json",
        on_click="ignore",
    )
    st.download_button("Wochenzusammenfassung (.txt)", build_summary_text(db, w).encode("utf-8"), f"gym_woche_{w}.txt", "text/plain", on_click="ignore")

with st.expander("Hosting-Hinweise (iPhone im Gym)"):
    st.markdown(
        "- **Empfohlen:** Internet-Hosting (z. B. Streamlit Community Cloud), damit das iPhone ueberall zugreifen kann.\n"
        "- **Fallback:** lokal auf dem PC nur im selben Netzwerk/VPN nutzbar.\n"
        "- **Speicher:** SQLite bleibt nur dann dauerhaft, wenn das Hosting persistente Daten traegt."
    )
