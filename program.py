from __future__ import annotations

PROG: dict[str, list] = {
    "squat": [52, 54, 56, 57, 58, 60, 62, 62, 63, 65, 66, 66, 68, 69, 70, 70, 71, 72, 73, 73, 74, 75, 76, 76],
    "cdl": [90, "–", 92, "–", 94, "–", 96, "–", 98, "–", 100, "–", 102, "–", 104, "–", 107, "–", 110, "–", 112, "–", 115, "–"],
    "rdl": ["–", 70, "–", 72, "–", 74, "–", 75, "–", 77, "–", 78, "–", 80, "–", 82, "–", 83, "–", 85, "–", 88, "–", 90],
    "bss": ["–", 12.5, "–", 14, "–", 14, "–", 16, "–", 16, "–", 18, "–", 18, "–", 20, "–", 20, "–", 22, "–", 22, "–", 24],
    "fc": [20, 20, 21, 21, 22, 22, 23, 23, 24, 24, 25, 25, 26, 26, 27, 27, 28, 28, 29, 29, 30, 30, 32, 32],
    "abd": [50, 50, 52, 52, 54, 54, 56, 56, 58, 58, 60, 60, 62, 62, 64, 64, 66, 66, 67, 67, 68, 68, 68, 68],
    "bench": [55, "–", 57, "–", 59, "–", 61, "–", 63, "–", 65, "–", 67, "–", 69, "–", 71, "–", 73, "–", 75, "–", 77, "–"],
    "incline": ["–", 55, "–", 57, "–", 58, "–", 60, "–", 61, "–", 62, "–", 63, "–", 64, "–", 65, "–", 66, "–", 67, "–", 69],
    "ohp": [35, 36.25, 36.25, 33, 33.75, 34.5, 35, 35, 35.75, 36.25, 37, 37, 37.5, 38, 38.75, 38.75, 39.5, 40, 40.75, 40.75, 41.5, 42, 42.5, 42.5],
    "pulu": [4, 4, 5, 5, 6, 6, 7, 8, "–", "–", "–", "–", "–", "–", "–", "–", "–", "–", "–", "–", "–", "–", "–", "–"],
    "pulw": ["–", "–", "–", "–", "–", "–", "–", "–", 0, 0, 2, 2, 2, 5, 5, 5, 5, 7, 7, 7, 7, 10, 10, 10],
    "dbrow": [22, 22, 23, 23, 24, 24, 25, 25, 26, 26, 27, 27, 28, 28, 29, 29, 30, 30, 31, 31, 32, 32, 33, 34],
    "lat": [6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10],
    "rdf": [35, 35, 37, 37, 39, 39, 40, 40, 42, 42, 44, 44, 45, 45, 47, 47, 48, 48, 49, 49, 50, 50, 50, 50],
    "pc": [52, 53, 54, 54, 55, 56, 57, 57, 58, 59, 60, 60, 61, 62, 63, 63, 64, 65, 66, 66, 67, 68, 69, 70],
    "fs": [52, 52, 53, 54, 55, 56, 57, 57, 58, 59, 61, 61, 62, 63, 64, 64, 65, 66, 68, 68, 69, 70, 70, 70],
    "rdips": [6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 10, 10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 14],
    "wb": [7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 11, 12, 12, 12, 13, 13, 13, 14, 14, 14, 15],
    "mm": [10, 10, 10, 10, 10, 12, 12, 12, "–", "–", "–", "–", "–", "–", "–", "–", 12, 12, 12, 12, 14, 14, 14, 14],
    "thr": ["–", "–", "–", "–", "–", "–", "–", "–", 35, 37, 39, 39, 41, 43, 44, 44, "–", "–", "–", "–", "–", "–", "–", "–"],
    "bcurl": [25, 25, 26, 26, 27, 27, 27, 28, 28, 29, 29, 29, 30, 30, 31, 31, 31, 32, 32, 33, 33, 33, 34, 35],
    "hcurl": [8, 8, 8, 9, 9, 9, 9, 9, 10, 10, 10, 10, 11, 11, 11, 11, 12, 12, 12, 12, 12, 13, 13, 13],
    "skull": [20, 20, 21, 21, 22, 22, 22, 23, 23, 24, 24, 24, 25, 25, 26, 26, 26, 27, 27, 28, 28, 28, 30, 32],
    "ohs": [20, 20, 22, 22, 22, 25, 25, 25, 27, 27, 30, 30, 30, 32, 32, 32, 35, 35, 37, 37, 37, 40, 40, 40],
    "coss": [12, 12, 12, 12, 14, 14, 14, 14, 16, 16, 16, 16, 18, 18, 20, 20, 20, 22, 22, 22, 24, 24, 24, 24],
    "pistol": [3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 10, 10],
    "hspu": [4, 4, 5, 5, 8, 8, 8, 8, 4, 4, 4, 4, 6, 6, 6, 6, 8, 8, 8, 8, 10, 10, 10, 10],
}

RPE_L = {
    1: "sehr leicht",
    2: "leicht",
    3: "moderat",
    4: "etwas anstrengend",
    5: "anstrengend",
    6: "anstrengend+",
    7: "sehr anstrengend",
    8: "sehr hart",
    9: "extrem hart",
    10: "maximal",
}

DELOAD = {4, 8, 12, 16, 20, 24}
DAYS = ["A", "B", "C", "D", "E"]
DAY_LBL = {"A": "Oberkörper", "B": "Unterkörper", "C": "CF Skills", "D": "Arme", "E": "Laufen"}


def p(k: str, w: int):
    arr = PROG.get(k)
    if not arr or w < 1 or w > len(arr):
        return "–"
    return arr[w - 1]


def day_exs(d: str, w: int) -> list[dict]:
    odd = w % 2 == 1
    ph = 1 if w <= 8 else (2 if w <= 16 else 3)
    if d == "A":
        return [
            {"id": "bpa", "name": "Band Pull-Aparts", "presc": "2×10", "wu": True},
            {"id": "sc", "name": "Shoulder Circles", "presc": "2×10", "wu": True},
            {"id": "dhw", "name": "Dead Hangs", "presc": "3×20-40s", "wu": True},
            *(
                [{"id": "bench", "name": "Bench Press", "presc": f"4×{3 if ph == 3 else 6} @ {p('bench', w)} kg", "tgt": p("bench", w), "unit": "kg", "alt": "Ungerade Woche"}]
                if odd
                else [{"id": "incline", "name": "Incline Press (Langhantel)", "presc": f"4×6 @ {p('incline', w)} kg", "tgt": p("incline", w), "unit": "kg", "alt": "Gerade Woche"}]
            ),
            {"id": "ohp", "name": "Strict Press (OHP)", "presc": f"4×6 @ {p('ohp', w)} kg", "tgt": p("ohp", w), "unit": "kg"},
            *(
                [{"id": "pulu", "name": "Pull-ups (BW)", "presc": f"3×{p('pulu', w)} @ BW", "tgt": p("pulu", w), "unit": "Wdh"}]
                if ph == 1
                else [{"id": "pulw", "name": "Weighted Pull-ups", "presc": f"3×6 @ BW+{p('pulw', w)} kg", "tgt": p("pulw", w), "unit": "kg extra"}]
            ),
            {"id": "dbrow", "name": "DB Row (Neutral Grip)", "presc": f"3×8/Seite @ {p('dbrow', w)} kg", "tgt": p("dbrow", w), "unit": "kg"},
            {"id": "lat", "name": "Lateral Raises", "presc": f"3×12 @ 2×{p('lat', w)} kg", "tgt": p("lat", w), "unit": "kg DB"},
            {"id": "rdf", "name": "Rear Delt Fly / Machine", "presc": f"3×12 @ {p('rdf', w)} kg", "tgt": p("rdf", w), "unit": "kg"},
        ]
    if d == "B":
        return [
            {"id": "clam", "name": "Clamshells (Band)", "presc": "2×12/Seite", "wu": True},
            {"id": "cossw", "name": "Cossack Squat", "presc": f"2×8/Seite @ {p('coss', w)} kg KB", "wu": True},
            {"id": "sldlw", "name": "Single-Leg Deadlift", "presc": "2×6/Seite @ 8 kg KB", "wu": True},
            {"id": "ohsw", "name": "Overhead Squat (Mob-Check)", "presc": f"3×5 @ {p('ohs', w)} kg", "wu": True},
            {"id": "sq", "name": "Tempo Squat (3-1-1)" if ph == 1 else "Back Squat", "presc": f"4×5 @ {p('squat', w)} kg", "tgt": p("squat", w), "unit": "kg"},
            *(
                [{"id": "cdl", "name": "Conventional Deadlift", "presc": f"3×5 @ {p('cdl', w)} kg", "tgt": p("cdl", w), "unit": "kg", "alt": "Ungerade Woche"}]
                if odd
                else [
                    {"id": "rdl", "name": "Romanian Deadlift", "presc": f"3×8 @ {p('rdl', w)} kg", "tgt": p("rdl", w), "unit": "kg", "alt": "Gerade Woche"},
                    {"id": "bss", "name": "Bulgarian Split Squat", "presc": f"3×8/Seite @ {p('bss', w)} kg", "tgt": p("bss", w), "unit": "kg", "alt": "Gerade Woche"},
                ]
            ),
            {"id": "fc", "name": "Farmers Carry", "presc": f"3×30m @ {p('fc', w)} kg/Hand", "tgt": p("fc", w), "unit": "kg"},
            *(
                [{"id": "abd", "name": "Abductor Machine", "presc": f"3×15 @ {p('abd', w)} kg", "tgt": p("abd", w), "unit": "kg", "alt": "Ungerade Woche"}]
                if odd
                else []
            ),
        ]
    if d == "C":
        ex = [
            {"id": "w1", "name": "Rudern / Laufen", "presc": "5 min locker", "wu": True},
            {"id": "gm", "name": "Good Mornings", "presc": f"3×10 @ {20 if ph == 1 else 30 if ph == 2 else 40} kg", "wu": True},
            {"id": "pistolw", "name": "Pistol Squat", "presc": f"3×{p('pistol', w)}/Seite", "wu": True},
            {"id": "ohsc", "name": "OHS Warmup", "presc": f"3×5 @ {p('ohs', w)} kg", "wu": True},
            {"id": "hspu", "name": "HSPU", "presc": f"{'Box HSPU' if ph == 1 else 'Kipping HSPU'} 3×{p('hspu', w)}", "tgt": p("hspu", w), "unit": "Wdh"},
            {"id": "pc", "name": "Power Clean", "presc": f"5×3 @ {p('pc', w)} kg", "tgt": p("pc", w), "unit": "kg"},
            {"id": "fs", "name": "Front Squat", "presc": f"3×5 @ {p('fs', w)} kg", "tgt": p("fs", w), "unit": "kg"},
            {"id": "rdips", "name": "Ring Dips", "presc": f"3×{p('rdips', w)}", "tgt": p("rdips", w), "unit": "Wdh"},
            {
                "id": "mu",
                "name": "Muscle-Up Progression",
                "presc": "Ring Support 3×20s" if ph == 1 else "Transition Drills 3×5" if ph == 2 else "Banded Muscle-Up 3×3",
                "noinput": True,
            },
            {"id": "wb", "name": "Wall Balls", "presc": f"4×{p('wb', w)} @ {6 if w <= 8 else 9}kg", "tgt": p("wb", w), "unit": "Wdh"},
        ]
        if p("mm", w) != "–":
            ex.append({"id": "mm", "name": "Man-Makers", "presc": f"3×6 @ 2×{p('mm', w)} kg DB", "tgt": p("mm", w), "unit": "kg DB"})
        if p("thr", w) != "–":
            ex.append({"id": "thr", "name": "Thrusters", "presc": f"3×8 @ {p('thr', w)} kg", "tgt": p("thr", w), "unit": "kg"})
        return ex
    if d == "D":
        return [
            {"id": "rb1", "name": "Rice Bucket – Spreizen", "presc": "2×30s", "wu": True},
            {"id": "rb2", "name": "Rice Bucket – Rotation", "presc": "2×30s", "wu": True},
            {"id": "rb3", "name": "Rice Bucket – Kreisen", "presc": "2×30s", "wu": True},
            {"id": "bcurl", "name": "Barbell Curl", "presc": f"3×10 @ {p('bcurl', w)} kg", "tgt": p("bcurl", w), "unit": "kg"},
            {"id": "hcurl", "name": "Hammer Curl", "presc": f"3×10/Seite @ {p('hcurl', w)} kg", "tgt": p("hcurl", w), "unit": "kg"},
            {"id": "tpd", "name": "Triceps Pushdown", "presc": "3×12 @ mittel", "noinput": True},
            {"id": "skull", "name": "Skull Crushers", "presc": f"3×10 @ {p('skull', w)} kg", "tgt": p("skull", w), "unit": "kg"},
            {"id": "wc", "name": "Wrist Curl", "presc": "3×15 @ 8–12 kg", "noinput": True},
            {"id": "rwc", "name": "Reverse Wrist Curl", "presc": "3×15 @ 6–10 kg", "noinput": True},
        ]
    if d == "E":
        ex = [{"id": "run", "name": "Easy Run Zone 2", "presc": f"{30 if ph == 1 else 35 if ph == 2 else 40} min Konversationstempo", "noinput": True}]
        if ph >= 2:
            ex.append({"id": "tempo", "name": "Tempo Run (2×/Monat optional)", "presc": "3×8 min schnell, 2 min Gehpause", "noinput": True})
        return ex
    return []


def sk(w: int, d: str, eid: str, f: str) -> str:
    return f"v2_{w}_{d}_{eid}_{f}"


def cnt_done(db: dict, w: int, d: str) -> tuple[int, int]:
    exs = [e for e in day_exs(d, w) if not e.get("wu")]
    done = sum(1 for e in exs if db.get(sk(w, d, e["id"], "chk"), False))
    return done, len(exs)
