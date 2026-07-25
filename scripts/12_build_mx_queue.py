#!/usr/bin/env python3
"""Runda de recuperare MX - construieste coada de verificare pentru firmele
fara site confirmat dar cu domeniu candidat cu server de email activ (MX).

Filtru de siguranta: domeniul candidat trebuie sa semene REAL cu numele firmei
(altfel un "valid" ar insemna mailboxul altcuiva - ex. electronics.com pentru
"A E ELECTRONICS"). Excludem si domeniile respinse la auditul din pasul 09.

Regula de acceptare (stats.md): tipar administrator valid = nominal;
doar office@ = generic incert. office@ se adauga ultimul in lista.
Scrie work/10_coada_mx_run.csv (id_firma,tipare).
"""
import re
import sys

import pandas as pd
from rapidfuzz import fuzz
from unidecode import unidecode

sys.path.insert(0, "scripts")
LEGAL = re.compile(r"\b(SRL|SA|SRL-D|PFA|II|SNC|SCS|SCA|COM|PROD|IMPEX|IMPORT|EXPORT|TRADING|GRUP|GROUP|RO)\b")

cand = pd.read_csv("work/11_candidati_mx.csv", dtype=str).fillna("")

# domenii respinse la audit / manual
bad = set()
for f, col in [("work/09_audit_domenii.csv", "verdict"), ("work/domenii_de_verificat_manual.csv", "verdict")]:
    try:
        a = pd.read_csv(f, dtype=str).fillna("")
        bad |= set(a[a[col].str.lower().isin(["gresit", "exclus", "incert"])]["domeniu"])
    except FileNotFoundError:
        pass

GENERIC_STEMS = {"electronics", "construct", "trading", "company", "office", "impex",
                 "prod", "com", "group", "grup", "service", "servicii", "consult",
                 "market", "media", "auto", "trans", "expert", "total", "global"}


def firm_norm(name):
    s = unidecode(name).upper()
    s = LEGAL.sub(" ", s)
    s = re.sub(r"[^A-Z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def domain_ok(domain, firma):
    stem = domain.split(".")[0].lower()
    if len(stem) < 4 or stem in GENERIC_STEMS:
        return False
    fn = firm_norm(firma)
    compact = fn.replace(" ", "").lower()
    if stem in compact or compact in stem:
        return True
    return fuzz.partial_ratio(stem, fn.lower()) >= 85 and len(stem) >= 5


PARTICLES = {"DE", "DEL", "VAN", "VON", "LA", "LE"}


def name_parts(person):
    s = unidecode(person).strip()
    s = re.sub(r"[^A-Za-z\- ]", " ", s)
    toks = [t for t in re.split(r"\s+", s) if len(t) > 1 or t.upper() in PARTICLES]
    if len(toks) < 2:
        return None
    # candidatii MX vin din 11_mx - persoana e in ordinea ANAF (NUME Prenume)
    fam, given = toks[0], toks[1:]
    first = given[0].split("-")[0].lower()
    return first, fam.lower()


def patterns(person, domain):
    parts = name_parts(person)
    if not parts:
        return []
    first, fam = parts
    fams = [fam.replace("-", "."), *fam.split("-")] if "-" in fam else [fam]
    out = []
    for f in fams:
        for c in [f"{first}.{f}@{domain}", f"{first}@{domain}", f"{f}.{first}@{domain}",
                  f"{f}@{domain}", f"{first}{f}@{domain}", f"{first[0]}.{f}@{domain}"]:
            if c not in out:
                out.append(c)
    return out


rows, excl_dom, no_dom = [], 0, 0
for _, r in cand.iterrows():
    doms = [d for d in r["candidati_mx"].split(";") if d and d not in bad]
    doms = [d for d in doms if domain_ok(d, r["firma"])]
    if not doms:
        excl_dom += 1
        continue
    dom = doms[0]
    pats = patterns(r["persoana"], dom) if r["persoana"] else []
    pats.append(f"office@{dom}")
    rows.append({"id_firma": r["id_firma"], "tipare": ";".join(pats)})

out = pd.DataFrame(rows)
out.to_csv("work/10_coada_mx_run.csv", index=False)
n_pats = sum(len(r["tipare"].split(";")) for r in rows)

with open("work/stats.md", "a") as f:
    f.write("\n## Runda MX - coada construita\n\n")
    f.write(f"- Firme candidate: {len(cand)}; excluse de filtrul de siguranta: {excl_dom}\n")
    f.write(f"- Firme in coada MX: {len(out)}; tipare totale (max): {n_pats}\n")

print(f"coada MX: {len(out)} firme (excluse {excl_dom} cu domenii nesigure), max {n_pats} verificari", flush=True)
