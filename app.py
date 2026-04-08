import csv
import json
import os
from io import StringIO
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from streamlit.errors import StreamlitSecretNotFoundError

from program import DAY_LBL, DAYS, DELOAD, RPE_L, cnt_done, day_exs, sk

load_dotenv()
STATE_PATH = Path(__file__).resolve().parent / "gymtracker_state.json"


def expected_password() -> str:
    v = os.getenv("GYM_APP_PASSWORD")
    if v:
        return v
    try:
        return str(st.secrets["GYM_APP_PASSWORD"])
    except (StreamlitSecretNotFoundError, KeyError):
        return "Gym!"


def load_db() -> dict:
    if not STATE_PATH.is_file():
        return {}
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def save_db(db: dict) -> None:
    STATE_PATH.write_text(json.dumps(db, ensure_ascii=False, indent=0), encoding="utf-8")


def ensure_db():
    if "db" not in st.session_state:
        st.session_state.db = load_db()


def persist_key(key: str):
    st.session_state.db[key] = st.session_state[key]
    save_db(st.session_state.db)


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

opts = [f"{x} · {DAY_LBL[x][:6]}" for x in DAYS]
idx = DAYS.index(d)
choice = st.radio("Tag", range(len(DAYS)), horizontal=True, format_func=lambda i: opts[i], index=idx, label_visibility="collapsed")
st.session_state.day = DAYS[choice]
d = st.session_state.day

exs = day_exs(d, w)
wus = [e for e in exs if e.get("wu")]
mains = [e for e in exs if not e.get("wu")]


def ex_block(e: dict, warmup: bool):
    k_chk = sk(w, d, e["id"], "chk")
    init_widget(k_chk, False)
    ca, cb = st.columns([1, 6])
    with ca:
        st.checkbox("✓", key=k_chk, on_change=persist_key, args=(k_chk,), label_visibility="collapsed")
    with cb:
        tag = " *(Warmup)*" if warmup else ""
        st.markdown(f"**{e['name']}**{tag}  \n{e['presc']}")
        if e.get("tgt") not in (None, "", "–"):
            st.caption(f"Ziel: {e['tgt']} {e.get('unit', '')}")
        if e.get("alt"):
            st.caption(e["alt"])
    if not e.get("noinput"):
        u = e.get("unit") or "kg"
        tgt = e.get("tgt", "")
        pholder = str(tgt) if tgt not in (None, "", "–") else "—"
        k_aw, k_ar, k_an = sk(w, d, e["id"], "aw"), sk(w, d, e["id"], "ar"), sk(w, d, e["id"], "an")
        init_widget(k_aw, "")
        init_widget(k_ar, "")
        init_widget(k_an, "")
        i1, i2 = st.columns(2)
        with i1:
            st.text_input(f"Erreicht ({u})", key=k_aw, placeholder=pholder, on_change=persist_key, args=(k_aw,))
        with i2:
            st.text_input("Wdh", key=k_ar, placeholder="—", on_change=persist_key, args=(k_ar,))
        st.text_input("Notiz", key=k_an, placeholder="…", on_change=persist_key, args=(k_an,))
    st.divider()


if wus:
    st.subheader("Warmup")
    for e in wus:
        ex_block(e, True)

st.subheader("Hauptübungen")
for e in mains:
    ex_block(e, False)

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

cd, ct = cnt_done(db, w, d)
all_done = ct > 0 and cd == ct
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
    st.download_button("CSV (alle Wochen)", build_csv(db).encode("utf-8"), "gym_tracker_export.csv", "text/csv")
    st.download_button(
        "JSON-Backup",
        json.dumps(db, ensure_ascii=False, indent=2).encode("utf-8"),
        "gym_tracker_backup.json",
        "application/json",
    )
    st.download_button("Wochenzusammenfassung (.txt)", build_summary_text(db, w).encode("utf-8"), f"gym_woche_{w}.txt", "text/plain")
