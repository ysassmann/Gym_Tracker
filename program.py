from __future__ import annotations

PROG: dict[str, list] = {
    "squat": [65, 67, 70, 70, 72, 75, 77, 77, 87, 90, 92, 92, 95, 97, 100, 100, 102, 105, 107, 107, 110, 112, 115, 115],
    "cdl": [90, "–", 92, "–", 95, "–", 97, "–", 100, "–", 102, "–", 107, "–", 110, "–", 115, "–", 117, "–", 120, "–", 122, "–"],
    "rdl": ["–", 70, "–", 70, "–", 72, "–", 72, "–", 75, "–", 75, "–", 80, "–", 80, "–", 85, "–", 85, "–", 90, "–", 90],
    "bss": ["–", "BW", "–", "BW", "–", "BW", "–", "BW", "–", 10, "–", 10, "–", 12, "–", 12, "–", 14, "–", 14, "–", 16, "–", 16],
    "fc": [20, 20, 22, 22, 22, 24, 24, 24, 26, 26, 28, 28, 28, 30, 30, 30, 32, 32, 34, 34, 34, 36, 36, 36],
    "abd": [70, 70, 72, 72, 74, 74, 76, 76, 80, 80, 82, 82, 84, 84, 86, 86, 90, 90, 92, 92, 94, 94, 96, 96],
    "bench": [60, "–", 62, "–", 65, "–", 67, "–", 70, "–", 72, "–", 75, "–", 77, "–", 80, "–", 82, "–", 85, "–", 87, "–"],
    "incline": ["–", 16, "–", 16, "–", 17, "–", 17, "–", 18, "–", 18, "–", 19, "–", 19, "–", 20, "–", 20, "–", 21, "–", 21],
    "ohp": [35, 36.25, 37.5, 38.75, 38.75, 40, 41.25, 42.5, 42.5, 43.75, 45, 46.25, 46.25, 47.5, 48.75, 50, 50, 51.25, 52.5, 53.75, 53.75, 55, 56.25, 57.5],
    "pulu": [8, 8, 9, 9, 9, 10, 10, 10, "–", "–", "–", "–", "–", "–", "–", "–", "–", "–", "–", "–", "–", "–", "–", "–"],
    "pulw": ["–", "–", "–", "–", "–", "–", "–", "–", 0, 0, 2, 2, 2, 5, 5, 5, 5, 7, 7, 7, 7, 10, 10, 10],
    "dbrow": [22, 22, 24, 24, 24, 24, 26, 26, 26, 28, 28, 28, 30, 30, 32, 32, 32, 34, 34, 34, 36, 36, 38, 38],
    "lat": [10, 10, 10, 10, 10, 10, 10, 10, 12, 12, 12, 12, 12, 12, 12, 12, 14, 14, 14, 14, 14, 14, 14, 14],
    "rdf": [8, 8, 8, 8, 8, 8, 8, 8, 10, 10, 10, 10, 10, 10, 10, 10, 12, 12, 12, 12, 12, 12, 12, 12],
    "pc": [52, 53, 54, 54, 55, 56, 57, 57, 59, 60, 61, 61, 63, 64, 65, 65, 67, 68, 69, 69, 71, 72, 73, 73],
    "fs": [50, 52, 54, 54, 56, 58, 60, 60, 62, 64, 66, 66, 68, 70, 72, 72, 74, 76, 78, 78, 80, 82, 84, 84],
    "rdips": [6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 10, 10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 14],
    "wb": [10, 10, 11, 11, 11, 12, 12, 12, 13, 13, 14, 14, 14, 15, 15, 15, 16, 16, 17, 17, 17, 18, 18, 18],
    "mm": [10, 10, 10, 10, 10, 12, 12, 12, "–", "–", "–", "–", "–", "–", "–", "–", 12, 12, 12, 12, 14, 14, 14, 14],
    "thr": ["–", "–", "–", "–", "–", "–", "–", "–", 35, 37, 39, 39, 41, 43, 44, 44, "–", "–", "–", "–", "–", "–", "–", "–"],
    "bcurl": [25, 25, 27, 27, 27, 29, 29, 29, 31, 31, 33, 33, 33, 35, 35, 35, 37, 37, 39, 39, 39, 41, 41, 41],
    "hcurl": [12, 12, 12, 12, 13, 13, 13, 13, 14, 14, 14, 14, 15, 15, 15, 15, 16, 16, 16, 16, 17, 17, 17, 17],
    "skull": [20, 20, 22, 22, 22, 24, 24, 24, 26, 26, 28, 28, 28, 30, 30, 30, 32, 32, 34, 34, 34, 36, 36, 36],
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
DAY_LBL = {"A": "Unterkörper", "B": "Oberkörper", "C": "CF Skills", "D": "Arme", "E": "Laufen"}


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
            {"id": "w1", "name": "Rudern / Laufen", "presc": "5 min locker", "wu": True},
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
                    {
                        "id": "bss",
                        "name": "Bulgarian Split Squat",
                        "presc": f"3×8/Seite @ {p('bss', w) if p('bss', w) == 'BW' else str(p('bss', w)) + ' kg'}",
                        "tgt": p("bss", w),
                        "unit": "kg",
                        "alt": "Gerade Woche",
                    },
                ]
            ),
            {"id": "fc", "name": "Farmers Carry", "presc": f"3×30m @ {p('fc', w)} kg/Hand", "tgt": p("fc", w), "unit": "kg/Hand"},
            {"id": "abd", "name": "Abductor Machine", "presc": f"3×15 @ {p('abd', w)} kg", "tgt": p("abd", w), "unit": "kg"},
        ]
    if d == "B":
        return [
            {"id": "w1", "name": "Rudern / Laufen", "presc": "5 min locker", "wu": True},
            {"id": "bpa", "name": "Band Pull-Aparts", "presc": "2×10", "wu": True},
            {"id": "sc", "name": "Shoulder Circles", "presc": "2×10", "wu": True},
            {"id": "dhw", "name": "Dead Hangs", "presc": "3×20–40s", "wu": True},
            *(
                [{"id": "bench", "name": "Bench Press", "presc": f"4×{3 if ph == 3 else 6} @ {p('bench', w)} kg", "tgt": p("bench", w), "unit": "kg", "alt": "Ungerade Woche"}]
                if odd
                else [{"id": "incline", "name": "Incline DB Press", "presc": f"3×10 @ 2×{p('incline', w)} kg DB", "tgt": p("incline", w), "unit": "kg/DB", "alt": "Gerade Woche"}]
            ),
            {"id": "ohp", "name": "Strict Press (OHP)", "presc": f"4×6 @ {p('ohp', w)} kg", "tgt": p("ohp", w), "unit": "kg"},
            {"id": "hspu", "name": "HSPU", "presc": f"{'Box HSPU' if ph == 1 else 'Kipping HSPU'} 3×{p('hspu', w)}", "tgt": p("hspu", w), "unit": "Wdh"},
            *(
                [{"id": "pulu", "name": "Pull-ups (BW)", "presc": f"3×{p('pulu', w)} @ BW", "tgt": p("pulu", w), "unit": "Wdh"}]
                if ph == 1
                else [{"id": "pulw", "name": "Weighted Pull-ups", "presc": f"3×6 @ BW+{p('pulw', w)} kg", "tgt": p("pulw", w), "unit": "kg extra"}]
            ),
            {"id": "dbrow", "name": "DB Row (Neutral Grip)", "presc": f"3×8/Seite @ {p('dbrow', w)} kg", "tgt": p("dbrow", w), "unit": "kg"},
            {"id": "lat", "name": "Lateral Raises", "presc": f"3×12 @ 2×{p('lat', w)} kg", "tgt": p("lat", w), "unit": "kg DB"},
            {"id": "rdf", "name": "Rear Delt Fly", "presc": f"3×12 @ 2×{p('rdf', w)} kg", "tgt": p("rdf", w), "unit": "kg DB"},
            {"id": "wr", "name": "Wrist Roller / Grip", "presc": "3 Richtungen", "noinput": True},
        ]
    if d == "C":
        ex = [
            {"id": "w1", "name": "Rudern / Laufen", "presc": "5 min locker", "wu": True},
            {"id": "gm", "name": "Good Mornings", "presc": f"3×10 @ {20 if ph == 1 else 30 if ph == 2 else 40} kg", "wu": True},
            {"id": "pistolw", "name": "Pistol Squat", "presc": f"3×{p('pistol', w)}/Seite", "wu": True},
            {"id": "ohsc", "name": "OHS Warmup", "presc": f"3×5 @ {p('ohs', w)} kg", "wu": True},
            {"id": "pc", "name": "Power Clean", "presc": f"5×3 @ {p('pc', w)} kg", "tgt": p("pc", w), "unit": "kg"},
            {"id": "fs", "name": "Front Squat", "presc": f"3×5 @ {p('fs', w)} kg", "tgt": p("fs", w), "unit": "kg"},
            {"id": "rdips", "name": "Ring Dips", "presc": f"3×{p('rdips', w)}", "tgt": p("rdips", w), "unit": "Wdh"},
            {
                "id": "mu",
                "name": "Muscle-Up Progression",
                "presc": "Ring Support 3×20s" if ph == 1 else "Transition Drills 3×5" if ph == 2 else "Banded Muscle-Up 3×3",
                "noinput": True,
            },
            {"id": "wb", "name": "Wall Balls", "presc": f"4×{p('wb', w)} @ {6 if w <= 8 else 9} kg", "tgt": p("wb", w), "unit": "Wdh"},
        ]
        if p("mm", w) != "–":
            ex.append({"id": "mm", "name": "Man-Makers", "presc": f"3×6 @ 2×{p('mm', w)} kg DB", "tgt": p("mm", w), "unit": "kg DB"})
        if p("thr", w) != "–":
            ex.append({"id": "thr", "name": "Thrusters", "presc": f"3×8 @ {p('thr', w)} kg", "tgt": p("thr", w), "unit": "kg"})
        ex.append(
            {
                "id": "amrap",
                "name": f"AMRAP {12 if ph == 1 else 15 if ph == 2 else 20} min",
                "presc": (
                    "5 PC @ 45 kg / 10 Ring Dips / 15 Air Squat"
                    if ph == 1
                    else "5 Clean / 6 Man-Makers / 12 Wall Balls"
                    if ph == 2
                    else "Cindy: 5 Pull-ups / 10 Push-ups / 15 Air Squat"
                ),
                "noinput": True,
            }
        )
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
    return f"{w}_{d}_{eid}_{f}"


def cnt_done(db: dict, w: int, d: str) -> tuple[int, int]:
    exs = [e for e in day_exs(d, w) if not e.get("wu")]
    done = sum(1 for e in exs if db.get(sk(w, d, e["id"], "chk"), False))
    return done, len(exs)
