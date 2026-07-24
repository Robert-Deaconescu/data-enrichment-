#!/usr/bin/env python3
"""Pasul 4 - Generarea tiparelor de e-mail nominale.
Pentru fiecare firma Pending cu persoana + domeniu propriu, genereaza tiparele
in ordinea probabilitatii din SKILL.md. Scrie work/05_tipare.csv
(un rand per firma, tipare separate cu ';', in ordine)."""
import re

import pandas as pd
from unidecode import unidecode

df = pd.read_csv("work/04_imbogatit.csv", dtype=str).fillna("")

ANAF_ORDER = df.get("obs_anaf", pd.Series([""] * len(df))).str.contains("persoana din ANAF")

PARTICLES = {"DE", "DEL", "VAN", "VON", "LA", "LE"}


def name_parts(person: str, anaf_order: bool):
    """Returneaza (prenume, nume_familie) - liste de tokenuri.
    ANAF: NUME PRENUME [PRENUME2]. Surse client: Prenume Nume (de regula)."""
    s = unidecode(person).strip()
    s = re.sub(r"[^A-Za-z\- ]", " ", s)
    toks = [t for t in re.split(r"\s+", s) if len(t) > 1 or t.upper() in PARTICLES]
    if len(toks) < 2:
        return None
    if anaf_order:
        fam, given = toks[0], toks[1:]
        fams = [fam]
    else:
        given, fams = toks[:-1], [toks[-1]]
    # prenume compus: primul token
    first = given[0].split("-")[0].lower()
    fam_full = [f.lower() for f in fams]
    return first, fam_full


def patterns(person: str, domain: str, anaf_order: bool):
    parts = name_parts(person, anaf_order)
    if not parts:
        return []
    first, fams = parts
    fam_variants = []
    for f in fams:
        if "-" in f:
            a, b = f.split("-", 1)
            fam_variants = [f.replace("-", "."), a, b]
        else:
            fam_variants = [f]
    out = []
    for fam in fam_variants:
        cand = [
            f"{first}.{fam}@{domain}",
            f"{first}@{domain}",
            f"{fam}.{first}@{domain}",
            f"{fam}@{domain}",
            f"{first}{fam}@{domain}",
            f"{first[0]}.{fam}@{domain}",
        ]
        for c in cand:
            if c not in out:
                out.append(c)
    return out


rows = []
for i, r in df.iterrows():
    if r["status"] != "Pending" or not r["persoana_fin"] or not r["domeniu"]:
        continue
    pats = patterns(r["persoana_fin"], r["domeniu"], bool(ANAF_ORDER.iloc[i]))
    if pats:
        rows.append({
            "id_firma": r["id_firma"],
            "firma": r["firma"],
            "persoana": r["persoana_fin"],
            "domeniu": r["domeniu"],
            "tipare": ";".join(pats),
            "nr_tipare": len(pats),
        })

out = pd.DataFrame(rows)
out.to_csv("work/05_tipare.csv", index=False)

with open("work/stats.md", "a") as f:
    f.write("\n## Pas 4 - Tipare e-mail\n\n")
    f.write(f"- Firme eligibile (Pending + persoana + domeniu propriu): {len(out)}\n")
    f.write(f"- Total tipare generate: {out['nr_tipare'].astype(int).sum() if len(out) else 0}\n")
    f.write(f"- Medie tipare/firma: {out['nr_tipare'].astype(int).mean():.1f}\n" if len(out) else "")

print(f"firme cu tipare: {len(out)}, total tipare: {out['nr_tipare'].astype(int).sum() if len(out) else 0}")
